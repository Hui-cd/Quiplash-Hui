import json
import logging

import azure.functions as func
import azure.cosmos as cosmos
import db_operation as db

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    input_json = req.get_json()
    try:
        username = input_json['username']
        password = input_json['password']
    except:
        return func.HttpResponse(
            "Please pass a username and password in the request body",
            status_code=400
        )
        
        

    result={}
    if db.login(username, password)==True:
        result = {'result': True, 'msg': 'OK'}
        return func.HttpResponse(body=json.dumps(result), status_code=200)
    else:
        result = {'result': False, 'msg': 'Username or password incorrect'}
        return func.HttpResponse(body=json.dumps(result), status_code=400)
    
