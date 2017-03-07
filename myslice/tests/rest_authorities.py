#!/usr/bin/env python3.5

import json
import requests
import unittest
import sys

from pprint import pprint
from random import randint

from myslice.tests import LocalTestCase
from myslice.tests.config import s, authority, server

class TestAuthority(LocalTestCase):

    created_authority = None

    def setUp(self):
        self.timeout = 10
        self.cookies = s['cookies']
        self.automateTest = s['automate_test']
        self.startTimer()

    def tearDown(self):
        self.stopTimer()

    # Open to non authenticated user get all authorities in the registration
    def test_0_getNoAuth(self):
        r = requests.get('http://'+server+':8111/api/v1/authorities')
        self.assertEqual(r.status_code, 200)

    def test_1_getAuthorities (self):
        r= requests.get('http://'+server+':8111/api/v1/authorities', cookies=self.cookies)
        self.assertEqual(r.status_code, 200)

    def test_2_postWrongAuthority(self):
        payload = {}
        r = requests.post('http://'+server+':8111/api/v1/authorities', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), cookies=self.cookies, timeout=self.timeout)
        self.assertEqual(r.status_code, 400)

    def test_3_postAuthorityNoAuth_AndDeny(self):
        name = 'autotest_' + str(randint(0, 10000))
        payload = { 'authority': name,
                    'name': 'Authotrity Auto',
                    'shortname': name,
                    'users': [{'first_name': 'Jan',
                               'last_name': 'Kowalski',
                               'password': 'Jasioqa12345',
                               'email': 'deeeb@wp.pl',
                               'terms': 'true'}],
                    'pi_users': [{'email': 'deeeb@wp.pl'}]}
        r = requests.post('http://'+server+':8111/api/v1/authorities', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), timeout=self.timeout)
        print(r.text)
        self.assertEqual(r.status_code, 200)

        result = json.loads(r.text)
        print(result)
        self.assertEqual(result['result'], "success")
        # Event status = PENDING
        print("postAuthorityNoAuth -> Denied")
        for event in result['events']:
            res = self.checkEvent(event)
            print("event: ", res)
            self.assertEqual("PENDING", res['status'])
            deny = {'action':'deny', 'message':'automated test denied this request'}
            rRequest = requests.put('http://'+server+':8111/api/v1/requests/'+event, headers={str('Content-Type'):'application/json'}, data=json.dumps(deny), cookies=self.cookies)
            self.assertEqual(rRequest.status_code, 200)

    def test_4_postAuthorityAuth(self):

        name = 'autotest_' + str(randint(0, 10000))
        payload = { 'authority': name, 'name': 'Authotrity Auto 2', 'shortname': name}
        r = requests.post('http://'+server+':8111/api/v1/authorities', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), cookies=self.cookies, timeout=self.timeout)
        print("postAuthority -> success")
        self.assertEqual(r.status_code, 200)

        result = json.loads(r.text)
        self.assertEqual(result['result'], "success")
        # Event status = SUCCESS
        for event in result['events']:
            res = self.checkEvent(event)
            self.assertEqual(res['status'], "SUCCESS")
            self.__class__.created_authority = res['data']['id']

    def test_5_deleteAuthority(self):

        id = self.__class__.created_authority

        if id:

            rDelete = requests.delete('http://' + server + ':8111/api/v1/authorities/' + id, cookies=self.cookies)

            print("deleteAuthority -> success")
            self.assertEqual(rDelete.status_code, 200)

            result = json.loads(rDelete.text)
            self.assertEqual(result['result'], "success")
            for event in result['events']:
                res = self.checkEvent(event)
                self.assertEqual(res['status'], "SUCCESS")

            rGet = requests.get('http://' + server + ':8111/api/v1/authorities/' + id, cookies=self.cookies)
            self.assertEqual(rGet.status_code, 400)
        else:
            self.assertEqual(id, "Authority was not created in previous test, we cannot continue this test")

    def test_6_postAuthorityUserNoAuth_AndApprove(self):
        name = 'autotest_' + str(randint(0, 10000))
        payload = {
           "name":"Aototest 5",
           "shortname":name,
           "authority":name,
           "domains":[
              "toto.com"
           ],
           "users":[
              {
                 "first_name":"toto2",
                 "last_name":"titi2",
                 "password":"12345678kl",
                 "email":"toto2@yopmail.com",
                 "terms":True
              }
           ],
           "pi_users":[
              {
                 "email":"toto2@yopmail.com"
              }
           ]
        }
        user_email = "toto2@yopmail.com"
        r = requests.post('http://'+server+':8111/api/v1/authorities', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), timeout=self.timeout)
        print("postAuthority with user -> approve")
        self.assertEqual(r.status_code, 200)

        result = json.loads(r.text)
        self.assertEqual(result['result'], "success")
        # Event status = PENDING
        for event in result['events']:
            res = self.checkEvent(event)
            self.assertEqual(res['status'], "PENDING")

            approve = {'action':'approve', 'message':'automated test approved this request'}
            rRequest = requests.put('http://'+server+':8111/api/v1/requests/'+event, headers={str('Content-Type'):'application/json'}, data=json.dumps(approve), cookies=self.cookies)
            self.assertEqual(rRequest.status_code, 200)
            res = self.checkEvent(event, initial_status="PENDING")
            self.__class__.created_authority = res['data']['id']
            self.assertEqual(res['status'], "SUCCESS")

        rCreated = requests.get('http://'+server+':8111/api/v1/users/'+user_email, cookies=self.cookies)
        res = json.loads(rCreated.text)
        userCreated = res['result'][0]
        self.assertEqual(rCreated.status_code, 200)
        self.assertNotEqual(len(userCreated), 0)

    def test_7_putAuthority(self):
        id = self.__class__.created_authority
        if id:
            rGet = requests.get('http://'+server+':8111/api/v1/authorities/'+id, cookies=self.cookies)
            res = json.loads(rGet.text)
            pprint(id)
            pprint(res)
            authority = res['result'][0]
            self.assertEqual(rGet.status_code, 200)

            rGetUser = requests.get('http://'+server+':8111/api/v1/users', cookies=self.cookies)
            res = json.loads(rGetUser.text)
            otherUser = res['result'][0]
            self.assertEqual(rGet.status_code, 200)

            payload = authority
            payload['pi_users'].append(otherUser['id'])
            rPut = requests.put('http://'+server+':8111/api/v1/authorities/'+id, headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), cookies=self.cookies, timeout=self.timeout)
            pprint(rPut.text)
            self.assertEqual(rPut.status_code, 200)
            result = json.loads(rPut.text)
            self.assertEqual(result['result'], "success")
            for event in result['events']:
                res = self.checkEvent(event)
                self.assertEqual(res['status'], "SUCCESS")

            rUpdated = requests.get('http://'+server+':8111/api/v1/authorities/'+id, cookies=self.cookies)
            res = json.loads(rUpdated.text)
            authorityUpdated = res['result'][0]
            self.assertEqual(rUpdated.status_code, 200)

            self.assertNotEqual(authority, authorityUpdated)
            self.assertEqual(authorityUpdated['pi_users'], payload['pi_users'])
        else:
            self.assertEqual(id, "Authority was not created in previous test, we cannot continue this test")

    def test_8_deleteAuthority(self):

        id = self.__class__.created_authority

        if id:

            rDelete = requests.delete('http://'+server+':8111/api/v1/authorities/'+id, cookies=self.cookies)

            print("deleteAuthority -> success")
            self.assertEqual(rDelete.status_code, 200)

            result = json.loads(rDelete.text)
            self.assertEqual(result['result'], "success")
            for event in result['events']:
                res = self.checkEvent(event)
                self.assertEqual(res['status'], "SUCCESS")

            rGet = requests.get('http://'+server+':8111/api/v1/authorities/'+id, cookies=self.cookies)
            self.assertEqual(rGet.status_code, 400)
        else:
            self.assertEqual(id, "Authority was not created in previous test, we cannot continue this test")



if __name__ == '__main__':
    unittest.main()
