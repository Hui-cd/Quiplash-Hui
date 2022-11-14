import logging

import azure.functions as func
import azure.cosmos as cosmos
import json
import db_operation as db


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    input_json = req.get_json()
    
    username = input_json['username'] 
    password = input_json["password"]
    id = str(input_json["id"])
    # id = req.params.get('id')
    # username = req.params.get('username')
    # password = req.params.get('password')
    result ={}
    if db.check_username(username) == False or db.check_password(username,password) == False:
        result = {'result': False, 'msg': 'bad username or password'}
        return func.HttpResponse(json.dumps(result),status_code=400)
    elif db.check_id(id) == True:
        result = {'result': False, 'msg': 'prompt id does not exist'}
        return func.HttpResponse(json.dumps(result),status_code=400)
    elif db.check_id_user(id, username) == True:
        result = {'result': False, 'msg': 'access denied'}
        return func.HttpResponse(json.dumps(result),status_code=400)
    else:
        db.delete_prompt(id, username)
        result = {'result': True, 'msg': 'OK'}
        return func.HttpResponse(json.dumps(result),status_code=200)
        
    