#!/usr/bin/env python3.5

import json
import requests
import sys
import unittest

from pprint import pprint

from tests import s

class TestUser(unittest.TestCase):

    #def setUp(self):

    def test_invalidRequest(self):
        payload = {'key1': 'value1', 'key2': 'value2'}
        r = requests.post("http://localhost:8111/api/v1/activity", data=payload)
        self.assertEqual(r.status_code, 400)

    def test_create_user_fail(self):
        payload = {
                "event": {
                    "action":"CREATE",
                    "user":"urn:publicid:IDN+onelab:upmc+user+",
                    "object":{
                        "type": "USER",
                        "id": "urn:publicid:IDN+onelab:upmc+user+test_auto"
                        }
                    },
                    "data":{
                        "email": "test_auto_onelab@yopmail.com",
                        "first_name": "test auto",
                        "last_name": "OneLab",
                        "bio": "...",
                        "url": "http://onelab.eu",
                        "password": "...",
                        "keys": []
                    }
                }
        r = requests.post("http://localhost:8111/api/v1/activity", headers={str('Content-Type'):'application/json'}, data=json.dumps(payload))
        pprint(r.text)
        self.assertEqual(r.status_code, 500)

    def test_create_user(self):
        payload = {
                "event": {
                    "action":"CREATE",
                    "user":"urn:publicid:IDN+onelab:upmc+user+loic_baron",
                    "object":{
                        "type": "USER",
                        "id": "urn:publicid:IDN+onelab:upmc+user+test_auto"
                        }
                    },
                    "data":{
                        "email": "test_auto_onelab@yopmail.com",
                        "first_name": "test auto",
                        "last_name": "OneLab",
                        "bio": "...",
                        "url": "http://onelab.eu",
                        "password": "...",
                        "keys": []
                    }
                }
        r = requests.post("http://localhost:8111/api/v1/activity", headers={str('Content-Type'):'application/json'}, data=json.dumps(payload))
        pprint(r.text)
        self.assertEqual(r.status_code, 200)

if __name__ == '__main__':
    unittest.main()
