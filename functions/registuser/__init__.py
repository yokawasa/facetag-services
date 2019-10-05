# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

import logging
import azure.functions as func
from commons.blockblob import AzureStorageBlockBlob
from commons.faceapi import AzureCognitiveFaceAPI
from commons.config import Config
from commons.cosmosdb import AssetDB, UserDB

config = Config()

"""
POST /user

body:
{
  "user_id": <user_id>,     // required
  "user_name": <user_name>  // optional
}
"""
def main(req: func.HttpRequest) -> func.HttpResponse:
  logging.info('Python HTTP trigger function processed a request.')

  try:
    req_body = req.get_json()
    logging.info('req_body=%s',req_body)
  except Exception as e:
    logging.info(e)
  except ValueError as ve:
    logging.info(ve)

  user_id = req_body.get('user_id')
  user_name = req_body.get('user_name') if req_body.get('user_name') else user_id

  if not user_id:
    # return func.HttpResponse(f"Hello {name}!")
    return func.HttpResponse(
        "Please pass a name on the query string or in the request body",
        status_code=400
    )

  ## Get user and check if it's already registed
  userdb = UserDB(config)
  try:
    user = userdb.get_user(user_id)
    if user:
      logging.info(f"A user with user_id {user_id} already exists")
      return func.HttpResponse(
          f"A user with user_id {user_id} already exists",
          status_code=409
      )
  except Exception as e:
    logging.info(e)
    return func.HttpResponse(
        str(e),
        status_code=400
    )

  ## Create person_group_id
  storage_info = AzureStorageBlockBlob.parse_storage_conn_string(config.get_value('AzureWebJobsStorage'))
  faceapi = AzureCognitiveFaceAPI(
        config.get_value('FACEAPI_ENDPOINT'),
        config.get_value('FACEAPI_SUBKEY'),
        storage_info['AccountName'], 
        storage_info['AccountKey'] )

  person_group_id = user_id
  person_group_name = user_name
  try:
    faceapi.create_person_group(person_group_id, person_group_name)
  except Exception as e:
    logging.info(e)
    return func.HttpResponse(
        str(e), 
        status_code=400
    )

  ## Regist user
  userdb = UserDB(config)
  try:
    userdb.add_user(user_id, person_group_id)
  except Exception as e:
    return func.HttpResponse(
        str(e),
        status_code=400
    )

  # return func.HttpResponse(f"Hello {user_id}!")
  return func.HttpResponse(user_id)
