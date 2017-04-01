#!/usr/bin/env python3.5

import json
import requests
import unittest

from pprint import pprint
from random import randint

from myslice.tests import LocalTestCase
from myslice.tests.config import s, server, authority

class TestUsers(LocalTestCase):

    created_user = None

    def setUp(self):
        self.timeout = 10
        self.cookies = s['cookies']
        self.automateTest = s['automate_test']
        self.startTimer()

    def tearDown(self):
        self.stopTimer()

    def test_0_getNoAuth(self):
        r = requests.get('http://'+server+':8111/api/v1/users')
        self.assertEqual(r.status_code, 400)

    def test_0_postNoAuth(self):
        r = requests.post('http://'+server+':8111/api/v1/users')
        self.assertEqual(r.status_code, 400)

    def test_0_putNoAuth(self):
        r = requests.put('http://'+server+':8111/api/v1/users')
        self.assertEqual(r.status_code, 400)


    def test_1_getUsers(self):
        r = requests.get('http://'+server+':8111/api/v1/users', cookies=self.cookies)
        self.assertEqual(r.status_code, 200)

    def test_2_postWrongUser(self):
        payload = {}
        r = requests.post('http://'+server+':8111/api/v1/users', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), cookies=self.cookies, timeout=self.timeout)
        self.assertEqual(r.status_code, 400)

    def test_3_postUserNoAuth(self):
        email = "onelab_autotest_"+str(randint(0,10000))+"@yopmail.com"
        payload = { 'authority': authority, 'first_name': 'radomir', 'last_name': 'autotest', 'email': email, 'password': '12341234', 'terms': True }
        r = requests.post('http://'+server+':8111/api/v1/users', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), timeout=self.timeout)
        pprint(r.text)
        if r.status_code == 400:
            res = json.loads(r.text)
            if "error" in res and "already registered" in res['error']:
                print("Please clean up records from previously run tests using clean.py")
        self.assertEqual(r.status_code, 200)

        result = json.loads(r.text)
        self.assertEqual(result['result'], "success")
        # Event status = PENDING
        for event in result['events']:
            res = self.checkEvent(event)
            self.assertEqual(res['status'], "CONFIRM")

            rConfirm = requests.get('http://'+server+':8111/confirm/'+event)
            self.assertEqual(rConfirm.status_code, 200)

            res = self.checkEvent(event, initial_status="CONFIRM")
            self.assertEqual(res['status'], "PENDING")

            # TODO: CONFIRM you received the email
            #sender = "zhouquantest16@gmail.com"
            #to = "onelabautotest1@yopmail.com"
            #obj = "Confirm your email"
            #search = '(?:href=[\'"])([:/.A-z?<_&\s=>0-9;-]+)'
            #event = self.checkEmail(search, sender, obj)

            deny = {'action':'deny', 'message':'automated test denied this request'}
            print(json.dumps(deny))
            rRequest = requests.put('http://'+server+':8111/api/v1/requests/'+event, headers={str('Content-Type'):'application/json'}, data=json.dumps(deny), cookies=self.cookies)
            print(rRequest.text)
            self.assertEqual(rRequest.status_code, 200)

    def test_4_postUser(self):
        email = "onelab_autotest_"+str(randint(0,10000))+"@yopmail.com"
        payload = { 'authority': authority, 'first_name': 'auto', 'last_name': 'test', 'email': email, 'password': '12341234', 'terms': True }
        r = requests.post('http://'+server+':8111/api/v1/users', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), cookies=self.cookies, timeout=self.timeout)
        pprint(r.text)
        if r.status_code == 400:
            res = json.loads(r.text)
            if "error" in res and "already registered" in res['error']:
                print("Please clean up records from previously run tests using clean.py")
        self.assertEqual(r.status_code, 200)
        # Event status = SUCCESS
        pprint(r.text)
        result = json.loads(r.text)
        self.assertEqual(result['result'], "success")
        for event in result['events']:
            res = self.checkEvent(event)
            self.assertEqual(res['status'], "SUCCESS")
            self.__class__.created_user = res['data']['id']
        print('created user:', self.__class__.created_user)

    def test_5_getUserId(self):
        id = self.__class__.created_user
        if id:
            r = requests.get('http://'+server+':8111/api/v1/users/'+id, cookies=self.cookies)
            self.assertEqual(r.status_code, 200)
            res = json.loads(r.text)
            self.assertGreater(len(res['result']),0)
            user = res['result'][0]
            self.assertEqual(user['id'], id)
        else:
            self.assertEqual(id, "User was not created in previous test, we cannot continue this test")

    def test_6_putUser(self):
        id = self.__class__.created_user
        if id:
            rGet = requests.get('http://'+server+':8111/api/v1/users/'+id, cookies=self.cookies)
            self.assertEqual(rGet.status_code, 200)
            res = json.loads(rGet.text)
            self.assertGreater(len(res['result']),0)
            user = res['result'][0]
            self.assertEqual(user['id'], id)

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
        else:
            self.assertEqual(id, "User was not created in previous test, we cannot continue this test")

    def test_7_deleteUser(self):
        id = self.__class__.created_user
        if id:

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
        else:
            self.assertEqual(id, "User was not created in previous test, we cannot continue this test")

if __name__ == '__main__':
    unittest.main()
