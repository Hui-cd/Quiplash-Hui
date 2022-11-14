import json
import logging

import azure.functions as func
import azure.cosmos as cosmos
import db_operation as db


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Computing Top Huggers in the Cloud')
    # 得到 json形式{username :[{}]}
    # username = req.params.get('username')
    input_json = req.get_json()
    
    username = input_json['username'] 
    password = input_json["password"]
    result ={}
    # result = {'result': 'true', 'msg': 'OK'}
    # result = {"username": username}
    # password = req.params.get('password')
    # result={}
    
    if not db.check_password_len(password):
        result = {'result': False, 'msg': 'Password less than 8 characters or more than 24 characters'}
        return func.HttpResponse(body=json.dumps(result), status_code=400)
    elif not db.check_username_len(username):
        result = {'result': False, 'msg': 'Username less than 4 characters or more than 16 characters'}
        return func.HttpResponse(body=json.dumps(result), status_code=400)
    elif db.check_username(username):
        result = {'result': False, 'msg': 'Username already exists'}
        return func.HttpResponse(body=json.dumps(result), status_code=400)
    else: 
        db.create_player(username, password)
        result = {'result': True, 'msg': 'OK'}
        return func.HttpResponse(body=json.dumps(result), status_code=200)
        