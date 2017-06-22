#!/usr/bin/env python3.5

import json
import requests
import time
import unittest

from pprint import pprint
from random import randint

from myslice.tests import LocalTestCase
from myslice.tests.config import s, authority, project
from datetime import datetime

class TestSlices(LocalTestCase):

    created_slice = None
    project = None
    testbeds = None
    testbedsLeases = None

    def setUp(self):

        self.automateTest = s['automate_test']
        self.startTimer()
        self.timeout = 10

        self.cookies = s['cookies']

        r = requests.get('http://'+self.server+':8111/api/v1/profile', cookies=self.cookies)
        result = json.loads(r.text)
        self.user = result['result']

    def tearDown(self):
        self.stopTimer()

    def test_0_getNoAuth(self):
        r = requests.get('http://'+self.server+':8111/api/v1/slices')
        self.assertEqual(r.status_code, 400)

    def test_0_postNoAuth(self):
        r = requests.post('http://'+self.server+':8111/api/v1/slices')
        self.assertEqual(r.status_code, 400)

    def test_0_putNoAuth(self):
        r = requests.put('http://'+self.server+':8111/api/v1/slices')
        self.assertEqual(r.status_code, 400)

    def test_1_getAllSlices(self):
        r = requests.get('http://'+self.server+':8111/api/v1/slices', cookies=self.cookies)
        self.assertEqual(r.status_code, 200)

    def test_1_getUserSlices(self):
        r = requests.get('http://'+self.server+':8111/api/v1/users/slices', cookies=self.cookies)
        self.assertEqual(r.status_code, 200)

    def test_1_getProjectSlices(self):
        project = self.getProjectId()
        print("project = %s" % project)
        self.assertNotEqual(project, None)
        r = requests.get('http://'+self.server+':8111/api/v1/projects/'+project+'/slices', cookies=self.cookies)
        data = json.loads(r.text)
        # print(data['result'][0])
        self.assertEqual(r.status_code, 200)

        self.__class__.project = project
        print("project = %s" % self.__class__.project)

    def test_2_postWrongSlice(self):
        payload = {}
        r = requests.post('http://'+self.server+':8111/api/v1/slices', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), cookies=self.cookies, timeout=self.timeout)
        self.assertEqual(r.status_code, 400)
    def test_2_postSlice(self):
        tock = datetime.now()
        name = 'autotest_' + str(randint(0,10000))
        project = self.__class__.project
        payload = {'shortname': name, 'name': name, 'project': {'id': project}}
        r = requests.post('http://'+self.server+':8111/api/v1/slices', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), cookies=self.cookies, timeout=self.timeout)
        pprint(r.text)
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.text)
        self.assertEqual(result['result'], "success")
        for event in result['events']:
            res = self.checkEvent(event)
            self.assertEqual(res['status'], "SUCCESS")
            self.__class__.created_slice = res['data']['id']
        pprint(self.__class__.created_slice)
        #print(datetime.now()-tock)
    def test_3_getSliceId(self):
        id = self.__class__.created_slice
        if not id:
            self.assertEqual(id, "expected created_slice but got none")
        rGet = requests.get('http://'+self.server+':8111/api/v1/slices/'+id, cookies=self.cookies)
        self.assertEqual(rGet.status_code, 200)
        slices = json.loads(rGet.text)['result']
        self.assertGreater(len(slices),0)

    def test_4_putSliceUser(self):
        id = self.__class__.created_slice
        if not id:
            self.assertEqual(id, "expected created_slice but got none")
        rGet = requests.get('http://'+self.server+':8111/api/v1/slices/'+id, cookies=self.cookies)
        self.assertEqual(rGet.status_code, 200)
        slice = json.loads(rGet.text)['result'][0]

        r = requests.get('http://'+self.server+':8111/api/v1/users', cookies=self.cookies)
        self.assertEqual(r.status_code, 200)
        users = json.loads(r.text)['result']
        self.assertGreater(len(users),0)

        slice['users'] = [x['id'] for x in slice['users']]
        slice['users'].append(users[0]['id'])

        rPut = requests.put('http://'+self.server+':8111/api/v1/slices/'+id, headers={str('Content-Type'):'application/json'}, data=json.dumps(slice), cookies=self.cookies, timeout=self.timeout)
        pprint(rPut.text)
        self.assertEqual(rPut.status_code, 200)
        result = json.loads(rPut.text)
        self.assertEqual(result['result'], "success")
        for event in result['events']:
            res = self.checkEvent(event)
            self.assertEqual(res['status'], "SUCCESS")

        rUpdated = requests.get('http://'+self.server+':8111/api/v1/slices/'+id, cookies=self.cookies)
        self.assertEqual(rUpdated.status_code, 200)
        sliceUpdated = json.loads(rUpdated.text)['result'][0]

        self.assertNotEqual(slice, sliceUpdated)
        self.assertCountEqual([x['id'] for x in sliceUpdated['users']], slice['users'])

    def test_5_getTestbeds(self):
        r = requests.get('http://'+self.server+':8111/api/v1/testbeds', cookies=self.cookies)
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.text)
        testbeds = []
        testbedsLeases = []
        for t in data['result']:
            if t['hasLeases']:
                testbedsLeases.append(t['id'])
            else:
                testbeds.append(t['id'])
        self.__class__.testbedsLeases = testbedsLeases
        self.__class__.testbeds = testbeds

    #def test_6_putSliceResources(self):
    #    id = self.__class__.created_slice
    #    if not id:
    #        self.assertEqual(id, "expected created_slice but got none")
    #    rGet = requests.get('http://'+self.server+':8111/api/v1/slices/'+id, cookies=self.cookies)
    #    self.assertEqual(rGet.status_code, 200)
    #    slice = json.loads(rGet.text)['result'][0]

    #    testbeds = self.__class__.testbeds
    #    if not testbeds:
    #        self.assertEqual(testbeds, "List of testbeds was not set, can't continue this test")
    #    r = requests.get('http://'+self.server+':8111/api/v1/testbeds/'+testbeds[0]+'/resources', cookies=self.cookies)
    #    self.assertEqual(r.status_code, 200)
    #    resources = json.loads(r.text)['result']
    #    self.assertGreater(len(resources),0)

    #    slice['resources'].append(resources[0]['id'])
    #    slice['resources'].append(resources[1]['id'])

    #    rPut = requests.put('http://'+self.server+':8111/api/v1/slices/'+id, headers={str('Content-Type'):'application/json'}, data=json.dumps(slice), cookies=self.cookies, timeout=self.timeout)
    #    pprint(rPut.text)
    #    self.assertEqual(rPut.status_code, 200)
    #    result = json.loads(rPut.text)
    #    self.assertEqual(result['result'], "success")
    #    for event in result['events']:
    #        res = self.checkEvent(event)
    #        self.assertEqual(res['status'], "SUCCESS")

    #    rUpdated = requests.get('http://'+self.server+':8111/api/v1/slices/'+id, cookies=self.cookies)
    #    self.assertEqual(rUpdated.status_code, 200)
    #    sliceUpdated = json.loads(rUpdated.text)['result'][0]

    #    self.assertNotEqual(slice, sliceUpdated)
    #    self.assertEqual([x['id'] for x in sliceUpdated['resources']], slice['resources'])

    def test_7_deleteSlice(self):
        id = self.__class__.created_slice
        pprint(id)
        if not id:
            self.assertEqual(id, "expected created_slice but got none")
        rDelete = requests.delete('http://'+self.server+':8111/api/v1/slices/'+id, cookies=self.cookies)
        pprint(rDelete.text)
        self.assertEqual(rDelete.status_code, 200)

        result = json.loads(rDelete.text)
        self.assertEqual(result['result'], "success")
        for event in result['events']:
            res = self.checkEvent(event)
            self.assertEqual(res['status'], "SUCCESS")

        rGet = requests.get('http://'+self.server+':8111/api/v1/slices/'+id, cookies=self.cookies)
        res = json.loads(rGet.text)
        slice = res['result']
        pprint(slice)
        self.assertEqual(rGet.status_code, 200)


if __name__ == '__main__':
    unittest.main()
