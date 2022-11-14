import unittest

import requests


class TestFunction(unittest.TestCase):
    def test_function(self):
       payload = {'username': '7s18g4', 'add_to_games_played': 1,"password": "89hdorpeyf31"}
       resp = requests.get('http://localhost:7071/api/update/', json=payload)
       self.assertEqual(resp.json()['msg'], "OK")
       
if __name__ == '__main__':
    unittest.main()
