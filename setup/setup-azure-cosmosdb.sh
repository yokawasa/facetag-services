#!/bin/sh

LEAVES_COLLECTION_NAME="leaves"   # FIXED

echo "Create CosmosDB Account"
az cosmosdb create \
    --name $COSMOSDB_ACCOUNT_NAME \
    --kind GlobalDocumentDB \
    --resource-group $RESOURCE_GROUP

echo "Get Key"
az cosmosdb list-keys --name $COSMOSDB_ACCOUNT_NAME --resource-group $RESOURCE_GROUP

echo "Create Database"
az cosmosdb database create \
    --name $COSMOSDB_ACCOUNT_NAME \
    --db-name $COSMOSDB_DATABASE_NAME \
    --resource-group $RESOURCE_GROUP

echo "Create Container"
# Create a container with a partition key and provision 400 RU/s throughput.
az cosmosdb collection create \
    --resource-group $RESOURCE_GROUP \
    --collection-name $COSMOSDB_ASSET_COLLECTION_NAME \
    --name $COSMOSDB_ACCOUNT_NAME \
    --db-name $COSMOSDB_DATABASE_NAME \
    --partition-key-path /asset_id \
    --throughput 400

# Create a container with a partition key and provision 400 RU/s throughput.
az cosmosdb collection create \
    --resource-group $RESOURCE_GROUP \
    --collection-name $COSMOSDB_USER_COLLECTION_NAME \
    --name $COSMOSDB_ACCOUNT_NAME \
    --db-name $COSMOSDB_DATABASE_NAME \
    --partition-key-path /asset_id \
    --throughput 400

# Create a container with a partition key and provision 400 RU/s throughput.
az cosmosdb collection create \
    --resource-group $RESOURCE_GROUP \
    --collection-name $COSMOSDB_PHOTO_COLLECTION_NAME \
    --name $COSMOSDB_ACCOUNT_NAME \
    --db-name $COSMOSDB_DATABASE_NAME \
    --partition-key-path /asset_id \
    --throughput 400

# 'leaves' need to be a single collection partition    
# Please see https://github.com/Azure/azure-functions-core-tools/issues/930
#az cosmosdb collection create \
#    --resource-group $RESOURCE_GROUP \
#    --collection-name $LEAVES_COLLECTION_NAME \
#    --name $COSMOSDB_ACCOUNT_NAME \
#    --db-name $COSMOSDB_DATABASE_NAME \
#    --throughput 400
