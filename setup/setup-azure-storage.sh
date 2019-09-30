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

# Get Storage Key
ACCESS_KEY=$(az storage account keys list --account-name $STORAGE_ACCOUNT_NAME --resource-group $RESOURCE_GROUP --output tsv |head -1 | awk '{print $3}')

echo "Creating a container: Images"
az storage container create  \
    --name "images" \
    --account-name $STORAGE_ACCOUNT_NAME \
    --account-key $ACCESS_KEY \
    --public-access off

echo "Creating a container: thumbnails"
# Make this public accessible
az storage container create  \
    --name "thumbnails" \
    --account-name $STORAGE_ACCOUNT_NAME \
    --account-key $ACCESS_KEY \
    --public-access container
