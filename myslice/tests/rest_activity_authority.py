#!/usr/bin/env python3.5

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

    def test_0_invalidRequest(self):
        payload = {'key1': 'value1', 'key2': 'value2'}
        r = requests.post("http://localhost:8111/api/v1/activity", data=payload, timeout=self.timeout)
        self.assertEqual(r.status_code, 400)

    def test_1_create_authority_fail(self):
        payload = {
                "event": {
                    "action":"CREATE",
                    "user":"urn:publicid:IDN+onelab:upmc+user+",
                    "object":{
                        "type": "AUTHORITY",
                        "id": "urn:publicid:IDN+onelab:test_authority+authority+sa"
                    },
                    "data":{
                        "name": "Test Autority",
                        "pi_users": ["urn:publicid:IDN+onelab:upmc+user+loic_baron"]
                    }
                }
            }
        r = requests.post("http://localhost:8111/api/v1/activity", headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), timeout=self.timeout)
        self.assertEqual(r.status_code, 500)

    def test_2_create_authority(self):
        payload = {
                "event": {
                    "action":"CREATE",
                    "user":"urn:publicid:IDN+onelab:upmc+user+loic_baron",
                    "object":{
                        "type": "AUTHORITY",
                        "id": "urn:publicid:IDN+onelab:test_authority+authority+sa"
                    },
                    "data":{
                        "name": "Test Autority",
                        "pi_users": ["urn:publicid:IDN+onelab:upmc+user+loic_baron"]
                    }
                }
            }
        r = requests.post("http://localhost:8111/api/v1/activity", headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), timeout=self.timeout)
        result = json.loads(r.text)
        #pprint(result)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['return']['messages']['object'], payload['event']['object'])
        # Check each value sent, can't check result==payload because the API is adding hrn, id and authority to the data
        for k,v in payload['event']['data'].items():
            self.assertEqual(result['return']['messages']['data'][k], v)

    def test_3_update_authority(self):
        payload = {
                "event": {
                    "action":"UPDATE",
                    "user":"urn:publicid:IDN+onelab:upmc+user+loic_baron",
                    "object":{
                        "type": "AUTHORITY",
                        "id": "urn:publicid:IDN+onelab:test_authority+authority+sa"
                    },
                    "data":{
                        "name": "Test Autority Updated",
                        "pi_users": ["urn:publicid:IDN+onelab:upmc+user+loic_baron","urn:publicid:IDN+onelab:upmc+user+radomir_klacza"]
                    }
                }
            }
        r = requests.post("http://localhost:8111/api/v1/activity", headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), timeout=self.timeout)
        result = json.loads(r.text)
        #pprint(result)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['return']['messages']['object'], payload['event']['object'])
        # Check each value sent, can't check result==payload because the API is adding hrn, id and authority to the data
        for k,v in payload['event']['data'].items():
            self.assertEqual(result['return']['messages']['data'][k], v)

    def test_4_add_pi_authority(self):
        payload = {
                "event": {
                    "action":"ADD",
                    "user":"urn:publicid:IDN+onelab:upmc+user+loic_baron",
                    "object":{
                        "type": "AUTHORITY",
                        "id": "urn:publicid:IDN+onelab:test_authority+authority+sa"
                    },
                    "data":{
                        "type": "PI",
                        "values": ["urn:publicid:IDN+onelab:upmc+user+ciro_scognamiglio"]
                    }
                }
            }
        r = requests.post("http://localhost:8111/api/v1/activity", headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), timeout=self.timeout)
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.text)
        self.assertEqual(result['return']['messages']['object'], payload['event']['object'])
        # Check each value sent, can't check result==payload because the API is adding hrn, id and authority to the data
        for k,v in payload['event']['data'].items():
            self.assertEqual(result['return']['messages']['data'][k], v)

    def test_5_remove_pi_authority(self):
        payload = {
                "event": {
                    "action":"REMOVE",
                    "user":"urn:publicid:IDN+onelab:upmc+user+loic_baron",
                    "object":{
                        "type": "AUTHORITY",
                        "id": "urn:publicid:IDN+onelab:test_authority+authority+sa"
                    },
                    "data":{
                        "type": "PI",
                        "values": ["urn:publicid:IDN+onelab:upmc+user+ciro_scognamiglio"]
                    }
                }
            }
        r = requests.post("http://localhost:8111/api/v1/activity", headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), timeout=self.timeout)
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.text)
        self.assertEqual(result['return']['messages']['object'], payload['event']['object'])
        # Check each value sent, can't check result==payload because the API is adding hrn, id and authority to the data
        for k,v in payload['event']['data'].items():
            self.assertEqual(result['return']['messages']['data'][k], v)

    def test_6_delete_authority(self):
        payload = {
                "event": {
                    "action":"DELETE",
                    "user":"urn:publicid:IDN+onelab:upmc+user+loic_baron",
                    "object":{
                        "type": "AUTHORITY",
                        "id": "urn:publicid:IDN+onelab:test_authority+authority+sa"
                    }
                }
            }
        r = requests.post("http://localhost:8111/api/v1/activity", headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), timeout=self.timeout)
        result = json.loads(r.text)
        #pprint(result)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['return']['messages']['object'], payload['event']['object'])

if __name__ == '__main__':
    unittest.main()
