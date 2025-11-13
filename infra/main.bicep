// Main Bicep template for Todo Application
// Deploys: Storage Account and Table Storage only

@description('Name of the storage account')
param storageAccountName string = 'todoapp${uniqueString(resourceGroup().id)}'

@description('Azure region for resources')
param location string = resourceGroup().location

@description('Storage account SKU')
@allowed([
  'Standard_LRS'
  'Standard_GRS'
  'Standard_ZRS'
])
param storageSku string = 'Standard_LRS'

@description('Name of the table for todos')
param tableName string = 'todos'

// Storage Account
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: take(storageAccountName, 24)
  location: location
  sku: {
    name: storageSku
  }
  kind: 'StorageV2'
  properties: {
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
  }
}

// Table Service
resource tableService 'Microsoft.Storage/storageAccounts/tableServices@2023-01-01' = {
  parent: storageAccount
  name: 'default'
}

// Todos Table
resource todosTable 'Microsoft.Storage/storageAccounts/tableServices/tables@2023-01-01' = {
  parent: tableService
  name: tableName
}

// Outputs
output storageAccountName string = storageAccount.name
output tableName string = tableName
output tableEndpoint string = storageAccount.properties.primaryEndpoints.table
output resourceGroupName string = resourceGroup().name
