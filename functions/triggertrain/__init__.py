# -*- coding: utf-8 -*-
import json
import logging
import azure.functions as func

def main(req: func.HttpRequest, msg: func.Out[str]) -> func.HttpResponse:
  logging.info('Python HTTP trigger function processed a request.')

  user_id = req.params.get('user_id')
  person_id = req.params.get('person_id')

  if not user_id or not person_id:
    return func.HttpResponse(
        "Please pass both user_id and person_id on the query string",
        status_code=400
    )

  try:

    sending_message = json.dumps(
      {
        "user_id": user_id,
        "person_id": person_id
      }
    )
    msg.set(sending_message)

  except Exception as e:
    logging.info(e)
    return func.HttpResponse(
      str(e),
      status_code=400 )
  except ValueError as ve:
    logging.info(ve)
    return func.HttpResponse(
      str(ve),
      status_code=400 )

  return func.HttpResponse("OK")
