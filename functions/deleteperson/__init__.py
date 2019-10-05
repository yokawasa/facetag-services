import logging

import azure.functions as func

"""
DELETE /api/deleteperson?user_id={user_id}&person_id={person_id}
"""

def main(req: func.HttpRequest) -> func.HttpResponse:
  logging.info('deleteperson function processed a request.')

  user_id = req.params.get('user_id')
  person_id = req.params.get('person_id')
  if not user_id or not person_id:
    return func.HttpResponse(
      "Please pass both user_id and person_id on the query string or in the request body",
      status_code=400
    )
  logging.info(f"deleting person: {person_id} for user: {user_id}")
  # FIXME
  return func.HttpResponse(person_id)
