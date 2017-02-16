#!/usr/bin/env python3.5

import json
import requests
import sys
import time
import unittest

from pprint import pprint

from myslice.tests import Tests
from myslice.tests.config import s, server, authority

class TestUsers(Tests):

    created_user = None

    def setUp(self):
        self.timeout = 10
        self.cookies = s['cookies']

    def test_0_getNoAuth(self):
        r = requests.get('http://'+server+':8111/api/v1/users')
        # user not authenticated
        #pprint(r.text)
        self.assertEqual(r.status_code, 400)

    def test_0_postNoAuth(self):
        r = requests.post('http://'+server+':8111/api/v1/users')
        # user not authenticated
        #pprint(r.text)
        self.assertEqual(r.status_code, 400)

    def test_0_putNoAuth(self):
        r = requests.put('http://'+server+':8111/api/v1/users')
        # user not authenticated
        #pprint(r.text)
        self.assertEqual(r.status_code, 400)


    def test_1_getUsers(self):
        r = requests.get('http://'+server+':8111/api/v1/users', cookies=self.cookies)
        #pprint(r.text)
        self.assertEqual(r.status_code, 200)

    def test_2_postWrongUser(self):
        payload = {}
        r = requests.post('http://'+server+':8111/api/v1/users', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), cookies=self.cookies, timeout=self.timeout)
        #pprint(r.text)
        self.assertEqual(r.status_code, 500)

    def test_2_postUserNoAuth(self):
        payload = { 'authority': authority, 'first_name': 'auto', 'last_name': 'test', 'email': 'onelabautotest1@yopmail.com', 'password': '12341234', 'terms': True }
        r = requests.post('http://'+server+':8111/api/v1/users', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), timeout=self.timeout)
        self.assertEqual(r.status_code, 200)

        result = json.loads(r.text)
        self.assertEqual(result['result'], "success")
        # Event status = PENDING
        pprint(r.text)
        for event in result['events']:
            res = self.checkEvent(event)
            self.assertEqual(res['status'], "PENDING")

            deny = {'action':'deny', 'message':'automated test denied this request'}
            rRequest = requests.put('http://'+server+':8111/api/v1/requests/'+event, headers={str('Content-Type'):'application/json'}, data=json.dumps(deny), cookies=self.cookies)
            self.assertEqual(rRequest.status_code, 200)

    def test_2_postUser(self):

        payload = { 'authority': authority, 'first_name': 'auto', 'last_name': 'test', 'email': 'onelabautotest2@yopmail.com', 'password': '12341234', 'terms': True }
        r = requests.post('http://'+server+':8111/api/v1/users', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), cookies=self.cookies, timeout=self.timeout)
        self.assertEqual(r.status_code, 200)
        # Event status = SUCCESS
        pprint(r.text)
        result = json.loads(r.text)
        self.assertEqual(result['result'], "success")
        for event in result['events']:
            res = self.checkEvent(event)
            self.assertEqual(res['status'], "SUCCESS")
            self.__class__.created_user = res['data']['id']
        pprint(self.__class__.created_user)

    def test_3_getUserId(self):
        id = self.__class__.created_user
        print(id)
        r = requests.get('http://'+server+':8111/api/v1/users/'+id, cookies=self.cookies)
        #pprint(r.text)
        self.assertEqual(r.status_code, 200)

    def test_4_putUser(self):
        id = self.__class__.created_user
        rGet = requests.get('http://'+server+':8111/api/v1/users/'+id, cookies=self.cookies)
        res = json.loads(rGet.text)
        user = res['result'][0]
        self.assertEqual(rGet.status_code, 200)

        payload = user
        payload['first_name'] = "toto"
        rPut = requests.put('http://'+server+':8111/api/v1/users/'+id, headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), cookies=self.cookies, timeout=self.timeout)
        pprint(rPut.text)
        self.assertEqual(rPut.status_code, 200)
        result = json.loads(rPut.text)
        self.assertEqual(result['result'], "success")
        for event in result['events']:
            res = self.checkEvent(event)
            self.assertEqual(res['status'], "SUCCESS")

        rUpdated = requests.get('http://'+server+':8111/api/v1/users/'+id, cookies=self.cookies)
        res = json.loads(rUpdated.text)
        userUpdated = res['result'][0]
        self.assertEqual(rUpdated.status_code, 200)

        self.assertNotEqual(user, userUpdated)
        self.assertEqual(userUpdated['first_name'], payload['first_name'])

    def test_5_deleteUser(self):
        id = self.__class__.created_user
        rDelete = requests.delete('http://'+server+':8111/api/v1/users/'+id, cookies=self.cookies)
        pprint(rDelete.text)
        self.assertEqual(rDelete.status_code, 200)

        result = json.loads(rDelete.text)
        self.assertEqual(result['result'], "success")
        for event in result['events']:
            res = self.checkEvent(event)
            self.assertEqual(res['status'], "SUCCESS")

        rGet = requests.get('http://'+server+':8111/api/v1/users/'+id, cookies=self.cookies)
        res = json.loads(rGet.text)
        user = res['result']
        self.assertEqual(rGet.status_code, 200)
        pprint(user)
        #self.assertEqual(len(user), 0)

if __name__ == '__main__':
    unittest.main()
