# Serverless Todo Application

A full-stack serverless todo application built with React and Azure Functions (Python), using Azure Table Storage for data persistence.

## Prerequisites

- **Node.js** v14 or higher
- **Python** 3.9 or higher
- **Azure Functions Core Tools** v4.x
- **Azure CLI** (for deployment)
- **Azure Storage Account** (or Azurite for local development)

Check your versions:
```bash
node --version
python3 --version
func --version
az --version
```

## Local Development Setup

### 1. Clone and Install Dependencies

```bash
git clone https://github.com/jqzba/Ele_v1.git
cd Ele_v1

# Install frontend dependencies
npm install

# Install backend dependencies
cd todo_api
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Azure Storage

Get your Azure Storage connection string:

```bash
az login
az storage account show-connection-string \
  --name YOUR_STORAGE_ACCOUNT \
  --resource-group YOUR_RESOURCE_GROUP \
  --output tsv
```

Create `todo_api/local.settings.json`:
```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
    "AZURE_STORAGE_CONNECTION_STRING": "YOUR_CONNECTION_STRING_HERE",
    "TABLE_NAME": "todos"
  }
}
```

**Note:** You can use Azurite for local development instead of Azure Storage:
```bash
npm install -g azurite
azurite --silent --location ~/azurite
# Set AZURE_STORAGE_CONNECTION_STRING="UseDevelopmentStorage=true"
```

### 3. Run the Application

Open two terminals:

**Terminal 1 - Backend:**
```bash
cd todo_api
source .venv/bin/activate
func start
```
Backend runs on http://localhost:7071

**Terminal 2 - Frontend:**
```bash
npm start
```
Frontend runs on http://localhost:3000

## Configuration

### API Endpoints

The frontend connects to the backend API at `http://localhost:7071/api/todo`. 

To change this, update `API_BASE_URL` in `src/TodoApp.jsx`:
```javascript
const API_BASE_URL = 'http://localhost:7071/api/todo';
```

### Environment Variables

**Backend** (`todo_api/local.settings.json`):
- `AZURE_STORAGE_CONNECTION_STRING` - Azure Storage connection string
- `TABLE_NAME` - Table name (default: "todos")

**Important:** `local.settings.json` is git-ignored to protect your secrets.

### CORS

CORS is configured in `todo_api/host.json` to allow all origins for development. For production, restrict to your specific domain.

## How to Deploy to Azure

### Deploy Backend (Azure Functions)

1. Create Azure resources:
```bash
# Create resource group
az group create --name rg-todoapp --location eastus

# Create storage account
az storage account create \
  --name todostorage$(date +%s) \
  --resource-group rg-todoapp \
  --location eastus \
  --sku Standard_LRS

# Create Function App
az functionapp create \
  --name todo-api-app \
  --storage-account YOUR_STORAGE_ACCOUNT \
  --resource-group rg-todoapp \
  --consumption-plan-location eastus \
  --runtime python \
  --runtime-version 3.9 \
  --functions-version 4
```

2. Configure app settings:
```bash
az functionapp config appsettings set \
  --name todo-api-app \
  --resource-group rg-todoapp \
  --settings \
    AZURE_STORAGE_CONNECTION_STRING="YOUR_CONNECTION_STRING" \
    TABLE_NAME="todos"
```

3. Deploy the functions:
```bash
cd todo_api
func azure functionapp publish todo-api-app
```

### Deploy Frontend (Azure Static Web Apps)

1. Build the React app:
```bash
npm run build
```

2. Deploy to Azure Static Web Apps:
```bash
# Install SWA CLI
npm install -g @azure/static-web-apps-cli

# Deploy
swa deploy ./build \
  --app-name todo-frontend \
  --resource-group rg-todoapp
```

3. Update `src/TodoApp.jsx` with your deployed backend URL:
```javascript
const API_BASE_URL = 'https://todo-api-app.azurewebsites.net/api/todo';
```

**Note:** For automated infrastructure deployment using Bicep, see the [infra/](infra/) directory.

## Known Limitations and Assumptions

### Limitations

1. **No Authentication** - API endpoints are anonymous. Anyone with the URL can access the data.

2. **Single Partition** - All todos use `PartitionKey='default'`. This works for small-scale use but won't scale efficiently for large datasets.

3. **No User Isolation** - All users see the same todos. There's no per-user data separation.

4. **No Pagination** - All todos are loaded at once. This could be slow with thousands of items.

5. **No Edit Function** - You can only create and delete todos. Editing existing todos is not implemented.

6. **Client-side Validation Only** - Limited validation on title field. Should add length limits and content sanitization for production.

7. **CORS Wildcard** - Development uses `allowedOrigins: ["*"]` which should be restricted in production.

### Assumptions

- **RowKey as Timestamp** - Using millisecond timestamp ensures uniqueness and provides chronological ordering
- **Auto-refresh on Mutations** - After creating or deleting a todo, the entire list is re-fetched to ensure consistency
- **Default Table Name** - Uses "todos" as the table name unless specified otherwise
- **Local Development** - Assumes you have the necessary tools installed and an Azure subscription for deployment

## Troubleshooting

**Backend won't start - Module not found:**
```bash
cd todo_api
source .venv/bin/activate
pip install -r requirements.txt
```

**Frontend can't connect:**
- Check backend is running at http://localhost:7071/api/health
- Verify `API_BASE_URL` in `src/TodoApp.jsx`

**Storage connection failed:**
- Verify `AZURE_STORAGE_CONNECTION_STRING` in `local.settings.json`
- Or use Azurite for local development
