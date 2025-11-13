// Parameters file for production environment
using './main.bicep'

param storageAccountName = 'todoappprodstg'
param appName = 'todoapp-api-prod'
param storageSku = 'Standard_GRS'
param appServicePlanSku = 'B2'
param pythonVersion = '3.11'
