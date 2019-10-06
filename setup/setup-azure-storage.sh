#!/bin/bash
set -e -x

echo "Creating an Azure Storage account: $STORAGE_ACCOUNT_NAME"
az storage account create --name $STORAGE_ACCOUNT_NAME \
  --location $REGION \
  --resource-group $RESOURCE_GROUP \
  --sku Standard_LRS \
  --kind StorageV2
# [NOTE] Make sure to configure the storage kind as `General Purpose V2` 
# as blob storage events are available in general-purpose v2 storage accounts
# See also 
# https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blob-event-quickstart

STORAGE_CONNECTION_STRING=$(az storage account show-connection-string \
--resource-group $RESOURCE_GROUP --name $STORAGE_ACCOUNT_NAME \
--query connectionString --output tsv)

echo "Creating Queue Storage: $QUEUE_NAME"
az storage queue create --name $QUEUE_NAME --connection-string $STORAGE_CONNECTION_STRING
