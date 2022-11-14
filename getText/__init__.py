import logging

import azure.functions as func
import azure.cosmos as cosmos
import json
import db_operation as db

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    input_json = req.get_json()
    word = input_json["word"]
    exact = input_json["exact"]
    result ={}
    result = db.get_word(word, exact)
    return func.HttpResponse(body=json.dumps(result), status_code=200)



