import sys
import json
import logging
import azure.functions as func
sys.path.append('../')
from commons.config import Config
from commons.cosmosdb import UserDB

config = Config()

def main(req: func.HttpRequest) -> func.HttpResponse:
  logging.info('getpersons function processed a request.')

  user_id = req.params.get('user_id')
  if not user_id:
    return func.HttpResponse(
      "Please pass a user_id on the query string",
      status_code=400
     )

  logging.info(f"getting presons for user: {user_id}")

  ## Get userinfo from CosmosDB using user_id: CosmosDB
  userdb = UserDB(config)
  try:
    user = userdb.get_user(user_id)
    person_ids =[]
    for p in user['persons']:
      person_ids.append(p['person_id'])
    return func.HttpResponse(json.dumps(person_ids))
  except Exception as e:
    return func.HttpResponse(
        str(e),
        status_code=400
    )
