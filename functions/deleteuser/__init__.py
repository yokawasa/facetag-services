# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

import logging
import azure.functions as func
from commons.blockblob import AzureStorageBlockBlob
from commons.config import Config
from commons.cosmosdb import AssetDB, UserDB

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello {name}!")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
