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
        password = input_json["password"]
        text = input_json["text"]
    except:
        return func.HttpResponse(
             "Please pass a username, password and text on the query string or in the request body",
             status_code=400
        )  
        
    result ={}
    if db.check_password(username,password) == False or db.check_username(username) == False:
        result = {'result': False, 'msg': 'bad username or password'}
        return func.HttpResponse(json.dumps(result),status_code=400)
    elif db.check_prompt_len(text) == False:
        result = {'result': False, 'msg': 'prompt length is <20 or > 100 characters'}
        return func.HttpResponse(json.dumps(result),status_code=400)
    elif db.check_prompt(text,username) == False:
        result = {'result': False, 'msg': 'This user already has a prompt with the same text'}
        return  func.HttpResponse(json.dumps(result),status_code=400)
    else:
        db.create_prompt(username, text)
        result = {'result': True, 'msg': 'OK'}
        return func.HttpResponse(body=json.dumps(result), status_code=200)

