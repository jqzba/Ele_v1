# Todo API - Azure Functions Backend

This is the backend API for the Ele Todo application built with Azure Functions and Python.

## Setup

1. **Install Azure Functions Core Tools**:
   ```bash
   npm install -g azure-functions-core-tools@4 --unsafe-perm true
   ```

2. **Create Python virtual environment**:
   ```bash
   cd todo_api
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up local settings**:
   ```bash
   cp local.settings.json.example local.settings.json
   # Edit local.settings.json with your Azure Storage connection string
   ```

## Running Locally

```bash
func start
```

The API will be available at `http://localhost:7071`

## Endpoints

- `GET /api/hello` - Simple hello world endpoint
- `GET /api/health` - Health check endpoint

## Environment Variables

- `AZURE_STORAGE_CONNECTION_STRING` - Azure Storage connection string for data tables
- `TABLE_NAME` - Name of the Azure Table Storage table (default: "todos")

## Deployment

```bash
func azure functionapp publish <your-function-app-name>
```