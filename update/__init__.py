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
    if 'add_to_games_played' in input_json:
        add_to_games_played = input_json['add_to_games_played']
    else:
        add_to_games_played = 0
        
    if 'add_to_score' in input_json:
        add_to_score = input_json['add_to_score']
    else:
        add_to_score = 0
        
        
    result ={}
    if db.check_username(username) == False:
        result = {'result': False, 'msg': 'user does not exist'}
        return func.HttpResponse(json.dumps(result), status_code=400)
    elif db.check_password(username, password) == False:
        result = {'result': False, 'msg': 'wrong password'}
        return func.HttpResponse(json.dumps(result), status_code=400)
    elif 'add_to_games_played' in input_json and 'add_to_score' in input_json:
        if add_to_games_played <= 0 or add_to_score <= 0:
            result = {'result': False, 'msg': 'Value to add is <=0'}
            return func.HttpResponse(json.dumps(result), status_code=400)
        else:
            db.update(username,add_to_games_played, add_to_score)
            result = {'result': True, 'msg': 'OK'}
            return func.HttpResponse(json.dumps(result), status_code=200)
    elif 'add_to_games_played' in input_json and 'add_to_score' not in input_json:
        if add_to_games_played <= 0:
            result = {'result': False, 'msg': 'Value to add is <=0'}
            return func.HttpResponse(json.dumps(result), status_code=400)
        else:
            db.update(username,  add_to_games_played, 0)
            result = {'result': True, 'msg': 'OK'}
            return func.HttpResponse(json.dumps(result), status_code=200)
        
    elif 'add_to_games_played' not in input_json and 'add_to_score' in input_json:
        if add_to_score <= 0:
            result = {'result': False, 'msg': 'Value to add is <=0'}
            return func.HttpResponse(json.dumps(result), status_code=400)
        else:
            db.update(username, 0, add_to_score)
            result = {'result': True, 'msg': 'OK'}
            return func.HttpResponse(json.dumps(result), status_code=200)

