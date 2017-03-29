#!/usr/bin/env python3.5

import json
import requests
import sys
import unittest
from datetime import datetime
from pprint import pprint
from myslice.tests import LocalTestCase
from myslice.tests.config import s, server

class CleanUp(LocalTestCase):

    def setUp(self):
        self.automateTest = s['automate_test']
        self.timeout = 10
        self.cookies = s['cookies']
        r = requests.get('http://'+server+':8111/api/v1/profile', cookies=self.cookies)
        result = json.loads(r.text)
        self.profile = result['result']

        self.startTimer()

    def tearDown(self):
        # self.tock = datetime.now()
        # diff = self.tock - self.tick
        # print((diff.microseconds / 1000), "ms")
        self.stopTimer()

    def test_0_auth_to_get_cookie(self):
        """Log in and check if we recive any cookie"""
        payload = {'email': s['email'], 'password': s['password']}
        r = requests.post("http://"+server+":8111/api/v1/login",
                          headers={str('Content-Type'):'application/json'},
                          data=json.dumps(payload),
                          timeout=self.timeout)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(hasattr(r, 'cookies'))
        self.assertIsNotNone(r.cookies)

    def test_1_cleanProjects(self):
        """Delete projects if the name contains auto"""
        print("Cleaning")
        pprint(self.profile)
        for p in self.profile['projects']:
            if "autotest" in p['name']:
                print("deleting project %s" % p['hrn'])
                rDelete = requests.delete('http://'+server+':8111/api/v1/projects/'+p['id'], cookies=self.cookies)
                pprint(rDelete.text)
                self.assertEqual(rDelete.status_code, 200)

                result = json.loads(rDelete.text)
                self.assertEqual(result['result'], "success")
                for event in result['events']:
                    res = self.checkEvent(event)
                    self.assertEqual(res['status'], "SUCCESS")

if __name__ == '__main__':
    unittest.main()
