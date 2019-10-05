# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

import logging
import azure.functions as func
from commons.blockblob import AzureStorageBlockBlob
from commons.config import Config
from commons.cosmosdb import AssetDB, UserDB

config = Config()

"""
POST /api/createasset?user_id={user_id}
body:
{
  "asset_name": <asset_name>
}
"""
def main(req: func.HttpRequest) -> func.HttpResponse:
  logging.info('Python HTTP trigger function processed a request.')

  user_id = req.params.get('user_id')

  try:
    req_body = req.get_json()
    logging.info('req_body=%s',req_body)
  except Exception as e:
    logging.info(e)
  except ValueError as ve:
    logging.info(ve)

  asset_name = req_body.get('asset_name')

  if not user_id or not asset_name:
    return func.HttpResponse(
        "Please pass user_id on the query string or asset_name in the request body",
        status_code=400
    )

  ## Get User Info and check if user_id exists
  userdb = UserDB(config)
  try:
    user = userdb.get_user(user_id)
    if not user:
      logging.info(f"A user with user_id {user_id} not exists")
      return func.HttpResponse(
          f"A user with user_id {user_id} not exists",
          status_code=409
      )
  except Exception as e:
    logging.info(e)
    return func.HttpResponse(
        str(e),
        status_code=400
    )

  ## Create an asset for train for the person
  storage_info = AzureStorageBlockBlob.parse_storage_conn_string(config.get_value('AzureWebJobsStorage'))
  asset_id = AssetDB.gen_random_id()
  blobclient = AzureStorageBlockBlob(storage_info['AccountName'], storage_info['AccountKey'])
  try:
    blobclient.create_container(asset_id)
  except Exception as e:
    return func.HttpResponse(
        str(e),
        status_code=400
    )

  assetdb = AssetDB(config)
  try:
    assetdb.add_asset(asset_id, asset_name, user_id)
  except Exception as e:
    return func.HttpResponse(
        str(e),
        status_code=400
    )

  return func.HttpResponse(asset_id)
