# -*- coding: utf-8 -*-
import os
import sys
import logging
from azure.storage.blob import BlockBlobService

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
