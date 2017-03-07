#!/usr/bin/env python3.5

import json
import requests
import time
import unittest

from pprint import pprint
from random import randint

from myslice.tests import LocalTestCase
from myslice.tests.config import s, authority, server, project
from datetime import datetime

class TestSlices(LocalTestCase):

    created_slice = None

    def setUp(self):

        self.automateTest = s['automate_test']
        self.startTimer()
        self.timeout = 10

        self.cookies = s['cookies']

        r = requests.get('http://'+server+':8111/api/v1/profile', cookies=self.cookies)
        result = json.loads(r.text)
        self.user = result['result']

    def tearDown(self):
        self.stopTimer()

    def test_0_getNoAuth(self):
        r = requests.get('http://'+server+':8111/api/v1/slices')
        self.assertEqual(r.status_code, 400)

    def test_0_postNoAuth(self):
        r = requests.post('http://'+server+':8111/api/v1/slices')
        self.assertEqual(r.status_code, 400)

    def test_0_putNoAuth(self):
        r = requests.put('http://'+server+':8111/api/v1/slices')
        self.assertEqual(r.status_code, 400)

    def test_1_getAllSlices(self):
        r = requests.get('http://'+server+':8111/api/v1/slices', cookies=self.cookies)
        self.assertEqual(r.status_code, 200)

    def test_1_getUserSlices(self):
        r = requests.get('http://'+server+':8111/api/v1/users/slices', cookies=self.cookies)
        self.assertEqual(r.status_code, 200)

    def test_1_getProjectSlices(self):
        r = requests.get('http://'+server+':8111/api/v1/projects/'+project+'/slices', cookies=self.cookies)
        data = json.loads(r.text)
        print(data['result'][0])
        self.assertEqual(r.status_code, 200)

    def test_2_postWrongSlice(self):
        payload = {}
        r = requests.post('http://'+server+':8111/api/v1/slices', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), cookies=self.cookies, timeout=self.timeout)
        self.assertEqual(r.status_code, 400)

    def test_2_postSlice(self):
        tock = datetime.now()
        name = 'autotest_' + str(randint(0,10000))
        payload = {'shortname': name, 'name': name, 'project': {'id': 'urn:publicid:IDN+onelab:upmc:testradomir+authority+sa'}}
        r = requests.post('http://'+server+':8111/api/v1/slices', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), cookies=self.cookies, timeout=self.timeout)
        pprint(r.text)
        self.assertEqual(r.status_code, 200)

        result = json.loads(r.text)
        self.assertEqual(result['result'], "success")
        for event in result['events']:
            res = self.checkEvent(event)
            self.assertEqual(res['status'], "SUCCESS")
            self.__class__.created_slice = res['data']['id']
        pprint(self.__class__.created_slice)
        print(datetime.now()-tock)

    def test_3_deleteSlice(self):
        id = self.__class__.created_slice
        # id = 'urn:publicid:IDN+onelab:upmc:labthursday+slice+yep'
        if not id:
            self.assertEqual(id, "expected created_slice but got none")
        rDelete = requests.delete('http://'+server+':8111/api/v1/slices/'+id, cookies=self.cookies)
        pprint(rDelete.text)
        self.assertEqual(rDelete.status_code, 200)

        result = json.loads(rDelete.text)
        self.assertEqual(result['result'], "success")
        for event in result['events']:
            res = self.checkEvent(event)
            self.assertEqual(res['status'], "SUCCESS")

        rGet = requests.get('http://'+server+':8111/api/v1/slices/'+id, cookies=self.cookies)
        res = json.loads(rGet.text)
        slice = res['result']
        self.assertEqual(rGet.status_code, 200)
        pprint(slice)


if __name__ == '__main__':
    unittest.main()
