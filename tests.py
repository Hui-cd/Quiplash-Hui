import unittest
import requests
import random
import time

import azure.functions as func

url = 'https://yg1a20.azurewebsites.net/api'
name = "".join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 6))
pswd = "".join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 12))
name2 = "".join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 6))
pswd2 = "".join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 12))
name3 = "".join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 6))
pswd3 = "".join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 12))
text = "".join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 22))
text2 = "".join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 19))
text3 = "".join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 20))
timestamp = int(round(time.time() * 1000))


class TestFunction(unittest.TestCase):
    def test1(self):
        resp = requests.get(url + "/player/register/", json={"username":  name, "password": pswd})
        resp2 = requests.get(url + "/player/register/", json={"username":  name2, "password": pswd2})
        self.assertEqual(resp.json()['result'], True)

    def test2(self):
        resp = requests.get(url + "/player/register/", json={"username":  name, "password": pswd})
        self.assertEqual(resp.json()['msg'], "Username already exists")

    def test3(self):
        resp = requests.get(
            url + "/player/register/", json={"username":  "nsk", "password": "238sdcdsj"})
        self.assertEqual(
            resp.json()['msg'], "Username less than 4 characters or more than 16 characters")

    def test4(self):
        resp = requests.get(
            url + "/player/register/", json={"username":  "238cksnkddskcdksddsj", "password": "238sdcdsj"})
        self.assertEqual(
            resp.json()['msg'], "Username less than 4 characters or more than 16 characters")

    def test5(self):
        resp = requests.get(
            url + "/player/register/", json={"username":  "dsjnkd", "password": "sdcdsj"})
        self.assertEqual(
            resp.json()['msg'], "Password less than 8 characters or more than 24 characters")

    def test6(self):
        resp = requests.get(
            url + "/player/register/", json={"username":  "dsjcnkd", "password": "sdcdsdehd23sdtysb2sdad83bssj"})
        self.assertEqual(
            resp.json()['msg'], "Password less than 8 characters or more than 24 characters")

    def test7(self):
        resp = requests.get(url + "/player/login/", json={"username": name, "password": pswd})
        self.assertEqual(resp.json()['result'], True)

    def test8(self):
        resp = requests.get(url + "/player/login/", json={"username": name, "password": pswd2})
        self.assertEqual(resp.json()['msg'], "Username or password incorrect")
        
    def test9(self):
        resp = requests.get(url + "/player/login/", json={"username": name3, "password": pswd3})
        self.assertEqual(resp.json()['msg'], "Username or password incorrect")
        
    def test10(self):
        resp = requests.get(url + "/player/update/", json={"username": name3, "password": pswd3, "add_to_games_played": 1, "add_to_score": 1})
        self.assertEqual(resp.json()['msg'], "user does not exist")
        
    def test11(self):
        resp = requests.get(url + "/player/update/", json={"username": name2, "password": pswd2, "add_to_games_played": 0, "add_to_score": 1000})
        self.assertEqual(resp.json()['msg'], "Value to add is <=0")
        
    def test12(self):
        resp = requests.get(url + "/player/update/", json={"username": name, "password": pswd, "add_to_score": timestamp + 100})
        resp = requests.get(url + "/player/update/", json={"username": name2, "password": pswd2, "add_to_score": timestamp})
        self.assertEqual(resp.json()['msg'], "OK")
        
    def test13(self):
        resp = requests.get(url + "/player/update/", json={"username": name, "password":pswd2, "add_to_games_played": 100})
        self.assertEqual(resp.json()['msg'], "wrong password")
        
    def test14(self):
        resp = requests.get(url + "/player/leaderboard/", json={"top": 2})
        self.assertEqual(resp.json()[0]['username'], name)
        self.assertEqual(resp.json()[1]['score'], timestamp)
        self.assertEqual(len(resp.json()), 2)
        
    def test15(self):
        resp = requests.get(url + "/prompt/create/", json={"username": name, "password": pswd, "text": text})
        self.assertEqual(resp.json()['msg'], "OK")
        
    def test16(self):
        resp = requests.get(url + "/prompt/create/", json={"username": name, "password": pswd, "text": text})
        self.assertEqual(resp.json()['msg'], "This user already has a prompt with the same text")
        
    def test17(self):
        resp = requests.get(url + "/prompt/create/", json={"username": name, "password": pswd, "text": text2})
        self.assertEqual(resp.json()['msg'], "prompt length is <20 or > 100 characters")
        
    def test18(self):
        resp = requests.get(url + "/prompt/create/", json={"username": name, "password": pswd2, "text": text})
        self.assertEqual(resp.json()['msg'], "bad username or password")
        
    def test19(self):
        resp = requests.get(url + "/prompt/create/", json={"username": name2, "password": pswd2, "text": text})
        self.assertEqual(resp.json()['msg'], "OK")
        
    def test20(self):
        resp = requests.get(url + "/prompt/create/", json={"username": name2, "password": pswd2, "text": text3})
        self.assertEqual(resp.json()['msg'], "OK")
        
    def test21(self):
        resp = requests.get(url + "/prompts/get", json={"prompts" : 3})
        self.assertEqual(len(resp.json()), 3)
        
    def test22(self):
        resp = requests.get(url + "/prompts/get", json={"players": [name, name2]})
        self.assertEqual(len(resp.json()), 3)
        
    def test23(self):
        id1 = requests.get(url + "/prompts/get", json=({"players": [name]})).json()[0]['id']
        resp = requests.get(url + "/prompt/edit/", json={"username": name, "password": pswd, "text": text3, "id": int(id1)})
        self.assertEqual(resp.json()['msg'], "OK")
        self.assertIsInstance(id1, int)
        
    def test24(self):
        ct2 = requests.get(url + "/prompts/get", json=({"players": [name2]})).json()[0]['text']
        id3 = requests.get(url + "/prompts/get", json=({"players": [name2]})).json()[1]['id']
        resp = requests.get(url + "/prompt/edit/", json={"username": name2, "password": pswd2, "text": ct2, "id": int(id3)})
        self.assertEqual(resp.json()['msg'], "This user already has a prompt with the same text")
    
    def test25(self):
        id3 = requests.get(url + "/prompts/get", json=({"players": [name2]})).json()[1]['id']
        resp = requests.get(url + "/prompt/delete/", json={"username": name2, "password": pswd2, "id": int(id3)})
        resp2 = requests.get(url + "/prompt/delete/", json={"username": name2, "password": pswd2, "id": int(id3)})
        resp3 = requests.get(url + "/prompt/edit/", json={"username": name2, "password": pswd2, "text": text3, "id": int(id3)})
        self.assertEqual(resp.json()['msg'], "OK")
        self.assertEqual(resp2.json()['msg'], "prompt id does not exist")
        self.assertEqual(resp3.json()['msg'], "prompt id does not exist")
        
    def test26(self):
        id1 = requests.get(url + "/prompts/get", json=({"players": [name]})).json()[0]['id']
        resp = requests.get(url + "/prompt/delete/", json={"username": name, "password": pswd2, "id": int(id1)})
        resp2 = requests.get(url + "/prompt/delete/", json={"username": name2, "password": pswd2, "id": int(id1)})
        self.assertEqual(resp.json()['msg'], "bad username or password")
        self.assertEqual(resp2.json()['msg'], "access denied")
        
    def test27(self):
        resp = requests.get(url + "/prompt/edit/", json={'id':1,"username": name, "password": pswd, "text": text2})
        self.assertEqual(resp.json()['msg'], "prompt length is <20 or > 100 characters")
        
    def test28(self):
        resp = requests.get(url + "/prompt/edit/", json={'id':2,"username": name, "password": pswd2, "text": text})
        self.assertEqual(resp.json()['msg'], "bad username or password")
        
    def test29(self):
        res1 = requests.get(url + "/prompt/create/", json={"username": name, "password": pswd, "text": "What Program you would never code in JavaScript"})
        res2 = requests.get(url + "/prompt/create/", json={"username": name, "password": pswd, "text": "What is the funniest programming language?"})
        res3 = requests.get(url + "/prompt/create/", json={"username": name, "password": pswd, "text": "How many lines your shorter program has?"})
        resp = requests.get(url + "/prompts/getText/", json={"word" : "program", "exact" : True})
        resp2 = requests.get(url + "/prompts/getText/", json={"word" : "program", "exact" : False})
        self.assertEqual(len(resp.json()), 1)
        self.assertEqual(len(resp2.json()), 2)
        self.assertIsInstance(resp.json()[0]['id'], int)
        
    def test30(self):
        resp = requests.get(url + "/prompts/getText/", json={"word" : "has", "exact" : True})
        resp2 = requests.get(url + "/prompts/getText/", json={"word" : "has", "exact" : False})
        self.assertEqual(len(resp.json()), 1)
        self.assertEqual(len(resp2.json()), 1)
        
if __name__ == '__main__':
    unittest.main()