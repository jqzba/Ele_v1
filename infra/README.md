# Infrastructure as Code

This directory contains Bicep templates for deploying the Todo application infrastructure to Azure.

## Resources Deployed

- **Storage Account** - Azure Table Storage for todos data
- **Function App** - Serverless API backend (Python 3.11)
- **App Service Plan** - Basic tier hosting for Function App
- **Application Insights** - Monitoring and logging

## Files

- `main.bicep` - Main Bicep template
- `main.parameters.json` - Example parameters file (JSON format)
- `main.dev.bicepparam` - Development environment parameters (Bicep format)
- `main.prod.bicepparam` - Production environment parameters (Bicep format)

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `storageAccountName` | string | `todoapp{uniqueString}` | Name of the storage account |
| `appName` | string | `todoapp-api-{uniqueString}` | Name of the Function App |
| `location` | string | Resource group location | Azure region for resources |
| `storageSku` | string | `Standard_LRS` | Storage redundancy (Standard_LRS/Standard_GRS/Standard_ZRS) |
| `appServicePlanSku` | string | `B1` | App Service Plan tier (B1/B2/B3/S1/S2/S3) |
| `pythonVersion` | string | `3.11` | Python version (3.9/3.10/3.11) |

## Deployment

### Prerequisites

- Azure CLI installed and logged in
- Bicep CLI (included with Azure CLI 2.20.0+)

### Deploy to Azure

1. **Login to Azure:**
   ```bash
   az login
   ```

2. **Create Resource Group:**
   ```bash
   az group create --name rg-todoapp-dev --location eastus
   ```

3. **Deploy Infrastructure:**
   
   **Option A: Using JSON parameters file:**
   ```bash
   az deployment group create \
     --resource-group rg-todoapp-dev \
     --template-file infra/main.bicep \
     --parameters infra/main.parameters.json
   ```

   **Option B: Using Bicep parameters file (development):**
   ```bash
   az deployment group create \
     --resource-group rg-todoapp-dev \
     --template-file infra/main.bicep \
     --parameters infra/main.dev.bicepparam
   ```

   **Option C: Using Bicep parameters file (production):**
   ```bash
   az deployment group create \
     --resource-group rg-todoapp-prod \
     --template-file infra/main.bicep \
     --parameters infra/main.prod.bicepparam
   ```

   **Option D: Inline parameters:**
   ```bash
   az deployment group create \
     --resource-group rg-todoapp-dev \
     --template-file infra/main.bicep \
     --parameters \
       storageAccountName=todoappdevstg \
       appName=todoapp-api-dev \
       location=eastus \
       storageSku=Standard_LRS \
       appServicePlanSku=B1 \
       pythonVersion=3.11
   ```

4. **Get Deployment Outputs:**
   ```bash
   az deployment group show \
     --resource-group rg-todoapp-dev \
     --name main \
     --query properties.outputs
   ```

## Outputs

The deployment provides the following outputs:

| Output | Description |
|--------|-------------|
| `storageAccountName` | Storage account name |
| `functionAppName` | Function App name |
| `functionAppUrl` | API endpoint URL (https://...) |
| `appInsightsName` | Application Insights resource name |
| `appInsightsInstrumentationKey` | App Insights instrumentation key |
| `tableName` | Table name for todos (default: "todos") |

## Post-Deployment Steps

1. **Get Storage Connection String:**
   ```bash
   az storage account show-connection-string \
     --name <storageAccountName> \
     --resource-group rg-todoapp-dev \
     --output tsv
   ```

2. **Deploy Function App Code:**
   ```bash
   cd todo_api
   func azure functionapp publish <functionAppName>
   ```

3. **Update Frontend with API URL:**
   Update `src/TodoApp.jsx` with the `functionAppUrl` from outputs.

## Cost Estimation

**Development (B1 tier):**
- App Service Plan (B1): ~$13/month
- Storage Account (LRS): ~$0.02/GB/month
- Application Insights: First 5GB free, then ~$2.30/GB
- Total: ~$13-15/month (depending on usage)

**Production (B2 tier, GRS):**
- App Service Plan (B2): ~$26/month
- Storage Account (GRS): ~$0.05/GB/month  
- Application Insights: First 5GB free, then ~$2.30/GB
- Total: ~$26-30/month (depending on usage)
