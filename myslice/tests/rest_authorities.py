#!/usr/bin/env python3.5

import json
import requests
import unittest

from pprint import pprint

from myslice.tests import Tests
from myslice.tests.config import s, rootAuthority

class TestAuthority(Tests):

    created_authority = None

    def setUp(self):
        self.timeout = 10
        self.cookies = s['cookies']

    # Open to non authenticated user get all authorities in the registration
    def test_0_getNoAuth(self):
        r = requests.get('http://localhost:8111/api/v1/authorities')
        self.assertEqual(r.status_code, 200)

    def test_0_getAuthorities (self):
        r= requests.get('http://localhost:8111/api/v1/authorities', cookies=self.cookies)
        self.assertEqual(r.status_code, 200)

    def test_1_postWrongAuthority(self):
        payload = {}
        r = requests.post('http://localhost:8111/api/v1/authorities', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), cookies=self.cookies, timeout=self.timeout)
        pprint(r.text)
        self.assertEqual(r.status_code, 400)

    def test_2_postAuthority(self):
        payload = { 'authority': rootAuthority, 'name': 'Authotrity Auto', 'shortname': 'auto_auth'}
        r = requests.post('http://localhost:8111/api/v1/authorities', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), cookies=self.cookies, timeout=self.timeout)
        pprint(r.text)
        self.assertEqual(r.status_code, 200)

        result = json.loads(r.text)
        self.assertEqual(result['result'], "success")
        # Event status = PENDING
        pprint(r.text)
        for event in result['events']:
            res = self.checkEvent(event)
            self.assertEqual(res['status'], "SUCCESS")
            self.__class__.created_authority = res['data']['id']
        pprint(self.__class__.created_authority)

#PUT

#DELETE

if __name__ == '__main__':
    unittest.main()
