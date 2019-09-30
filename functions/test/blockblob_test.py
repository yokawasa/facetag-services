# -*- coding: utf-8 -*-
import os, io
import sys
sys.path.append('../')
from commons.config import Config
from commons.blockblob import AzureStorageBlockBlob

config = Config()

# Azure Storage Block blob
# pip install azure-storage-blob
# pip install azure-storage-common

if __name__ == "__main__":

  storage_info = AzureStorageBlockBlob.parse_storage_conn_string(config.get_value('AzureWebJobsStorage'))
  blobclient = AzureStorageBlockBlob(storage_info['AccountName'], storage_info['AccountKey'])

  asset_id_for_train =  "imageslocal"

  photo_files = []
  try:
    photo_files = blobclient.list_blob(asset_id_for_train)
    for photo_file in photo_files:
      print(photo_file)
  except Exception as e:
    print(str(e))
    quit()
