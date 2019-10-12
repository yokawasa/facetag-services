# -*- coding: utf-8 -*-
import os, uuid, hashlib
import logging
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors

"""
CosmosDB
pip install azure-cosmos
"""

class AzureCosmosDB(object):

  def __init__(self,
      endpoint, primary_key, database_name, collection_name):
    self._client = cosmos_client.CosmosClient(
        url_connection=endpoint,
        auth={ 'masterKey': primary_key}
      )

    self._options = {
        'enableCrossPartitionQuery':True,
        'maxItemCount':1
    }

    self._collection_link = "/dbs/{}/colls/{}".format(
      database_name, collection_name)

  """
  def store_document(self, document):
    _newdoc = None
    try:
      _newdoc = self._client.CreateItem(self._collection_link,document)
    except Exception as e:
      logging.error("Cosmos DB store_document error:{}".format(e))
    return _newdoc
  """

  def add_document(self, document, disable_automatic_id_gen = False):
    options = self._options
    if disable_automatic_id_gen:
      options['disableAutomaticIdGeneration']=True
    try:
      return self._client.CreateItem(self._collection_link,document, options)
    except errors.HTTPFailure as e:
      if e.status_code == 404:
          logging.error('A collection with id \'{0}\' does not exist'.format(self._collection_link))
      elif e.status_code == 409:
          #logger.error('A Item with id \'{0}\' already exists'.format(document['id']))            
          logging.error('A Item with id \'{0}\' already exists'.format(document['id']))            
      else: 
          raise errors.HTTPFailure(e.status_code)
    except Exception as e:
      raise e
    return None

  def upsert_document(self, document, disable_automatic_id_gen = False):
    options = self._options
    if disable_automatic_id_gen:
      options['disableAutomaticIdGeneration']=True
    try:
      return self._client.UpsertItem(self._collection_link, document,options)
    except errors.HTTPFailure as e:
      if e.status_code == 404:
        logging.error('A collection with id \'{0}\' does not exist'.format(self._collection_link))
      else:
        raise errors.HTTPFailure(e.status_code)
    except Exception as e:
      raise e
    return None

  def delete_document(self, id):
    options = self._options
    query = {'query': 'SELECT * FROM c WHERE c.id = "{0}"'.format(id)}
    try:
        results = self.client.QueryItems(self._collection_link, query, options)
        for item in list(results):
            self.client.DeleteItem(item['_self'], options)
    except errors.HTTPFailure as e:
      if e.status_code == 404:
        logging.error('A collection with id \'{0}\' does not exist'.format(self._collection_link))
      else:
        raise errors.HTTPFailure(e.status_code)
    except Exception as e:
      raise e

  def get_document(self, query):
    options = self._options
    partition_key=None

    docs_iterable = self._client.QueryItems(self._collection_link, query, options, partition_key)
    if len(list(docs_iterable)) > 0:
      return docs_iterable.fetch_next_block()[0]
    return None

  def get_documents(self, query):
    options = {}
    options['enableCrossPartitionQuery'] = True
    options['maxItemCount'] = 1000
    partition_key="asset_id"

    docs_iterable = self._client.QueryItems(self._collection_link, query, options, partition_key)
    return list(docs_iterable)


"""
Asset data object
- id  (primary) = asset id
- asset_name  = asset name
- user_id
"""
class AssetDB(AzureCosmosDB):
  def __init__(self, config):
    endpoint = config.get_value('COSMOSDB_ENDPOINT')
    primary_key = config.get_value('COSMOSDB_KEY')
    database_name = config.get_value('COSMOSDB_DATABASE_NAME')
    collection_name = config.get_value('COSMOSDB_ASSET_COLLECTION_NAME')
    super(AssetDB, self).__init__(endpoint, primary_key, database_name, collection_name)

  @staticmethod
  def gen_random_id():
    return str(uuid.uuid4())

  def get_user_id(self, asset_id):
    query = {'query': "SELECT * FROM s WHERE s.id='{}'".format(asset_id)}
    try:
      doc = self.get_document(query)
      if doc:
        return doc['user_id']
    except Exception as e:
      logging.error("AssetDB get_user_id error ( asset_id {} ): {} ".format(asset_id, e))
    return None

  def get_assets(self, user_id):
    query = {'query': "SELECT s.id as asset_id, s.asset_name, s.user_id FROM s WHERE s.user_id='{}'".format(user_id)}
    try:
      return self.get_documents(query)
    except Exception as e:
      logging.error("AssetDB get_assets error ( user_id {} ): {} ".format(user_id, e))
    return None

  def add_asset(self, asset_id, asset_name, user_id):
    doc = {
      "id" : asset_id,
      "asset_name" : asset_name,
      "user_id": user_id
    }
    return self.upsert_document(doc)

  def delete_asset(self, asset_id):
    try :
        self.delete_document(asset_id)
    except Exception as e:
      logging.error("AssetDB delete asset error ( asset_id {} ): {} ".format(asset_id, str(e)))
    return None


"""
User data object
- id  (primary) = user_id
- user_name
- person_group_id
- asset_id_for_train
- persons
  [
    { "person_id": "wxxx", "person_name": "wxxx", "asset_id_for_train": "xxxx" },
    { "person_id": "yyyy", "person_name": "wyyy", "asset_id_for_train": "yyyy" },
    { "person_id": "zzzz", "person_name": "wzzz", "asset_id_for_train": "zzzz" },
  ]
"""
class UserDB(AzureCosmosDB):
  def __init__(self, config):
    endpoint = config.get_value('COSMOSDB_ENDPOINT')
    primary_key = config.get_value('COSMOSDB_KEY')
    database_name = config.get_value('COSMOSDB_DATABASE_NAME')
    collection_name = config.get_value('COSMOSDB_USER_COLLECTION_NAME')
    super(UserDB, self).__init__(endpoint, primary_key, database_name, collection_name)

  def get_user(self, user_id):
    query = {'query': "SELECT * FROM s WHERE s.id='{}'".format(user_id)}
    try:
      return self.get_document(query)
    except Exception as e:
      logging.error("userDB get_user_id error ( user_id {} ): {} ".format(user_id, e))
    return None

  def add_user(self, user_id, user_name, person_group_id, persons=[]):
    doc = {
      "id" : user_id,
      "user_name" : user_name,
      "person_group_id": person_group_id,
      "persons": persons
    }
    return self.upsert_document(doc)    

"""
Photo data object
- id  (primary) = photo_id
- asset_id
- blob_name
- user_id
- persons
  [
    { "person_id": "wxxx" },
    { "person_id": "yyyy" },
    { "person_id": "zzzz" },
  ],
"""
class PhotoDB(AzureCosmosDB):
  def __init__(self, config):
    endpoint = config.get_value('COSMOSDB_ENDPOINT')
    primary_key = config.get_value('COSMOSDB_KEY')
    database_name = config.get_value('COSMOSDB_DATABASE_NAME')
    collection_name = config.get_value('COSMOSDB_PHOTO_COLLECTION_NAME')
    super(PhotoDB, self).__init__(endpoint, primary_key, database_name, collection_name)

  @staticmethod
  def gen_id(asset_id, blob_name):
    s = "{}/{}".format(asset_id.lower(), blob_name.lower())
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

  def add_photo(self, asset_id, blob_name, user_id, persons):
    photo_id = PhotoDB.gen_id(asset_id, blob_name)
    doc = {
      "id" : photo_id,
      "asset_id": asset_id,
      "blob_name": blob_name,
      "user_id": user_id,
      "persons": persons
    }
    return self.upsert_document(doc)

  def get_photos_of_person(self, user_id, person_id, order_desc = True, offset=0, limit=100 ):
    order_s = 'DESC' if order_desc else 'ASC'
    # query = {"query": "SELECT * FROM c WHERE c.user_id=\"{0}\" and ARRAY_CONTAINS(c.persons, {{ \"person_id\" : \"{1}\" }}, true) ORDER BY c._ts {2} OFFSET {3} LIMIT {4}".format( user_id, person_id, order_s, offset, limit) }
    query = {"query": "SELECT c.id as photo_id, c.asset_id, c.blob_name, c.user_id, c.persons, c._ts as last_updated FROM c WHERE c.user_id=\"{0}\" and ARRAY_CONTAINS(c.persons, {{ \"person_id\" : \"{1}\" }}, true) ORDER BY c._ts {2} OFFSET {3} LIMIT {4}".format( user_id, person_id, order_s, offset, limit) }
    # print("query={}".format(query))
    try:
      return self.get_documents(query)
    except Exception as e:
      logging.error("PhotoDB get photos of person error ( user_id {} person_id {} query {} ): {} ".format(user_id, person_id, query, str(e)))
    return None

  def get_photos_in_asset(self, user_id, asset_id, order_desc = True, offset=0, limit=100 ):
    order_s = 'DESC' if order_desc else 'ASC'
    query = {"query": "SELECT c.id as photo_id, c.asset_id, c.blob_name, c.user_id, c.persons, c._ts as last_updated FROM c WHERE c.user_id=\"{0}\" and c.asset_id=\"{1}\" ORDER BY c._ts {2} OFFSET {3} LIMIT {4}".format( user_id, asset_id, order_s, offset, limit) }
    # print("query={}".format(query))
    try:
      return self.get_documents(query)
    except Exception as e:
      logging.error("PhohtoDB get photos in asset error ( user_id {} asset_id {} query {} ): {} ".format(user_id, asset_id, query, str(e)))
    return None

  def delete_photos_in_asset(self, user_id, asset_id):
    try :
      docs = self.get_photos_in_asset(user_id, asset_id)
      for doc in list(docs):
        logging.info("PhotoDB deleting photo (user_id {} asset_id {} photo_id {} )".format(user_id, asset_id, doc['id']) )
        self.delete_document(doc['id'])
    except Exception as e:
      logging.error("PhotoDB delete photos in asset error ( user_id {} asset_id {} ): {} ".format(user_id, asset_id, str(e)))
    return None
