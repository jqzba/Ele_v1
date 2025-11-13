// Parameters file for development environment
using './main.bicep'

param storageAccountName = 'todoappdevstg'
param appName = 'todoapp-api-dev'
param storageSku = 'Standard_LRS'
param appServicePlanSku = 'B1'
param pythonVersion = '3.11'
