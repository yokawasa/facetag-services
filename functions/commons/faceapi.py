# -*- coding: utf-8 -*-
import logging

import io
from urllib.parse import urlparse
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType
from commons.blockblob import AzureStorageBlockBlob

# Face API
# pip install azure-cognitiveservices-vision-face

# FaceAPI Python SDK
# https://docs.microsoft.com/en-us/azure/cognitive-services/face/quickstarts/python-sdk
# https://azure.microsoft.com/en-us/services/cognitive-services/face/
# https://github.com/Azure-Samples/cognitive-services-quickstart-code/blob/master/python/Face/FaceQuickstart.py

class AzureCognitiveFaceAPI(object):

  def __init__(self, 
      faceapi_endpoint, faceapi_subkey,
      storage_account_name, storage_account_key):
    self._face_client = FaceClient(faceapi_endpoint,CognitiveServicesCredentials(faceapi_subkey))
    self._blob_client = AzureStorageBlockBlob(storage_account_name, storage_account_key)

  def create_person_group(self, group_id, group_name):
    # SDK ref: https://t.ly/PbDGr
    return self._face_client.person_group.create(person_group_id=group_id, name=group_name)

  def train_person_group(self, group_id):
    # SDK ref: https://t.ly/xYkmw
    # Train the person group
    self._face_client.person_group.train(group_id)
    while (True):
      training_status = self._face_client.person_group.get_training_status(group_id)
      print("Training status: {}.".format(training_status.status))
      if (training_status.status is TrainingStatusType.succeeded):
        break
      elif (training_status.status is TrainingStatusType.failed):
        raise Exception("Training the person group has failed")
      time.sleep(5)

  def create_person(self, group_id, person_name):
    # {'additional_properties': {}, 'name': None, 'user_data': None, 'person_id': '683507d1-5c55-4f59-a389-68f8707589ad', 'persisted_face_ids': None}
    # SDK ref:  https://t.ly/K19Bb
    return self._face_client.person_group_person.create(group_id, person_name)

  def add_face_stream(self, group_id, person_id, stream):
    # {'additional_properties': {}, 'persisted_face_id': '4a8313db-6eb8-4a89-b058-23073c04571c', 'user_data': None}
    # SDK ref: https://t.ly/9gnel
    return self._face_client.person_group_person.add_face_from_stream(group_id, person_id, stream)

  def add_face_blob(self, group_id, person_id, container_name, blob_name):
    in_stream = io.BytesIO()
    self._blob_client.get_blob_stream(container_name, blob_name, in_stream)
    in_stream.seek(0)
    return self.add_face_stream(group_id, person_id, in_stream)

  def identify_face_stream(self, group_id, stream, max_num_of_candidates_returned=1, confidence_threshold=None ):
    # Detect faces
    # SDK ref: https://t.ly/K19RP
    face_ids = []
    faces = self._face_client.face.detect_with_stream(stream)
    for face in faces:
      face_ids.append(face.face_id)
    # Identify faces
    # SDK ref: https://t.ly/0vrV5
    # confidence_threshold: 0-1
    results = self._face_client.face.identify(face_ids, group_id,
         max_num_of_candidates_returned=max_num_of_candidates_returned,
         confidence_threshold=confidence_threshold)
    ret = []
    if not results:
      print('No person identified in the person group for faces')
      return ret

    for face in results:
      if len(face.candidates) > 0:
        person_id = face.candidates[0].person_id
        confidence = face.candidates[0].confidence
        # print('face_id: {}, person_id: {}, confidence: {}.'.format(face.face_id, person_id, confidence)) 
        ret.append(
          {
            "face_id": face.face_id,
            "person_id": person_id,
            "confidence": confidence
          }
        )
    return ret

  def identify_face_blob(self, group_id, container_name, blob_name,  max_num_of_candidates_returned=1, confidence_threshold=None ):
    in_stream = io.BytesIO()
    self._blob_client.get_blob_stream(container_name, blob_name, in_stream)
    in_stream.seek(0)
    return self.identify_face_stream(group_id, in_stream, max_num_of_candidates_returned, confidence_threshold)
