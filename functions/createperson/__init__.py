# -*- coding: utf-8 -*-
import logging
import azure.functions as func
from __app__.commons.blockblob import AzureStorageBlockBlob
from __app__.commons.faceapi import AzureCognitiveFaceAPI
from __app__.commons.config import Config
from __app__.commons.cosmosdb import AssetDB, UserDB

config = Config()

"""
POST /api/createperson?user_id={user_id}
body:
{
  "person_name": <person_name>  // required
}
"""
def main(req: func.HttpRequest) -> func.HttpResponse:
  logging.info('createperson function processed a request.')

  user_id = req.params.get('user_id')

  try:
    req_body = req.get_json()
    logging.info('req_body=%s',req_body)
  except Exception as e:
    logging.info(e)
  except ValueError as ve:
    logging.info(ve)

  person_name = req_body.get('person_name')

  if not user_id or not person_name:
    return func.HttpResponse(
        "Please pass both user_id and person_name on the query string or in the request body",
        status_code=400
    )

  ## Get User Info
  userdb = UserDB(config)
  user = None
  try:
    user = userdb.get_user(user_id)
    if not user:
      logging.info(f"A user with user_id {user_id} not exists")
      return func.HttpResponse(
          f"A user with user_id {user_id} not exists",
          status_code=409
      )
    if not 'person_group_id' in user:
      return func.HttpResponse(
          f"A user with user_id {user_id} does not have person_group_id",
          status_code=409
      )
  except Exception as e:
    logging.info(e)
    return func.HttpResponse(
        str(e),
        status_code=400
    )

  ## Create person
  storage_info = AzureStorageBlockBlob.parse_storage_conn_string(config.get_value('AzureWebJobsStorage'))
  faceapi = AzureCognitiveFaceAPI(
        config.get_value('FACEAPI_ENDPOINT'),
        config.get_value('FACEAPI_SUBKEY'),
        storage_info['AccountName'], 
        storage_info['AccountKey'] )

  created_person_id = None
  try:
    created_person = faceapi.create_person(user['person_group_id'], person_name)
    created_person_id = created_person.person_id
  except Exception as e:
    logging.info(e)
    return func.HttpResponse(
        str(e), 
        status_code=400
    )

  ## Create an asset for train for the person
  asset_id = AssetDB.gen_random_id()
  blobclient = AzureStorageBlockBlob(storage_info['AccountName'], storage_info['AccountKey'])
  try:
    blobclient.create_container(asset_id)
  except Exception as e:
    return func.HttpResponse(
        str(e),
        status_code=400
    )

  ## Update user
  try:
    persons = user['persons'] if user['persons'] else []
    logging.info("persons=%s", persons)
    persons.append(
      {
        "person_id": created_person_id,
        "person_name": person_name,
        "asset_id_for_train": asset_id
      })
    user['persons'] = persons
    userdb.upsert_document(document=user)
  except Exception as e:
    return func.HttpResponse(
        str(e),
        status_code=400
    )

  # return func.HttpResponse("OK")
  return func.HttpResponse(created_person_id)
