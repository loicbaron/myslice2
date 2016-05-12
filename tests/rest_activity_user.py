#!/usr/bin/env python3.5

import json
import requests
import sys
import unittest

from pprint import pprint

from tests import s

class TestUser(unittest.TestCase):

    def setUp(self):
        self.timeout = 10

    def test_0_invalidRequest(self):
        payload = {'key1': 'value1', 'key2': 'value2'}
        r = requests.post("http://localhost:8111/api/v1/activity", data=payload, timeout=self.timeout)
        self.assertEqual(r.status_code, 400)

    def test_1_create_user_fail(self):
        payload = {
                "event": {
                    "action":"CREATE",
                    "user":"urn:publicid:IDN+onelab:upmc+user+",
                    "object":{
                        "type": "USER",
                        "id": "urn:publicid:IDN+onelab:upmc+user+test_auto"
                    },
                    "data":{
                        "email": "test_auto_onelab@yopmail.com",
                        "first_name": "test auto",
                        "last_name": "OneLab",
                        "bio": "...",
                        "url": "http://onelab.eu",
                        "password": "...",
                        "generate_keys": True,
                        "keys": []
                    }
                }
            }
        r = requests.post("http://localhost:8111/api/v1/activity", headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), timeout=self.timeout)
        self.assertEqual(r.status_code, 500)

    def test_2_create_user(self):
        payload = {
                "event": {
                    "action":"CREATE",
                    "user":"urn:publicid:IDN+onelab:upmc+user+loic_baron",
                    "object":{
                        "type": "USER",
                        "id": "urn:publicid:IDN+onelab:upmc+user+test_auto"
                    },
                    "data":{
                        "email": "test_auto_onelab@yopmail.com",
                        "first_name": "test auto",
                        "last_name": "OneLab",
                        "bio": "...",
                        "url": "http://onelab.eu",
                        "password": "...",
                        "generate_keys": True,
                        #"keys": []
                    }
                }
            }
        r = requests.post("http://localhost:8111/api/v1/activity", headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), timeout=self.timeout)
        pprint(r.text)
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.text)
        self.assertEqual(result['return']['messages']['object'], payload['event']['object'])
        # Check each value sent, can't check result==payload because the API is adding hrn, id and authority to the data
        for k,v in payload['event']['data'].items():
            self.assertEqual(result['return']['messages']['data'][k], v)

    def test_3_update_user(self):
        payload = {
                "event": {
                    "action":"UPDATE",
                    "user":"urn:publicid:IDN+onelab:upmc+user+loic_baron",
                    "object":{
                        "type": "USER",
                        "id": "urn:publicid:IDN+onelab:upmc+user+test_auto"
                    },
                    "data":{
                        "email": "test_auto_onelab@yopmail.com",
                        "first_name": "test auto",
                        "last_name": "updated",
                        "bio": "...",
                        "url": "http://onelab.eu",
                        "password": "...",
                        #"keys": ['ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCXE8DJbz/WZxDG1w3McxipIBSdL8FHNmCFFlWPB3mWzujK1LPR0fzLpf+jD30aXmppB4O3WUr7qtuhPWsj2DQGvH5PxtX70hf0ehJeqHFCEn9n0+dt0+LLanuQHsPZQujp7tDkPTc5nz2b4xKn4MbZfpGQ8bwTPWfJ130felrFMsYOWlT2y/0u2pkvmUO9wxwSZxe/giqe9XlJ38rwy+V/Jt7iCR+VSHB5vqv/Hi8FBFKhqydtTSlEeY9X9f90GXKPCHEqmH0g37Vdy2V9LC4CQVECSrqQjBo31BAfdwsmKKsXzaK5sBOva3Y9rFHPlfDaf2beiMibjU5pjNDGVOLJ root@theseus']
                    }
                }
            }
        r = requests.post("http://localhost:8111/api/v1/activity", headers={str('Content-Type'):'application/json'}, data=json.dumps(payload))
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.text)
        self.assertEqual(result['return']['messages']['object'], payload['event']['object'])
        # Check each value sent, can't check result==payload because the API is adding hrn, id and authority to the data
        for k,v in payload['event']['data'].items():
            self.assertEqual(result['return']['messages']['data'][k], v)


    def test_4_delete_user(self):
        payload = {
                "event": {
                    "action":"DELETE",
                    "user":"urn:publicid:IDN+onelab:upmc+user+loic_baron",
                    "object":{
                        "type": "USER",
                        "id": "urn:publicid:IDN+onelab:upmc+user+test_auto"
                    }
                }
            }
        r = requests.post("http://localhost:8111/api/v1/activity", headers={str('Content-Type'):'application/json'}, data=json.dumps(payload))
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.text)
        self.assertEqual(result['return']['messages']['object'], payload['event']['object'])

if __name__ == '__main__':
    unittest.main()
