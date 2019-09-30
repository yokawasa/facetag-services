#!/bin/bash
set -e -x

az functionapp create \
  --resource-group $RESOURCE_GROUP \
  --name $AZFUNC_APP_NAME \
  --storage-account $STORAGE_ACCOUNT_NAME \
  --consumption-plan-location $REGION \
  --os-type Linux \
  --runtime python
