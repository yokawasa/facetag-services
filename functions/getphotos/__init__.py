# -*- coding: utf-8 -*-
import json
import sys
sys.path.append('../')

import logging
import azure.functions as func
from commons.config import Config
from commons.cosmosdb import PhotoDB

config=Config()

"""
req method: POST
body:
{
  "user_id": <user_id>,      // required
  "person_id": <person_id>,  // required
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
  order = req_body.get('order')
  offset = req_body.get('offset')
  limit = req_body.get('limit')
  if not user_id or not person_id:
    return func.HttpResponse(
        "Please pass both user_id and person_id on the query string or in the request body",
        status_code=400
    )

  order_desc = True if order.lower == 'desc' else False
  offset = int(offset) if offset and int(offset) > 0  else 100
  limit = int(limit) if limit and int(limit) >= 0  else 0

  photodb = PhotoDB(config)
  try:
    docs = photodb.get_photos_of_person(user_id, person_id, order_desc = order_desc, offset=offset, limit=limit )
    return func.HttpResponse(json.dumps(docs))
  except Exception as e:
    return func.HttpResponse(
        str(e),
        status_code=400
    )
