import sys
import json
import logging
import azure.functions as func
sys.path.append('../')
from commons.config import Config
from commons.cosmosdb import AssetDB

config = Config()

def main(req: func.HttpRequest) -> func.HttpResponse:
  logging.info('getassets function processed a request.')

  user_id = req.params.get('user_id')
  if not user_id:
    return func.HttpResponse(
      "Please pass a user_id on the query string",
      status_code=400
     )

  logging.info(f"getting presons for user: {user_id}")

  ## Get assets list from CosmosDB using user_id: CosmosDB
  assetdb = AssetDB(config)
  try:
    assets = assetdb.get_assets(user_id)
    return func.HttpResponse(json.dumps(assets))
  except Exception as e:
    return func.HttpResponse(
        str(e),
        status_code=400
    )
