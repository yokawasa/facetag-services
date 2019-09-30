import json
import logging
import azure.functions as func

def main(req: func.HttpRequest, msg: func.Out[str]) -> func.HttpResponse:
  logging.info('Python HTTP trigger function processed a request.')

  try:
    req_body = req.get_json()
    logging.info('req_body=%s',req_body)
    user_id = req_body.get('user_id')
    person_id = req_body.get('person_id')

    if not user_id or not person_id:
      return func.HttpResponse(
          "Please pass both user_id and person_id on the query string or in the request body",
          status_code=400
      )

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


