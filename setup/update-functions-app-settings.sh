#!/bin/bash
set -e -x

# Get Storage connection string
STORAGE_CONNECTION_STRING=$(az storage account show-connection-string \
--resource-group $RESOURCE_GROUP --name $STORAGE_ACCOUNT_NAME \
--query connectionString --output tsv)

az webapp config appsettings set \
  -n $AZFUNC_APP_NAME \
  -g $RESOURCE_GROUP \
  --settings \
AzureWebJobsStorage=$STORAGE_CONNECTION_STRING \
THUMBNAIL_CONTAINER_NAME=thumbnails \
THUMBNAIL_WIDTH=100 \
FUNCTIONS_EXTENSION_VERSION=~2 \
APPINSIGHTS_INSTRUMENTATIONKEY=$APPINSIGHTS_INSTRUMENTATIONKEY
