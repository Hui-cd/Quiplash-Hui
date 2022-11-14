import json
import logging

import azure.functions as func

import db_operation as db


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    input_json = req.get_json()
    result={}
    if 'prompts' in input_json and 'players' not in input_json:
        prompts = input_json['prompts']
        result = db.getN(prompts)
        return func.HttpResponse(json.dumps(result), status_code=200)
    elif 'prompts' not in input_json and 'players' in input_json:
        players = input_json['players']
        result = db.get_prompts_by_user(players)
        return func.HttpResponse(json.dumps(result), status_code=200)