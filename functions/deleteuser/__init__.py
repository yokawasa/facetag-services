# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

import logging
import azure.functions as func
from commons.blockblob import AzureStorageBlockBlob
from commons.config import Config
from commons.cosmosdb import AssetDB, UserDB

def main(req: func.HttpRequest) -> func.HttpResponse:
  logging.info('Python HTTP trigger function processed a request.')

  user_id = req.params.get('user_id')
  if not user_id:
    return func.HttpResponse(
      "Please pass a user_id on the query string",
      status_code=400
     )

  logging.info(f"deleting {user_id}")
  # FIXME
  return func.HttpResponse(user_id)
