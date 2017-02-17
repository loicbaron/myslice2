#!/usr/bin/env python3.5

import json
import requests
import sys
import unittest

from pprint import pprint

from tests import s

class TestSlice(unittest.TestCase):

    def setUp(self):
        self.timeout = 30
        result = requests.get("http://"+server+":8111/api/v1/resources", headers={str('Content-Type'): 'application/json'}, timeout=self.timeout)
        resources = json.loads(result.text)
        self.resource = resources['result'][0]['id']

    #def test_1_create_user(self):
    #    payload = {
    #            "event": {
    #                "action":"CREATE",
    #                "user":"urn:publicid:IDN+onelab:upmc+user+loic_baron",
    #                "object":{
    #                    "type": "USER",
    #                    "id": "urn:publicid:IDN+onelab:upmc+user+test_auto"
    #                },
    #                "data":{
    #                    "email": "test_auto_onelab@yopmail.com",
    #                    "first_name": "test auto",
    #                    "last_name": "OneLab",
    #                    "bio": "...",
    #                    "url": "http://onelab.eu",
    #                    "password": "...",
    #                    "generate_keys": True,
    #                    "keys": []
    #                }
    #            }
    #        }
    #    r = requests.post("http://"+server+":8111/api/v1/activity", headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), timeout=self.timeout)
    #    pprint(r.text)
    #    self.assertEqual(r.status_code, 200)
    #    result = json.loads(r.text)
    #    self.assertEqual(result['return']['messages']['object'], payload['event']['object'])
    #    # Check each value sent, can't check result==payload because the API is adding hrn, id and authority to the data
    #    for k,v in payload['event']['data'].items():
    #        self.assertEqual(result['return']['messages']['data'][k], v)

    #def test_2_create_project(self):
    #    payload = {
    #            "event": {
    #                "action":"CREATE",
    #                "user":"urn:publicid:IDN+onelab:upmc+user+loic_baron",
    #                "object":{
    #                    "type": "PROJECT",
    #                    "id": "urn:publicid:IDN+onelab:upmc:apitest+authority+sa"
    #                },
    #                "data":{
    #                    "name": "Test Autority",
    #                    #"pi_users": ["urn:publicid:IDN+onelab:upmc+user+loic_baron"]
    #                }
    #            }
    #        }
    #    r = requests.post("http://"+server+":8111/api/v1/activity", headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), timeout=self.timeout)
    #    self.assertEqual(r.status_code, 200)
    #    result = json.loads(r.text)
    #    # Check each value sent, can't check result==payload because the API is adding hrn, id and authority to the data
    #    for k, v in payload['event']['data'].items():
    #        self.assertEqual(result['return']['messages']['data'][k], v)

    #def test_3_addUser_project(self):
    #    payload = {
    #            "event": {
    #                "action":"ADD",
    #                "user":"urn:publicid:IDN+onelab:upmc+user+loic_baron",
    #                "object":{
    #                    "type": "PROJECT",
    #                    "id": "urn:publicid:IDN+onelab:upmc:apitest+authority+sa"
    #                },
    #                "data":{
    #                    "type": "PI",
    #                    "values": ["urn:publicid:IDN+onelab:upmc+user+test_auto"]
    #                }
    #            }
    #        }
    #    r = requests.post("http://"+server+":8111/api/v1/activity", headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), timeout=self.timeout)
    #    self.assertEqual(r.status_code, 200)
    #    result = json.loads(r.text)
    #    pprint(result)
    #    # Check each value sent has been added to the object
    #    for k, v in payload['event']['data'].items():
    #        self.assertEqual(result['return']['messages']['data'][k], v)

    #def test_4_create_slice(self):
    #    payload = {
    #            "event": {
    #                "action":"CREATE",
    #                "user":"urn:publicid:IDN+onelab:upmc+user+test_auto",
    #                "object":{
    #                    "type": "SLICE",
    #                    "id": "urn:publicid:IDN+onelab:upmc:apitest+slice+s1"
    #                },
    #                "data":{
    #                    "name": "Slice number 1",
    #                    "description": "This is an automated creation of Slice number 1",
    #                    "users": ["urn:publicid:IDN+onelab:upmc+user+test_auto"]
    #                }
    #            }
    #        }
    #    r = requests.post("http://"+server+":8111/api/v1/activity", headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), timeout=self.timeout)
    #    self.assertEqual(r.status_code, 200)
    #    result = json.loads(r.text)
    #    # Check each value sent, can't check result==payload because the API is adding hrn, id and authority to the data
    #    for k, v in payload['event']['data'].items():
    #        self.assertEqual(result['return']['messages']['data'][k], v)

    def test_5_addUser_slice(self):
        payload = {
                "event": {
                    "action":"ADD",
                    "user":"urn:publicid:IDN+onelab:upmc+user+test_auto",
                    "object":{
                        "type": "SLICE",
                        "id": "urn:publicid:IDN+onelab:upmc:apitest+slice+s1"
                    },
                    "data":{
                        "type": "USER",
                        "values": ["urn:publicid:IDN+onelab:upmc+user+loic_baron"]
                    }
                }
            }
        r = requests.post("http://"+server+":8111/api/v1/activity", headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), timeout=self.timeout)
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.text)
        # Check each value sent has been added to the object
        for k, v in payload['event']['data'].items():
            self.assertEqual(result['return']['messages']['data'][k], v)

    def test_6_removeUser_slice(self):
        payload = {
                "event": {
                    "action":"REMOVE",
                    "user":"urn:publicid:IDN+onelab:upmc+user+test_auto",
                    "object":{
                        "type": "SLICE",
                        "id": "urn:publicid:IDN+onelab:upmc:apitest+slice+s1"
                    },
                    "data":{
                        "type": "USER",
                        "values": ["urn:publicid:IDN+onelab:upmc+user+loic_baron"]
                    }
                }
            }
        r = requests.post("http://"+server+":8111/api/v1/activity", headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), timeout=self.timeout)
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.text)
        # Check each value sent has been added to the object
        for k, v in payload['event']['data'].items():
            self.assertEqual(result['return']['messages']['data'][k], v)

    def test_7_addResource_slice(self):
        payload = {
                "event": {
                    "action":"ADD",
                    "user":"urn:publicid:IDN+onelab:upmc+user+test_auto",
                    "object":{
                        "type": "SLICE",
                        "id": "urn:publicid:IDN+onelab:upmc:apitest+slice+s1"
                    },
                    "data":{
                        "type": "RESOURCE",
                        "values": [{'id':self.resource}]
                    }
                }
            }
        r = requests.post("http://"+server+":8111/api/v1/activity", headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), timeout=self.timeout)
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.text)
        # Check each value sent has been added to the object
        for k, v in payload['event']['data'].items():
            self.assertEqual(result['return']['messages']['data'][k], v)

    #def test_8_removeResource_slice(self):

    #    payload = {
    #        "event": {
    #            "action": "REMOVE",
    #            "user": "urn:publicid:IDN+onelab:upmc+user+test_auto",
    #            "object": {
    #                "type": "SLICE",
    #                "id": "urn:publicid:IDN+onelab:upmc:apitest+slice+s1"
    #            },
    #            "data": {
    #                "type": "RESOURCE",
    #                "values": [{'id':self.resource}]
    #            }
    #        }
    #    }

    #    r = requests.post("http://"+server+":8111/api/v1/activity", headers={str('Content-Type'): 'application/json'},
    #                      data=json.dumps(payload), timeout=self.timeout)
    #    self.assertEqual(r.status_code, 200)
    #    result = json.loads(r.text)
    #    # Check each value sent has been added to the object
    #    for v in payload['event']['data']['values']:
    #        self.assertNotIn(v, result['return']['messages']['data']['resources'])

    #def test_9_delete_project(self):
    #    payload = {
    #            "event": {
    #                "action":"DELETE",
    #                "user":"urn:publicid:IDN+onelab:upmc+user+test_auto",
    #                "object":{
    #                    "type": "PROJECT",
    #                    "id": "urn:publicid:IDN+onelab:upmc:apitest+authority+sa"
    #                }
    #            }
    #        }
    #    r = requests.post("http://"+server+":8111/api/v1/activity", headers={str('Content-Type'):'application/json'}, data=json.dumps(payload))
    #    self.assertEqual(r.status_code, 200)
    #    result = json.loads(r.text)
    #    self.assertEqual(result['return']['messages']['object'], payload['event']['object'])

if __name__ == '__main__':
    unittest.main()
