# -*- coding: utf-8 -*-
import json
import logging
import azure.functions as func
from __app__.commons.config import Config
from __app__.commons.cosmosdb import PhotoDB
from __app__.commons.blockblob import AzureStorageBlockBlob

config=Config()

"""
req method: POST
body:
{
  "user_id": <user_id>,      // required
  "person_id": <person_id>,  // optional
  "asset_id": <asset_id>,   // optional
  "order": <order: ASC|DESC> // optional (default: DESC)
  "offset": <offset num>     // optional (default: 0)
  "limit": <limit num>       // optional (default: 100)
}
"""
def main(req: func.HttpRequest) -> func.HttpResponse:

  try:
    req_body = req.get_json()
    logging.info('req_body=%s',req_body)
  except Exception as e:
    logging.info(e)
  except ValueError as ve:
    logging.info(ve)

  user_id = req_body.get('user_id')
  person_id = req_body.get('person_id')
  asset_id = req_body.get('asset_id')
  order = req_body.get('order')
  offset = req_body.get('offset')
  limit = req_body.get('limit')

  if not user_id:
    return func.HttpResponse(
        "Please pass user_id in the request body",
        status_code=400
    )

  order_desc = True if order.lower == 'desc' else False
  offset = int(offset) if offset and int(offset) >= 0  else 0
  limit = int(limit) if limit and int(limit) >= 0  else 100

  storage_info = AzureStorageBlockBlob.parse_storage_conn_string(config.get_value('AzureWebJobsStorage'))
  photodb = PhotoDB(config)
  try:
    docs = photodb.get_photos( 
          user_id=user_id,
          person_id=person_id,
          asset_id=asset_id,
          order_desc = order_desc,
          offset=offset,
          limit=limit)
    ret_doc = []
    for doc in list(docs):
      token_dict = AzureStorageBlockBlob.generate_sas_token(
                    storage_info['AccountName'],
                    storage_info['AccountKey'],
                    "rl", 
                    1, 
                    doc['asset_id'], 
                    doc['blob_name'])
      doc['blob_url']=token_dict['url']
      ret_doc.append(doc)
    return func.HttpResponse(json.dumps(docs))
  except Exception as e:
    return func.HttpResponse(
        str(e),
        status_code=400
    )
