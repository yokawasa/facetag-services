# -*- coding: utf-8 -*-
import sys
import json
import logging
import azure.functions as func

sys.path.append('../')
from commons.blockblob import AzureStorageBlockBlob
from commons.faceapi import AzureCognitiveFaceAPI
from commons.config import Config
from commons.cosmosdb import AssetDB, UserDB, PhotoDB

config = Config()

"""
** Identify Face Function Strategy **

1. Get user_id from container_name
2. Get userinfo from CosmosDB using user_id
3. Identify faces
4. Regist face tags
"""

def main(event: func.EventGridEvent):
  result = json.dumps({
    'id': event.id,
    'data': event.get_json(),
    'topic': event.topic,
    'subject': event.subject,
    'event_type': event.event_type,
  })
  logging.info('Python EventGrid trigger processed an event: %s', result)

  # Event Validation
  if event.event_type != 'Microsoft.Storage.BlobCreated':
    logging.info('Invalid event_type: %s', event.event_type) 
    return # Skip

  # Get Blockblob url
  event_data = event.get_json()
  blob_url= event_data['url']
  logging.info('Blob url: %s', blob_url) 

  # Get Blob Container and file name
  container_name, file_name = AzureStorageBlockBlob.parse_url(blob_url)
  logging.info('Blob container=%s file=%s', container_name, file_name)

  ## 1. Get user_id from container_name: CosmosDB
  assetdb = AssetDB(config)
  user_id = assetdb.get_user_id(container_name)
  logging.info('user_id: %s', user_id) 

  ## 2. Get userinfo from CosmosDB using user_id: CosmosDB
  userdb = UserDB(config)
  user = userdb.get_user(user_id)
  group_id = user['person_group_id']
  person_ids =[]
  for p in user['persons']:
    person_ids.append(p['person_id'])
  logging.info('group_id: %s person_ids: %s', group_id, ','.join(person_ids)) 

  ## 3. Identify faces 
  storage_info = AzureStorageBlockBlob.parse_storage_conn_string(config.get_value('AzureWebJobsStorage'))
  faceapi = AzureCognitiveFaceAPI(
        config.get_value('FACEAPI_ENDPOINT'),
        config.get_value('FACEAPI_SUBKEY'),
        storage_info['AccountName'], 
        storage_info['AccountKey'] )
  ret_dict = faceapi.identify_face_blob(group_id, container_name=container_name, blob_name=file_name, max_num_of_candidates_returned=1, confidence_threshold=0.5)
  person_included = False
  identified_persons = []
  for r in ret_dict:
    logging.info("detected_person_id: %s person_face_id: %s", r['person_id'], r['face_id'])
    identified_persons.append({"person_id": r['person_id']})

  ## 4. Regist face tags: CosmosDB
  photodb = PhotoDB(config)
  photo_id = PhotoDB.gen_id(container_name, file_name)
  logging.info("photo_id = {}".format(photo_id))
  added_photo = photodb.add_photo(container_name, file_name, user_id, identified_persons)
  logging.info("added_photo: %s", added_photo)
