# -*- coding: utf-8 -*-
import os, io
import sys
import blockblob

# Azure Storage Block blob
# pip install azure-storage-blob
# pip install azure-storage-common

# for test
import urllib.parse
import requests

if __name__ == "__main__":
  account_name = "facetagstore"
  account_key= "kQoygy0zzqjHe2vV4NWYP94j7VXGi1ZK2WV6ZWaJkFvZfrUifCzN9Dfm3NsO8Tf7r/2tTQl7b5kEBqBzEjqxPQ=="
  container_name = "test"
  blob_name = "yoichi.jpg"
  compvision_endpoint = "https://yoichikacompvision01.cognitiveservices.azure.com"
  subscription_key = "656688f321594e0b9db12a1316176a6a"

  blobclient = blockblob.AzureStorageBlockBlob(account_name,account_key)
  image_blob = blobclient.get_blob(container_name, blob_name)
  #in_stream = io.BytesIO()
  # blobclient.get_blob_stream(container_name, blob_name, in_stream )
  # in_stream.seek(0)
  # Request headers
  headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key,
  }
  # Request parameters
  params = urllib.parse.urlencode({
        # All of them are optional
        #'visualFeatures': 'Tags',
        'visualFeatures': 'Description',
        'language': 'en',
  })

  tagsets = []
  try:
    api_url = "{}/vision/v2.0/analyze?{}".format(compvision_endpoint, params)
    print("API URL:{}".format(api_url))
    r = requests.post(api_url,
                    headers=headers,
                    data=image_blob.content)
    raw_parsed = r.json()
    print(raw_parsed)

    #tags = [d.get('name') for d in tagsets]
    ## [Data Structure]
    ## raw_parsed['tags'] = [
    ##  {"name": "tagname1", "confidence":0.9999},
    ##  {"name": "tagname2", "confidence":0.9999},
    ##  ...]
    #tagsets = raw_parsed['tags']
    
    tagsets = raw_parsed['description']['tags']
  except Exception as e:
    sys.stderr.write("Error:{}".format(e))

  #sys.stdout.write(tagsets)
  print(tagsets)

  # URL: parase_url
  testurl = "https://facetagstore.blob.core.windows.net/test/yoichi.jpg"
  print(blockblob.AzureStorageBlockBlob.parase_url(testurl))
