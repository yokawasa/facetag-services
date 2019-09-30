# -*- coding: utf-8 -*-
import glob,os,io
import sys
sys.path.append('../')

from commons.faceapi import AzureCognitiveFaceAPI
from commons.blockblob import AzureStorageBlockBlob
# import faceapi
# import blockblob

# Face API
# pip install azure-cognitiveservices-vision-face

# FaceAPI Python SDK
# https://docs.microsoft.com/en-us/azure/cognitive-services/face/quickstarts/python-sdk
# https://azure.microsoft.com/en-us/services/cognitive-services/face/
# https://github.com/Azure-Samples/cognitive-services-quickstart-code/blob/master/python/Face/FaceQuickstart.py

if __name__ == "__main__":
  account_name = "yoichikafaceapi01"
  subkey = "fc16229040f748f68849b86fb3911ee6"
  endpoint = "https://yoichikafaceapi01.cognitiveservices.azure.com"

  storage_account_name = "facetagstore"
  storage_account_key= "kQoygy0zzqjHe2vV4NWYP94j7VXGi1ZK2WV6ZWaJkFvZfrUifCzN9Dfm3NsO8Tf7r/2tTQl7b5kEBqBzEjqxPQ=="

  api = AzureCognitiveFaceAPI(endpoint, subkey, storage_account_name, storage_account_key)

  # person group id should be lowercase and alphanumeric (dash is ok)
  person_group_id = "my-unique-person-group00"

  ## Create PersonGroup
  #print('Create Person group:', person_group_id)
  #try:
  #  faceapi.create_person_group(person_group_id, person_group_id)
  #except Exception as e:
  #  # print("[Errno {0}] {1}".format(e.errno, e.strerror))
  #  print(e)

  ## Create Person  
  #person_name = "Yoichi01"
  #print('Create Person:', person_name)
  #try:
  #  person = faceapi.create_person(person_group_id, person_name)
  #  print("person: id={}".format(person.person_id))
  #except Exception as e:
  #  print(e)

  ## Add images to a person
  person1_id = "47ca6a82-f5d1-45a8-9ac2-86a61ad6de90"
  person2_id = "4caa393c-510f-4d56-9438-f7fc8eadb52c"
  # Find all jpeg images of friends in working directory

  ## 絶対パス指定、なぜかうまくいかない
  #person1_images = [file for file in glob.glob('/Users/yoichika/dev/github/facetag-services/samples/*.jpg') if file.startswith("man")] 
  ## 相対パス指定だとうまくいく
  os.chdir("/Users/yoichika/dev/github/facetag-services/samples")
  person1_images = [file for file in glob.glob('*.jpg') if file.startswith("man")] 
  # Add to a woman person
  for image in person1_images:
    print(image)
    #w = open(image, 'r+b')
    #face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, woman.person_id, w)

  ## これをblob storageから読み込むやり方
  """
  storage_account_name = "facetagstore"
  storage_account_key= "kQoygy0zzqjHe2vV4NWYP94j7VXGi1ZK2WV6ZWaJkFvZfrUifCzN9Dfm3NsO8Tf7r/2tTQl7b5kEBqBzEjqxPQ=="
  compvision_endpoint = "https://yoichikacompvision01.cognitiveservices.azure.com"
  container_name = "test"

  blobclient = blockblob.AzureStorageBlockBlob(storage_account_name,storage_account_key)

  blob_names = ["man1-person-group.jpg", "man2-person-group.jpg", "man3-person-group.jpg"]
  for blob_name in blob_names:
    ## get blob to bytes
    # image_blob1 = blobclient.get_blob(container_name, blob1_name)
    ## get blob to stream
    in_stream = io.BytesIO()
    blobclient.get_blob_stream(container_name, blob_name, in_stream)
    in_stream.seek(0)
    persisted_face = api.add_face(person_group_id, person1_id, in_stream)
    print("persion_id={} persisted_face id={}".format(person1_id, persisted_face.persisted_face_id))

  blob_names = ["woman1-person-group.jpg", "woman2-person-group.jpg", "woman3-person-group.jpg"]
  for blob_name in blob_names:
    ## get blob to bytes
    # image_blob1 = blobclient.get_blob(container_name, blob1_name)
    ## get blob to stream
    in_stream = io.BytesIO()
    blobclient.get_blob_stream(container_name, blob_name, in_stream)
    in_stream.seek(0)
    persisted_face = api.add_face(person_group_id, person2_id, in_stream)
    print("persion_id={} persisted_face id={}".format(person2_id, persisted_face.persisted_face_id))

  # expected output 
  #persion_id=47ca6a82-f5d1-45a8-9ac2-86a61ad6de90 persisted_face id=837f5342-fa1c-4c3d-bf85-7ace20632f7d
  """
  """
  ## Train PersonGroup
  print("Train Person group:", person_group_id)
  try:
    api.train_person_group(person_group_id)
  except Exception as e:
    print(e)
  """

  container_name = "imageslocal"
  blob_name = "test-image-person-group.jpg"

  """
  blobclient = AzureStorageBlockBlob(storage_account_name,storage_account_key)
  in_stream = io.BytesIO()
  blobclient.get_blob_stream(container_name, blob_name, in_stream)
  in_stream.seek(0)
  ## Identify Face
  api.identify_face(person_group_id, in_stream, max_num_of_candidates_returned=1, confidence_threshold=0.5)
  """
  ret = api.identify_face_blob(person_group_id, container_name, blob_name, max_num_of_candidates_returned=1, confidence_threshold=0.5)
  print(ret)
