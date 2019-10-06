# -*- coding: utf-8 -*-
import json
import logging
import azure.functions as func
from __app__.commons.blockblob import AzureStorageBlockBlob
from __app__.commons.faceapi import AzureCognitiveFaceAPI
from __app__.commons.config import Config
from __app__.commons.cosmosdb import AssetDB, UserDB

"""
- Get userinfo from CosmosDB using user_id
- Glob upload images
- Create usergroup if not exists
- Create persion if not exists
- Add faces to persion
- Train the user group
- Update status in CosmosDB
"""
config = Config()

def main(msg: func.QueueMessage) -> None:
  received_message = msg.get_body().decode('utf-8')
  o = json.loads(received_message)
  if not 'user_id' in o or not 'person_id' in o:
    logging.error("Invalid message: message needs to contain both user_id and person_id")
    return
  user_id = o['user_id']
  person_id = o['person_id']
  logging.info("train user_id=%s person_id=%s", user_id, person_id) 

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
  except Exception as e:
    logging.info(e)
    return func.HttpResponse(
        str(e),
        status_code=400
    )
  person_group_id = user['person_group_id']

  ## Get asset_id for person_id
  asset_id_for_train = None
  persons = user['persons']
  for person in persons:
    if person_id == person['person_id']:
      asset_id_for_train = person['asset_id_for_train']
      break
  if not asset_id_for_train:
    logging.error("Invalid user info: persons in user info do not contain asset_id_for_train for person_id {} of user_id {}".format(person_id, user_id))
    return

  ## Glob blobs and add faces to person_id
  storage_info = AzureStorageBlockBlob.parse_storage_conn_string(config.get_value('AzureWebJobsStorage'))
  blobclient = AzureStorageBlockBlob(storage_info['AccountName'], storage_info['AccountKey'])
  photo_files = []
  try:
    photo_files = blobclient.list_blob(asset_id_for_train)
  except Exception as e:
    logging.error("Error: user_id {} person_id {}: {}".format( user_id, person_id, str(e)))
    return

  faceapi = AzureCognitiveFaceAPI(
        config.get_value('FACEAPI_ENDPOINT'),
        config.get_value('FACEAPI_SUBKEY'),
        storage_info['AccountName'], 
        storage_info['AccountKey'])
  for photo_file in photo_files:
    try:
      faceapi.add_face_blob(person_group_id, person_id, asset_id_for_train, photo_file)
    except Exception as e:
      logging.error("Error: user_id {} person_id {} asset_id {} photo_file {}: {}".format(user_id, person_id, asset_id_for_train, photo_file, str(e)))
      return

  ## Train PersonGroup
  try:
    faceapi.train_person_group(person_group_id)
  except Exception as e:
    logging.error("Error: user_id {} person_id {} asset_id {}: {}".format(user_id, person_id, asset_id_for_train, str(e)))
    return

  logging.info("Train succeeded!: user_id {} person_id {} asset_id {}".format(user_id, person_id, asset_id_for_train))
