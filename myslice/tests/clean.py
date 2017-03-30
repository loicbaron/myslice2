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
        self.timeout = 10
        self.cookies = s['cookies']
        self.automateTest = s['automate_test']
        r = requests.get('http://'+server+':8111/api/v1/profile', cookies=self.cookies)
        result = json.loads(r.text)
        self.profile = result['result']

        r = requests.get('http://'+server+':8111/api/v1/authorities', cookies=self.cookies)
        result = json.loads(r.text)
        self.authorities = result['result']

        r = requests.get('http://'+server+':8111/api/v1/users', cookies=self.cookies)
        result = json.loads(r.text)
        self.users = result['result']

        r = requests.get('http://'+server+':8111/api/v1/projects', cookies=self.cookies)
        result = json.loads(r.text)
        self.projects = result['result']

        r = requests.get('http://'+server+':8111/api/v1/slices', cookies=self.cookies)
        result = json.loads(r.text)
        self.slices = result['result']

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

    def test_1_cleanAuthorities(self):
        """Delete authorities if the name contains autotest"""
        print("Cleaning")
        for a in self.authorities:
            if "autotest" in a['id']:
                print("deleting project %s" % a['hrn'])
                rDelete = requests.delete('http://'+server+':8111/api/v1/auhtorities/'+a['id'], cookies=self.cookies)
                pprint(rDelete.text)
                self.assertEqual(rDelete.status_code, 200)

                result = json.loads(rDelete.text)
                self.assertEqual(result['result'], "success")
                for event in result['events']:
                    res = self.checkEvent(event)
                    self.assertEqual(res['status'], "SUCCESS")

    def test_2_cleanUsers(self):
        """Delete users if the name contains autotest"""
        print("Cleaning")
        for u in self.users:
            if "autotest" in u['id']:
                print("deleting user %s" % u['hrn'])
                rDelete = requests.delete('http://'+server+':8111/api/v1/users/'+u['id'], cookies=self.cookies)
                pprint(rDelete.text)
                self.assertEqual(rDelete.status_code, 200)

                result = json.loads(rDelete.text)
                self.assertEqual(result['result'], "success")
                for event in result['events']:
                    res = self.checkEvent(event)
                    self.assertEqual(res['status'], "SUCCESS")

    def test_3_cleanProjects(self):
        """Delete projects if the name contains autotest"""
        print("Cleaning")
        for p in self.projects:
            if "autotest" in p['id']:
                print("deleting project %s" % p['hrn'])
                rDelete = requests.delete('http://'+server+':8111/api/v1/projects/'+p['id'], cookies=self.cookies)
                pprint(rDelete.text)
                self.assertEqual(rDelete.status_code, 200)

                result = json.loads(rDelete.text)
                self.assertEqual(result['result'], "success")
                for event in result['events']:
                    res = self.checkEvent(event)
                    self.assertEqual(res['status'], "SUCCESS")

    def test_4_cleanSlices(self):
        """Delete slices if the name contains autotest"""
        print("Cleaning")
        for sl in self.slices:
            if "autotest" in sl['id']:
                print("deleting slice %s" % sl['hrn'])
                rDelete = requests.delete('http://'+server+':8111/api/v1/projects/'+sl['id'], cookies=self.cookies)
                pprint(rDelete.text)
                self.assertEqual(rDelete.status_code, 200)

                result = json.loads(rDelete.text)
                self.assertEqual(result['result'], "success")
                for event in result['events']:
                    res = self.checkEvent(event)
                    self.assertEqual(res['status'], "SUCCESS")

if __name__ == '__main__':
    unittest.main()
