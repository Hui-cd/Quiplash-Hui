import json
import logging

import azure.functions as func
import azure.cosmos as cosmos
import db_operation as db


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    input_json = req.get_json()
    
    top = input_json['top']
    result = {}
    result = db.get_leaderboard(top)
    return func.HttpResponse(body=json.dumps(result), status_code=200)