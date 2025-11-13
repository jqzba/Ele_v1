import azure.functions as func
import logging
import json
import time
import os
from datetime import datetime
from azure.data.tables import TableServiceClient, TableClient
from azure.core.exceptions import ResourceNotFoundError, ResourceExistsError

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Helper function to get table client
def get_table_client():
    """
    Get a TableClient instance for the 'todos' table.
    Creates the table if it doesn't exist.
    """
    try:
        # Get connection string from environment variables
        connection_string = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        
        if not connection_string:
            logging.error('AZURE_STORAGE_CONNECTION_STRING not found in environment variables')
            return None
        
        # Create TableServiceClient
        table_service_client = TableServiceClient.from_connection_string(connection_string)
        
        # Get or create table client for 'todos' table
        table_name = os.environ.get('TABLE_NAME', 'todos')
        table_client = table_service_client.get_table_client(table_name)
        
        # Create table if it doesn't exist
        try:
            table_service_client.create_table(table_name)
            logging.info(f'Created table: {table_name}')
        except ResourceExistsError:
            logging.info(f'Table {table_name} already exists')
        
        return table_client
    
    except Exception as e:
        logging.error(f'Error creating table client: {str(e)}')
        return None

@app.route(route="hello", auth_level=func.AuthLevel.ANONYMOUS)
def hello_world(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name') if req_body else None

    if name:
        return func.HttpResponse(
            json.dumps({
                "message": f"Hello {name} from Azure Functions!",
                "status": "success"
            }),
            status_code=200,
            headers={'Content-Type': 'application/json'}
        )
    else:
        return func.HttpResponse(
            json.dumps({
                "message": "Hello from Azure Functions!",
                "status": "success"
            }),
            status_code=200,
            headers={'Content-Type': 'application/json'}
        )

@app.route(route="health", auth_level=func.AuthLevel.ANONYMOUS)
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Health check endpoint called.')
    
    return func.HttpResponse(
        json.dumps({
            "status": "healthy",
            "message": "Todo API is running"
        }),
        status_code=200,
        headers={'Content-Type': 'application/json'}
    )

@app.route(route="todo", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def get_todos(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('GET /api/todo - Retrieving all todos')
    
    try:
        # Get table client
        table_client = get_table_client()
        
        if not table_client:
            return func.HttpResponse(
                json.dumps({
                    "error": "Failed to connect to table storage"
                }),
                status_code=500,
                headers={'Content-Type': 'application/json'}
            )
        
        # Query all entities from the table
        todos = []
        entities = table_client.list_entities()
        
        for entity in entities:
            todo = {
                "id": entity['RowKey'],
                "title": entity.get('title', ''),
                "timestamp": entity.get('timestamp', ''),
                "partitionKey": entity['PartitionKey'],
                "rowKey": entity['RowKey']
            }
            todos.append(todo)
        
        logging.info(f'Retrieved {len(todos)} todos')
        
        return func.HttpResponse(
            json.dumps(todos),
            status_code=200,
            headers={'Content-Type': 'application/json'}
        )
    
    except Exception as e:
        logging.error(f'Error retrieving todos: {str(e)}')
        return func.HttpResponse(
            json.dumps({
                "error": "An error occurred while retrieving todos",
                "details": str(e)
            }),
            status_code=500,
            headers={'Content-Type': 'application/json'}
        )

@app.route(route="todo", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def create_todo(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('POST /api/todo - Creating new todo')
    
    try:
        # Parse request body
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({
                "error": "Invalid JSON in request body"
            }),
            status_code=400,
            headers={'Content-Type': 'application/json'}
        )
    
    # Validate that title field exists and is not empty
    title = req_body.get('title', '').strip()
    if not title:
        return func.HttpResponse(
            json.dumps({
                "error": "Title is required and cannot be empty"
            }),
            status_code=400,
            headers={'Content-Type': 'application/json'}
        )
    
    try:
        # Get table client
        table_client = get_table_client()
        
        if not table_client:
            return func.HttpResponse(
                json.dumps({
                    "error": "Failed to connect to table storage"
                }),
                status_code=500,
                headers={'Content-Type': 'application/json'}
            )
        
        # Generate unique RowKey using timestamp
        row_key = str(int(time.time() * 1000))  # Millisecond timestamp
        partition_key = 'default'
        
        # Create entity for Azure Table Storage
        entity = {
            'PartitionKey': partition_key,
            'RowKey': row_key,
            'title': title,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        # Insert entity into table
        table_client.create_entity(entity)
        
        # Create response object
        new_todo = {
            "id": row_key,
            "title": title,
            "timestamp": entity['timestamp'],
            "partitionKey": partition_key,
            "rowKey": row_key
        }
        
        logging.info(f'Created todo with RowKey: {row_key}')
        
        # Return created todo with 201 status
        return func.HttpResponse(
            json.dumps(new_todo),
            status_code=201,
            headers={'Content-Type': 'application/json'}
        )
    
    except Exception as e:
        logging.error(f'Error creating todo: {str(e)}')
        return func.HttpResponse(
            json.dumps({
                "error": "An error occurred while creating the todo",
                "details": str(e)
            }),
            status_code=500,
            headers={'Content-Type': 'application/json'}
        )

@app.route(route="todo/{partitionKey}/{rowKey}", methods=["DELETE"], auth_level=func.AuthLevel.ANONYMOUS)
def delete_todo(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('DELETE /api/todo - Deleting todo')
    
    try:
        # Get the partition key and row key from route parameters
        partition_key = req.route_params.get('partitionKey')
        row_key = req.route_params.get('rowKey')
        
        logging.info(f'Attempting to delete todo with PartitionKey: {partition_key}, RowKey: {row_key}')
        
        # Get table client
        table_client = get_table_client()
        
        if not table_client:
            return func.HttpResponse(
                json.dumps({
                    "error": "Failed to connect to table storage"
                }),
                status_code=500,
                headers={'Content-Type': 'application/json'}
            )
        
        # Try to get the entity first to check if it exists
        try:
            entity = table_client.get_entity(partition_key=partition_key, row_key=row_key)
            
            # Delete the entity
            table_client.delete_entity(partition_key=partition_key, row_key=row_key)
            
            logging.info(f'Successfully deleted todo with RowKey: {row_key}')
            
            # Return success message with 200 status
            return func.HttpResponse(
                json.dumps({
                    "message": "Todo deleted successfully",
                    "deleted": {
                        "id": row_key,
                        "title": entity.get('title', ''),
                        "timestamp": entity.get('timestamp', ''),
                        "partitionKey": partition_key,
                        "rowKey": row_key
                    }
                }),
                status_code=200,
                headers={'Content-Type': 'application/json'}
            )
        
        except ResourceNotFoundError:
            logging.warning(f'Todo with PartitionKey: {partition_key}, RowKey: {row_key} not found')
            return func.HttpResponse(
                json.dumps({
                    "error": "Todo item not found"
                }),
                status_code=404,
                headers={'Content-Type': 'application/json'}
            )
    
    except Exception as e:
        logging.error(f'Error deleting todo: {str(e)}')
        return func.HttpResponse(
            json.dumps({
                "error": "An error occurred while deleting the todo",
                "details": str(e)
            }),
            status_code=500,
            headers={'Content-Type': 'application/json'}
        )