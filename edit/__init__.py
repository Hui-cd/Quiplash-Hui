import json
import logging

import azure.functions as func
import azure.cosmos as cosmos
import db_operation as db


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    input_json = req.get_json()
    
    username = input_json['username'] 
    password = input_json["password"]
    text = input_json["text"]
    id = input_json["id"]
    id = str(id)
    result ={}
    if db.check_id(id) == True:
        result = {'result': False, 'msg': 'prompt id does not exist'}
        return func.HttpResponse(json.dumps(result),status_code=400)
    elif db.check_prompt_len(text) == False:
        result = {'result': False, 'msg': 'prompt length is <20 or > 100 characters'}
        return func.HttpResponse(json.dumps(result),status_code=400)
    elif db.check_username(username) == False or db.check_password(username,password) == False:
        result = {'result': False, 'msg': 'bad username or password'}
        return  func.HttpResponse(json.dumps(result),status_code=400)
    elif db.check_prompt(text,username) == False:
        result = {'result': False, 'msg': 'This user already has a prompt with the same text'}
        return func.HttpResponse(json.dumps(result),status_code=400)
    else: 
        db.edit(id,username,text)
        result = {'result': True, 'msg': 'OK'}
        return func.HttpResponse(json.dumps(result), status_code=200)
        


