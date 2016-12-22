#!/usr/bin/env python3.5

import json
import requests
import sys
import unittest

from pprint import pprint

from tests import s

class TestAuth(unittest.TestCase):

    def setUp(self):
        self.timeout = 10
        self.cookies = s['cookies']

    def test_0_noAuth(self):
        r = requests.get('http://localhost:8111/api/v1/profile')
        # user not authenticated
        self.assertEqual(r.status_code, 400)

    def test_1_cookies(self):
        payload = {'email': s['email'], 'password': s['password']}
        r = requests.post("http://localhost:8111/api/v1/login", headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), timeout=self.timeout)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(hasattr(r, 'cookies'))
        self.assertIsNotNone(r.cookies)

    def test_2_auth(self):
        r = requests.get('http://localhost:8111/api/v1/profile', cookies=self.cookies)
        self.assertEqual(r.status_code, 200)

if __name__ == '__main__':
    unittest.main()
