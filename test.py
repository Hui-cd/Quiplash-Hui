import unittest
import json
# We use the requests library to communicate with servers programatically 
# You should install it in your virtual environment using pip install requests
# Read this: https://requests.readthedocs.io/en/latest/user/quickstart/#make-a-request
import requests 

import azure.functions as func
#Important for the import name to match the case of the Function folder

login_url = ' http://localhost:7071/api/player/login'
register_url = ' http://localhost:7071/api/player/register'
update_url = ' http://localhost:7071/api/player/update'
leaderboard_url = ' http://localhost:7071/api/player/leaderboard'
create_url = ' http://localhost:7071/api/prompt/create'
edit_url = ' http://localhost:7071/api/prompt/edit'
delete_url = ' http://localhost:7071/api/prompt/delete'
get_url = ' http://localhost:7071/api/prompts/get'
getText_url = 'http://localhost:7071/api/prompts/getText'



class TestFunction(unittest.TestCase):
##########################################################################################################
###################################  LOGIN TEST #######################################################
##########################################################################################################
    def test_login(self):
        payload={"username": "py_luis" , "password": "pythonrulz"}

        resp = requests.get(
                #This is the URL of the function deployed in the local development server
                # The URL of the function deployed in your server changes depending on the name you assigned
                login_url, 
                #send payload as JSON
                json = payload)
        
        result = resp.json()
        self.assertEqual(result['result'], True)
        self.assertEqual(result['msg'], 'OK')
        
    def test_login_false(self):
        payload={"username": "py_luidss" , "password": "pythonrulz"}

        resp = requests.get(
               
                login_url, 
             
                json = payload)
        
        result = resp.json()
        self.assertEqual(result['result'], False)
        self.assertEqual(result['msg'], 'Username or password incorrect')
        
##########################################################################################################
###################################  REGISTER TEST #######################################################
##########################################################################################################
    def test_register_false(self):
        payload={"username": "py_luis" , "password": "pythonrulz"}

        resp = requests.get(
       
                register_url ,
    
                json = payload)
        
        result = resp.json()
        self.assertEqual(result['result'], False)
        self.assertEqual(result['msg'], 'Username already exists')

    def test_register_success(self):
        payload={"username": "Husdsdki" , "password": "12345678910"}

        resp = requests.get(
               
                register_url, 
             
                json = payload)
        
        result = resp.json()
        self.assertEqual(result['result'], True)
        self.assertEqual(result['msg'], 'OK')
    
    def test_check_username(self):
        payload={"username": "py" , "password": "pythonrulz"}
        resp = requests.get(register_url,  json = payload)
        
        result = resp.json()
        self.assertEqual(result['result'], False)
        self.assertEqual(result['msg'], 'Username less than 4 characters or more than 16 characters')
    
    def test_check_password(self):
        payload={"username": "py_luis" , "password": "123"}
        resp = requests.get(register_url,  json = payload)
        
        result = resp.json()
        self.assertEqual(result['result'], False)
        self.assertEqual(result['msg'], 'Password less than 8 characters or more than 24 characters')
        
        
##########################################################################################################
###################################  UPDATE TEST ########################################################
##########################################################################################################
    def test_update_add_played(self):
        payload={"username": "py_luis" , "add_to_games_played": 123,'password': 'pythonrulz'}
        resp = requests.get(update_url,  json = payload)
        
        result = resp.json()
        self.assertEqual(result['result'], True)
        self.assertEqual(result['msg'], 'OK')
        
    def test_update_value(self):
        payload={"username": "py_luis" , "add_to_games_played": -12,'password': 'pythonrulz'}
        resp = requests.get(update_url,  json = payload)
        
        result = resp.json()
        self.assertEqual(result['result'], False)
        self.assertEqual(result['msg'], 'Value to add is <=0')
        
    def test_update_password(self):
        payload={"username": "py_luis" , "add_to_games_played": 12,'password': 'pythonrulasdadasdasdz'}
        resp = requests.get(update_url,  json = payload)
        
        result = resp.json()
        self.assertEqual(result['result'], False)
        self.assertEqual(result['msg'], 'wrong password')
##########################################################################################################
###################################  LeaderBoard TEST ########################################################
##########################################################################################################
        
    def test_leaderboard(self):
        payload={'top':10}
        resp = requests.get(leaderboard_url,  json = payload)
        
        result = resp.json()
        print(result)

    
##########################################################################################################
###################################  CREATE TEST ########################################################
##########################################################################################################
#error
    def test_create_exist_prompt(self):
        payload={'text':"What app you would never code in JavaScript?",'username':'py_luis','password': 'pythonrulz'}
        resp = requests.get(create_url,  json = payload)
        result = resp.json()
        self.assertEqual(result['result'], False)
        self.assertEqual(result['msg'], 'This user already has a prompt with the same text')

    def test_prompt_len(self):
        payload = {'text':"What",'username':'py_luis','password': 'pythonrulz'}
        resp = requests.get(create_url,  json = payload)
        result = resp.json()
        self.assertEqual(result['result'], False)
        self.assertEqual(result['msg'], 'prompt length is <20 or > 100 characters')
    def test_prompt_username(self):
        payload = {'text':"This is use for test ",'username':'py_luisasdasd','password': 'pythonrulz'}
        resp = requests.get(create_url,  json = payload)
        result = resp.json()
        self.assertEqual(result['result'], False)
        self.assertEqual(result['msg'], 'bad username or password')
        # error
    def test_prompt_password(self):
        payload = {'text':"This is use for test ",'username':'py_luis','password': 'pythonrulz123123'}
        resp = requests.get(create_url,  json = payload)
        result = resp.json()
        self.assertEqual(result['result'], False)
        self.assertEqual(result['msg'], 'bad username or password')
        #error
    def test_create_prompt(self):
        payload = {'text':"This is use for test create",'username':'py_luis','password': 'pythonrulz'}
        resp = requests.get(create_url,  json = payload)
        result = resp.json()
        self.assertEqual(result['result'], True)
        self.assertEqual(result['msg'], 'OK')
        
##########################################################################################################
###################################  EDIT TEST ########################################################
##########################################################################################################   

    def test_edit_promptID_exist(self):
        payload = {'id':10,'text':"This is use for test prompt id ",'username':'py_luis','password': 'pythonrulz'}
        resp = requests.get(edit_url,  json = payload)
        result = resp.json()
        self.assertEqual(result['result'], False)
        self.assertEqual(result['msg'], 'prompt id does not exist')
    
    def test_edit_check_username(self):
        payload = {'id':420,'text':"This is use for test prompt id ",'username':'py_luisasdasd','password': 'pythonrulz'}
        resp = requests.get(edit_url,  json = payload)
        result = resp.json()
        self.assertEqual(result['result'], False)
        self.assertEqual(result['msg'], 'bad username or password')
        
    def test_edit_check_password(self):
        payload = {'id':420,'text':"This is use for test prompt id ",'username':'py_luis','password': 'pythonrulzdasd'}
        resp = requests.get(edit_url,  json = payload)
        result = resp.json()
        self.assertEqual(result['result'], False)
        self.assertEqual(result['msg'], 'bad username or password')
        
    def test_edit_same_prompt(self):
        payload = {'id':420,'text':"What app you would never code in JavaScript?",'username':'py_luis','password': 'pythonrulz'}
        resp = requests.get(edit_url,  json = payload)
        result = resp.json()
        self.assertEqual(result['result'], False)
        self.assertEqual(result['msg'], 'This user already has a prompt with the same text')
    def test_edit(self):
        payload = {'id':420,'text':"this is used to test edit ",'username':'py_luis','password': 'pythonrulz'}
        resp = requests.get(edit_url,  json = payload)
        result = resp.json()
        self.assertEqual(result['result'], True)
        self.assertEqual(result['msg'], 'OK')
        
##########################################################################################################
###################################  DELETE TEST ########################################################
########################################################################################################## 
    def test_delete_promptID_exist(self):
        payload = {'id':10,'username':'py_luis','password': 'pythonrulz'}
        resp = requests.get(delete_url,  json = payload)
        result = resp.json()
        self.assertEqual(result['result'], False)
        self.assertEqual(result['msg'], 'prompt id does not exist')
        
    def test_delete_check_username(self):
        payload = {'id':420,'username':'py_luisasdasd','password': 'pythonrulz'}
        resp = requests.get(delete_url,  json = payload)
        result = resp.json()
        self.assertEqual(result['result'], False)
        self.assertEqual(result['msg'], 'bad username or password')
        
    def test_delete_check_password(self):
        payload = {'id':420,'username':'py_luis','password': 'pythonrulzdasd'}
        resp = requests.get(delete_url,  json = payload)
        result = resp.json()
        self.assertEqual(result['result'], False)
        self.assertEqual(result['msg'], 'bad username or password')
    def test_delete_access_denied(self):
        payload = {'id':2,'username':'py_luis','password': 'pythonrulz'}
        resp = requests.get(delete_url,  json = payload)
        result = resp.json()
        self.assertEqual(result['result'],False)
        self.assertEqual(result['msg'], 'access denied')
        
    def test_delete(self):
        payload = {'id':3,'username':'py_luis','password': 'pythonrulz'}
        resp = requests.get(delete_url,  json = payload)
        result = resp.json()
        self.assertEqual(result['result'], True)
        self.assertEqual(result['msg'], 'OK')
    
    
    def test_get_player(self):
        payload = {"players":["py_luis","dasdad"]}
        resp = requests.get(get_url,  json = payload)
        result = resp.json()
        print(result)
        
    def test_get_prompt(self):
        payload = {"prompts":5}
        resp = requests.get(get_url,  json = payload)
        result = resp.json()
        print(result)
        
    def test_get_text(self):
        payload = {"word" : "What " , "exact" : True}
        resp = requests.get(getText_url,  json = payload)
        result = resp.json()
        print(result)
    
        
if __name__ == '__main__':
    unittest.main()
