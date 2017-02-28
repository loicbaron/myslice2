#!/usr/bin/env python3.5

import json
import requests
import sys
import unittest

from pprint import pprint

from myslice.tests.config import s, server

class TestLogin(unittest.TestCase):

    def setUp(self):
        self.timeout = 10
        self.cookies = s['cookies']

    def test_0_noAuth(self):
        """Check if unauth user can get profile data"""
        r = requests.get('http://'+server+':8111/api/v1/profile')
        self.assertEqual(r.status_code, 400)

    def test_1_auth_to_get_cookie(self):
        """Log in and check if we recive any cookie"""

        payload = {'email': s['email'], 'password': s['password']}
        r = requests.post("http://"+server+":8111/api/v1/login",
                          headers={str('Content-Type'):'application/json'},
                          data=json.dumps(payload),
                          timeout=self.timeout)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(hasattr(r, 'cookies'))
        self.assertIsNotNone(r.cookies)
        if r.cookies is not None:
            self.cookies = r.cookies

    def test_2_get_profile_with_cookie(self):
        """Takes cookie from test 1 and check if we can get users profile hrn"""
        r = requests.get("http://"+server+":8111/api/v1/profile", cookies=self.cookies)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(s['hrn'], json.loads(r.text)['result']['hrn'])

