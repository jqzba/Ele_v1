# Todo App

A simple full-stack todo application built with React and Azure Functions. Uses Azure Table Storage for persistence.

## Prerequisites

You'll need these installed:

- **Node.js** 14+ (I used v18.17.0)
- **Python** 3.9+ (tested with 3.9.6)
- **Azure Functions Core Tools** v4
- **Azure CLI** (if you want to deploy)
- An **Azure subscription** with a Storage Account

Quick version check:
```bash
node --version
python3 --version
func --version
az --version
```

## Local Development Setup

### Getting Started

Clone the repo and install dependencies:

```bash
git clone https://github.com/jqzba/Ele_v1.git
cd Ele_v1

# Frontend
npm install

# Backend
cd todo_api
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Configure Azure Storage

You'll need a connection string from Azure Storage. Get it like this:

```bash
az login
az storage account show-connection-string \
  --name YOUR_STORAGE_ACCOUNT_NAME \
  --resource-group YOUR_RESOURCE_GROUP \
  --output tsv
```

Then create `todo_api/local.settings.json` (this file is gitignored):

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
    "AZURE_STORAGE_CONNECTION_STRING": "your_connection_string_here",
    "TABLE_NAME": "todos"
  }
}
```

There's an example file (`local.settings.json.example`) you can copy.

### Run It

Open two terminal windows:

**Backend (Terminal 1):**
```bash
cd todo_api
source .venv/bin/activate
func start
```

The API runs at `http://localhost:7071`

**Frontend (Terminal 2):**
```bash
npm start
```

The app opens at `http://localhost:3000`

## Deployment to Azure

I only tested this locally, but here's how you'd deploy it:

### Using Bicep (Infrastructure as Code)

There are Bicep templates in the `infra/` folder that set up the Azure Storage Account and Table Storage. To use them:

```bash
cd infra
az deployment group create \
  --resource-group YOUR_RESOURCE_GROUP \
  --template-file main.bicep \
  --parameters main.dev.bicepparam
```

This creates the storage resources you need.

### Manual Deployment

If you prefer doing it manually:

**1. Deploy the Backend:**

```bash
# Create a Function App (you'll need a storage account first)
az functionapp create \
  --name YOUR_FUNCTION_APP_NAME \
  --storage-account YOUR_STORAGE_ACCOUNT \
  --resource-group YOUR_RESOURCE_GROUP \
  --consumption-plan-location eastus \
  --runtime python \
  --runtime-version 3.9 \
  --functions-version 4

# Set the connection string
az functionapp config appsettings set \
  --name YOUR_FUNCTION_APP_NAME \
  --resource-group YOUR_RESOURCE_GROUP \
  --settings AZURE_STORAGE_CONNECTION_STRING="your_connection_string"

# Deploy
cd todo_api
func azure functionapp publish YOUR_FUNCTION_APP_NAME
```

**2. Deploy the Frontend:**

Build and host the React app somewhere (Static Web Apps, Blob Storage with CDN, etc.):

```bash
npm run build
# Then upload the build/ folder to your hosting service
```

Don't forget to update the API URL in `src/TodoApp.jsx` to point to your deployed backend.

## Configuration

### API Endpoint

The frontend talks to the backend via the `API_BASE_URL` constant in `src/TodoApp.jsx`:

```javascript
const API_BASE_URL = 'http://localhost:7071/api/todo';
```

Change this to your deployed Function App URL when you go to production.

### Azure Connection String

The backend needs `AZURE_STORAGE_CONNECTION_STRING` set in `todo_api/local.settings.json` locally, or in your Function App settings when deployed.

### CORS

CORS is set to allow all origins in `todo_api/host.json` for development. You should lock this down to your specific domain in production.

## Known Limitations and Assumptions

A short section in the README covering:

• Which AI tools you used and how
  - Perplexity Spaces for planning, Github Copilot for dev

    
• Challenges you encountered and how you solved them
  - Identifiend the issues in code manually and notified it to copilot, and it fixed them. Making videos of coding took way longer and made development very slow, also problems to upload those
    
• What you'd improve with more time
  - User authentication and per-user todo lists
  - Edit/update functionality
  - Better error handling and loading states
  - Pagination or infinite scroll
  - Some tests
    
• Any assumptions you made about requirements



