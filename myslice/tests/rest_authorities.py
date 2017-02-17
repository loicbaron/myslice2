#!/usr/bin/env python3.5

import json
import requests
import unittest
import sys

from pprint import pprint

from myslice.tests import Tests
from myslice.tests.config import s, authority, server

class TestAuthority(Tests):

    created_authority = None

    def setUp(self):
        self.timeout = 10
        self.cookies = s['cookies']
        try:
            payload = {'email': s['email'], 'password': s['password']}
            r = requests.post("http://" + server + ":8111/api/v1/login",
                              headers={str('Content-Type'): 'application/json'},
                              data=json.dumps(payload))
            self.cookies = r.cookies
        except:
            self.cookies = None

    # Open to non authenticated user get all authorities in the registration
    def test_0_getNoAuth(self):
        r = requests.get('http://'+server+':8111/api/v1/authorities')
        self.assertEqual(r.status_code, 200)

    def test_0_getAuthorities (self):
        print("cookies: ", self.cookies)
        r= requests.get('http://'+server+':8111/api/v1/authorities', cookies=self.cookies)
        self.assertEqual(r.status_code, 200)

    def test_1_postWrongAuthority(self):
        payload = {}
        r = requests.post('http://'+server+':8111/api/v1/authorities', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), cookies=self.cookies, timeout=self.timeout)
        self.assertEqual(r.status_code, 400)

    def test_2_postAuthorityNoAuth(self):
        payload = { 'authority': authority,
                    'name': 'Authotrity Auto',
                    'shortname': 'auto_auth',
                    'users': [{'first_name': 'Jan',
                               'last_name': 'Kowalski',
                               'password': 'Jasioqa',
                               'email': 'deeeb@wp.pl',
                               'terms': 'true'}],
                    'pi_users': [{'email': 'deeeb@wp.pl'}]}
        r = requests.post('http://'+server+':8111/api/v1/authorities', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), timeout=self.timeout)
        self.assertEqual(r.status_code, 200)

        result = json.loads(r.text)
        print(result)
        self.assertEqual(result['result'], "success")
        # Event status = PENDING
        print("postAuthorityNoAuth -> Denied")
        for event in result['events']:
            res = self.checkEvent(event)
            print("event: ", res)
            self.assertEqual(res['status'], "PENDING")

            deny = {'action':'deny', 'message':'automated test denied this request'}
            rRequest = requests.put('http://'+server+':8111/api/v1/requests/'+event, headers={str('Content-Type'):'application/json'}, data=json.dumps(deny), cookies=self.cookies)
            self.assertEqual(rRequest.status_code, 200)

    def test_3_postAuthority(self):
        payload = { 'authority': authority, 'name': 'Authotrity Auto 2', 'shortname': 'auto_auth2'}
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

    def test_4_deleteAuthority(self):

        id = self.__class__.created_authority

        if not id:
            self.assertEqual(id = "Authority was not created in previous test, we cannot continue this test")
            sys.exit()

        rDelete = requests.delete('http://'+server+':8111/api/v1/authorities/'+id, cookies=self.cookies)

        print("deleteAuthority -> success")
        self.assertEqual(rDelete.status_code, 200)

        result = json.loads(rDelete.text)
        self.assertEqual(result['result'], "success")
        for event in result['events']:
            res = self.checkEvent(event)
            self.assertEqual(res['status'], "SUCCESS")

        rGet = requests.get('http://'+server+':8111/api/v1/authorities/'+id, cookies=self.cookies)
        res = json.loads(rGet.text)
        self.assertEqual(rGet.status_code, 400)

    def test_5_postAuthorityUserNoAuth(self):
        payload = {
           "name":"toto2",
           "shortname":"t2",
           "authority":authority,
           "domains":[
              "toto.com"
           ],
           "users":[
              {
                 "first_name":"toto2",
                 "last_name":"titi2",
                 "password":"12345678",
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
#PUT
    def test_6_putAuthority(self):
        id = self.__class__.created_authority
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

#DELETE
    def test_7_deleteAuthority(self):
        id = self.__class__.created_authority
        rDelete = requests.delete('http://'+server+':8111/api/v1/authorities/'+id, cookies=self.cookies)
        self.assertEqual(rDelete.status_code, 200)

        result = json.loads(rDelete.text)
        self.assertEqual(result['result'], "success")
        for event in result['events']:
            res = self.checkEvent(event)
            self.assertEqual(res['status'], "SUCCESS")

        rGet = requests.get('http://'+server+':8111/api/v1/authorities/'+id, cookies=self.cookies)
        res = json.loads(rGet.text)
        pprint(res)
        self.assertEqual(rGet.status_code, 400)

if __name__ == '__main__':
    unittest.main()
