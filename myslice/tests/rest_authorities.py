import json
import requests
import sys
import unittest

from pprint import pprint

from config import s
class TestAuthority(unittest.TestCase):

    def setUp(self):
        self.timeout = 10
        self.cookies = s['cookies']


# GET
    #test_get_authorities_id_0_as_unauth - open to get all authorities in the registration
    def test_get_0_noAuth(self):
        r = requests.get('http://localhost:8111/api/v1/authorities')
        self.assertEqual(r.status_code, 200)

    #test_get_authorities_id_1_as_pi - Checking if API responded with the same values as rethinkdb for the PI User
    def test_get_1_Auth_Pi (self):
        payload = {'email': s['email'], 'password': s['password']}
        r= requests.get('http://localhost:8111/api/v1/authorities', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), timeout=self.timeout)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(hasattr(r,'cookies'))
        self.assertIsNotNone(r.cookies)

    def test_get_0_auth(self):
        r = requests.get('http://localhost:8111/api/v1/authorities', cookies=self.cookies)
        self.assertEqual(r.status_code, 200)

#POST

#PUT

#DELETE

if __name__ == '__main__':
    unittest.main()
