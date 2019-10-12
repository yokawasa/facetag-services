# -*- coding: utf-8 -*-
import logging
import azure.functions as func
from __app__.commons.blockblob import AzureStorageBlockBlob
from __app__.commons.config import Config
from __app__.commons.cosmosdb import AssetDB, PhotoDB

config = Config()

"""
DELETE /api/deleteasset?user_id={user_id}&asset_id={asset_id}
"""
def main(req: func.HttpRequest) -> func.HttpResponse:
  logging.info('deleteasset function processed a request.')

  user_id = req.params.get('user_id')
  asset_id = req.params.get('asset_id')
  if not user_id or not asset_id:
    return func.HttpResponse(
      "Please pass both user_id and asset_id on the query string",
      status_code=400
    )
  logging.info(f"deleting asset: {asset_id} for user: {user_id}")
  # 1. Delete Asset from AssetDB
  assetdb = AssetDB(config)
  try:
    assetdb.delete_asset(asset_id)
  except Exception as e:
    return func.HttpResponse(
      str(e),
      status_code=400
    )

  # 2. Delete Photos stored in the asset from PhotoDB
  photodb = PhotoDB(config)
  try:
    photodb.delete_photos_in_asset(user_id, asset_id)
  except Exception as e:
    return func.HttpResponse(
        str(e),
        status_code=400
    )
    
  # 3. Delete the container for the asset
  storage_info = AzureStorageBlockBlob.parse_storage_conn_string(config.get_value('AzureWebJobsStorage'))
  blobclient = AzureStorageBlockBlob(storage_info['AccountName'], storage_info['AccountKey'])
  try:
    blobclient.delete_container(asset_id)
  except Exception as e:
    return func.HttpResponse(
        str(e),
        status_code=400
    )

  deleted_asset ={
      "user_id": user_id,
      "asset_id": asset_id
  }
  return func.HttpResponse(json.dumps(deleted_asset)
