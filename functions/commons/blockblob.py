# -*- coding: utf-8 -*-
import os
import sys
import base64
import hmac
import hashlib
import urllib.parse
from datetime import datetime, timedelta
import logging
from azure.storage.blob import BlockBlobService

_AZURE_STORAGE_API_VERSION = "2018-03-28"

# Azure Storage Block blob
# pip install azure-storage-blob
# pip install azure-storage-common

# azure.storage.blob.baseblobservice SDK ref
# https://azure-storage.readthedocs.io/_modules/azure/storage/blob/baseblobservice.html
class AzureStorageBlockBlob(object):

  def __init__(self, account_name, account_key ):
    self._client = BlockBlobService(account_name=account_name,
                                    account_key=account_key)

  @staticmethod
  def parse_url(url):
    blob_name = url.rsplit('/',1)[-1]
    container_name = url.rsplit('/',2)[-2]
    return container_name, blob_name

  @staticmethod
  def parse_storage_conn_string(conn_str):
    h ={}
    for x in conn_str.split(';'):
      i = x.find('=')
      k = x[:i]
      h[k] = x[i+1:]
    return h

  @staticmethod
  def generate_sas_token (storage_account, storage_key, permission, token_ttl, container_name, blob_name = None ):
    sp = permission
    # Set start time to five minutes ago to avoid clock skew.
    st= str((datetime.utcnow() - timedelta(minutes=5) ).strftime("%Y-%m-%dT%H:%M:%SZ"))
    se= str((datetime.utcnow() + timedelta(hours=token_ttl)).strftime("%Y-%m-%dT%H:%M:%SZ"))
    srt = 'o' if blob_name else 'co'

    # Construct input value
    inputvalue = "{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}\n{8}\n".format(
      storage_account,  # 0. account name
      sp,                   # 1. signed permission (sp)
      'b',                  # 2. signed service (ss)
      srt,                  # 3. signed resource type (srt)
      st,                   # 4. signed start time (st)
      se,                   # 5. signed expire time (se)
      '',                   # 6. signed ip
      'https',              # 7. signed protocol
      _AZURE_STORAGE_API_VERSION)  # 8. signed version

    # Create base64 encoded signature
    hash =hmac.new(
          base64.b64decode(storage_key),
          inputvalue.encode(encoding='utf-8'),
          hashlib.sha256
      ).digest()

    sig = base64.b64encode(hash)

    querystring = {
      'sv':  _AZURE_STORAGE_API_VERSION,
      'ss':  'b',
      'srt': srt,
      'sp': sp,
      'se': se,
      'st': st,
      'spr': 'https',
      'sig': sig,
    }
    sastoken = urllib.parse.urlencode(querystring)

    sas_url = None
    if blob_name:
      sas_url = "https://{0}.blob.core.windows.net/{1}/{2}?{3}".format(
          storage_account,
          container_name,
          blob_name,
          sastoken)
    else:
      sas_url = "https://{0}.blob.core.windows.net/{1}?{2}".format(
          storage_account,
          container_name,
          sastoken)

    return {
          'token': sastoken,
          'url' : sas_url
         }

  def create_container(self, container_name):
    return self._client.create_container(container_name)
  
  def delete_container(self, container_name):
    return self._client.delete_container(container_name)

  def get_blob(self, container_name, blob_name):
    return self._client.get_blob_to_bytes(container_name, blob_name)
  
  def get_blob_stream(self, container_name, blob_name, stream):
    # stream = io.BytesIO()
    return self._client.get_blob_to_stream(container_name, blob_name, stream=stream)

  def purge_blob(self, container_name, blob_name):
    return self._client.delete_blob(container_name, blob_name)

  def list_blob(self, container_name ):
    l = []
    generator = self._client.list_blobs(container_name)
    for blob in generator:
      # print("\t Blob name: " + blob.name)
      l.append(blob.name)
    return l
    # https://stackoverflow.com/questions/51145124/how-to-list-all-blobs-inside-of-a-specific-subdirectory-in-azure-cloud-storage-u
    # https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python#list-the-blobs-in-a-container

  # def get_purge_blob(self, container_name, blob_name):
  #  blob = self.get_blob(container_name, blob_name)
  #  if blob.content is not None:
  #    self.purge_blob(container_name, blob_name)
  #  return blob
