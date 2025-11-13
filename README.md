# Serverless Todo Application

A full-stack serverless todo application built with React frontend and Azure Functions Python backend, using Azure Table Storage for data persistence.

## Architecture

- **Frontend**: React 19.2.0 with responsive UI
- **Backend**: Python Azure Functions (serverless API)
- **Storage**: Azure Table Storage for persistent data
- **Infrastructure**: Azure (IaC with Bicep/Terraform - coming soon)

## Features

✅ Add and remove todo items  
✅ Display list of existing todos  
✅ Persistent storage with Azure Table Storage  
✅ RESTful API with error handling  
✅ Responsive design  
✅ CORS enabled for local development  

## Project Structure

```
Ele_v1/
├── src/                      # React frontend
│   ├── TodoApp.jsx          # Main todo component
│   ├── TodoApp.css          # Component styles
│   ├── App.js               # Root component
│   └── App.css              # App styles
├── todo_api/                # Azure Functions backend
│   ├── function_app.py      # API endpoints
│   ├── requirements.txt     # Python dependencies
│   ├── host.json            # Function host config
│   ├── local.settings.json.example  # Config template
│   └── README.md            # Backend documentation
└── README.md                # This file
```

## Prerequisites

- Node.js 14+ and npm
- Python 3.9+
- Azure Functions Core Tools v4+
- Azure CLI (for deployment)
- Azure Storage Account

## Local Development Setup

### 1. Clone and Install Dependencies

```bash
# Install frontend dependencies
npm install

# Install backend dependencies
cd todo_api
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Azure Storage

Create a storage account and get the connection string:

```bash
# Login to Azure
az login

# Get your storage account connection string
az storage account show-connection-string \
  --name YOUR_STORAGE_ACCOUNT \
  --resource-group YOUR_RESOURCE_GROUP \
  --output tsv
```

Copy `local.settings.json.example` to `local.settings.json` and add your connection string:

```bash
cd todo_api
cp local.settings.json.example local.settings.json
# Edit local.settings.json and add your AZURE_STORAGE_CONNECTION_STRING
```

See [todo_api/AZURE_STORAGE_SETUP.md](todo_api/AZURE_STORAGE_SETUP.md) for detailed storage setup instructions.

### 3. Run the Application

**Terminal 1 - Backend:**
```bash
cd todo_api
func start
```

Backend will run on http://localhost:7071

**Terminal 2 - Frontend:**
```bash
npm start
```

Frontend will run on http://localhost:3000

## API Endpoints

- `GET /api/hello` - Test endpoint
- `GET /api/health` - Health check
- `GET /api/todo` - Get all todos
- `POST /api/todo` - Create a new todo (requires `{ "title": "..." }`)
- `DELETE /api/todo/{partitionKey}/{rowKey}` - Delete a todo

## Testing

Test the backend API:

```bash
cd todo_api
./test_azure_storage.sh
```

## Data Schema

Todos are stored in Azure Table Storage with the following structure:

```json
{
  "partitionKey": "default",
  "rowKey": "1731491234567",
  "id": "1731491234567",
  "title": "Buy groceries",
  "timestamp": "2025-11-13T10:00:00.000000Z"
}
```

## Deployment

> 🚧 Infrastructure as Code (Bicep/Terraform) and deployment instructions coming soon!

## What's Implemented

✅ **Backend API** - Azure Functions with GET, POST, DELETE endpoints  
✅ **Frontend UI** - React form and list display  
✅ **Data Persistence** - Azure Table Storage integration  
✅ **Error Handling** - 400, 404, 500 responses  
⏳ **Infrastructure as Code** - Coming next  
⏳ **Frontend-Backend Integration** - Coming next  

## Next Steps

1. Connect React frontend to backend API
2. Create Bicep/Terraform files for infrastructure
3. Add Azure deployment configuration
4. Deploy to Azure

## Learn More

- [Azure Functions Python](https://learn.microsoft.com/azure/azure-functions/functions-reference-python)
- [Azure Table Storage](https://learn.microsoft.com/azure/storage/tables/table-storage-overview)
- [Create React App](https://facebook.github.io/create-react-app/docs/getting-started)
- [React Documentation](https://reactjs.org/)


### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
