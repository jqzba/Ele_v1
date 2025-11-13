# Azure Table Storage Setup

## Overview
The Todo API now uses Azure Table Storage for persistent data storage instead of in-memory storage.

## Configuration

### Option 1: Use Azure Storage Account (Recommended for Production)

1. Create an Azure Storage Account:
   - Go to Azure Portal
   - Create a new Storage Account
   - Copy the connection string

2. Update `local.settings.json`:
   ```json
   {
     "IsEncrypted": false,
     "Values": {
       "AzureWebJobsStorage": "UseDevelopmentStorage=true",
       "FUNCTIONS_WORKER_RUNTIME": "python",
       "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
       "AZURE_STORAGE_CONNECTION_STRING": "<YOUR_CONNECTION_STRING_HERE>",
       "TABLE_NAME": "todos"
     }
   }
   ```

### Option 2: Use Azurite Storage Emulator (For Local Development)

1. Install Azurite:
   ```bash
   npm install -g azurite
   ```

2. Start Azurite:
   ```bash
   azurite --silent --location ~/azurite --debug ~/azurite/debug.log
   ```

3. Update `local.settings.json`:
   ```json
   {
     "IsEncrypted": false,
     "Values": {
       "AzureWebJobsStorage": "UseDevelopmentStorage=true",
       "FUNCTIONS_WORKER_RUNTIME": "python",
       "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
       "AZURE_STORAGE_CONNECTION_STRING": "UseDevelopmentStorage=true",
       "TABLE_NAME": "todos"
     }
   }
   ```

## API Endpoints

### GET /api/todo
Retrieve all todos from Azure Table Storage.

**Response:**
```json
[
  {
    "id": "1731491234567",
    "title": "Buy groceries",
    "timestamp": "2025-11-13T10:00:00.000000Z",
    "partitionKey": "default",
    "rowKey": "1731491234567"
  }
]
```

### POST /api/todo
Create a new todo in Azure Table Storage.

**Request Body:**
```json
{
  "title": "My new todo"
}
```

**Response (201):**
```json
{
  "id": "1731491234567",
  "title": "My new todo",
  "timestamp": "2025-11-13T10:00:00.000000Z",
  "partitionKey": "default",
  "rowKey": "1731491234567"
}
```

### DELETE /api/todo/{partitionKey}/{rowKey}
Delete a todo from Azure Table Storage.

**Response (200):**
```json
{
  "message": "Todo deleted successfully",
  "deleted": {
    "id": "1731491234567",
    "title": "Buy groceries",
    "timestamp": "2025-11-13T10:00:00.000000Z",
    "partitionKey": "default",
    "rowKey": "1731491234567"
  }
}
```

## Testing

Run the comprehensive test script:
```bash
./test_azure_storage.sh
```

Make sure the Azure Functions are running:
```bash
func start
```

## Table Structure

**Table Name:** `todos`

**Schema:**
- **PartitionKey:** `default` (all todos use the same partition)
- **RowKey:** Unique timestamp (milliseconds)
- **title:** The todo title (string)
- **timestamp:** ISO 8601 timestamp (string)

## Error Handling

All endpoints include comprehensive error handling:
- 400: Invalid request (empty title, invalid JSON)
- 404: Todo not found
- 500: Server error (connection issues, storage errors)

## Notes

- The table is automatically created if it doesn't exist when the function starts
- All todos are stored in the same partition (`default`) for simplicity
- RowKey is generated using millisecond timestamp for uniqueness
- Connection string is read from `AZURE_STORAGE_CONNECTION_STRING` environment variable
