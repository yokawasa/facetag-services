# -*- coding: utf-8 -*-
import os
import json
import sys
sys.path.append('../')
from commons.cosmosdb import AssetDB, UserDB, PhotoDB
from commons.config import Config

config = Config()

if __name__ == "__main__":

  argvs = sys.argv 
  argc = len(argvs)
  if (argc != 2): 
    print('Usage: # python %s <local.settings.json>' % argvs[0])
    quit() 
  print('The content of %s ...\n' % argvs[1])
  local_settings_json= argvs[1]
  with open(local_settings_json) as json_file:
    data = json.load(json_file)
    os.environ['COSMOSDB_ENDPOINT'] = data['Values']['COSMOSDB_ENDPOINT']
    os.environ['COSMOSDB_KEY'] = data['Values']['COSMOSDB_KEY']
    os.environ['COSMOSDB_DATABASE_NAME'] = data['Values']['COSMOSDB_DATABASE_NAME']
    os.environ['COSMOSDB_ASSET_COLLECTION_NAME'] = data['Values']['COSMOSDB_ASSET_COLLECTION_NAME']
    os.environ['COSMOSDB_USER_COLLECTION_NAME'] = data['Values']['COSMOSDB_USER_COLLECTION_NAME']
    os.environ['COSMOSDB_PHOTO_COLLECTION_NAME'] = data['Values']['COSMOSDB_PHOTO_COLLECTION_NAME']

  container_name= "imageslocal"
  asset_id = container_name
  blob_name = "test-image-person-group.jpg"
  ### AssetDB test
  assetdb = AssetDB(config)
  user_id = assetdb.get_user_id(container_name)
  print('user_id: {}'.format(user_id)) 

  ### UserDB test
  userdb = UserDB(config)
  user = userdb.get_user(user_id)
  group_id = user['person_group_id']
  person_ids =[]
  for p in user['persons']:
    person_ids.append(p['person_id'])
  print("group_id: {} person_ids: {}".format(group_id, ','.join(person_ids))) 

  ### PhotoDB test
  photodb = PhotoDB(config)
  photo_id = PhotoDB.gen_id(asset_id, blob_name)
  print("photo_id = {}".format(photo_id))
  persons = []
  persons.append({"person_id": "xxxxxxxxxxxxxxxx"})
  persons.append({"person_id": "yyyyyyyyyyyyyyyyy"})
  print(photodb.add_photo(asset_id, blob_name, user_id, persons))

  user_id = 'yoichika4'
  person_id='a654f4c2-dc7d-43dc-a95a-8819da69587a'
  print("offset 1 limit 1")
  docs = photodb.get_photos_of_person(user_id, person_id, order_desc = True, offset=1, limit=1 )
  for doc in docs:
    print(doc)
  print("offset 2 limit 2")
  docs = photodb.get_photos_of_person(user_id, person_id, order_desc = True, offset=2, limit=2 )
  for doc in docs:
    print(doc)
