# -*- coding: utf-8 -*-
import logging
import azure.functions as func
from __app__.commons.blockblob import AzureStorageBlockBlob
from __app__.commons.config import Config
from __app__.commons.cosmosdb import AssetDB, UserDB

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
  # FIXME

  return func.HttpResponse(asset_id)
