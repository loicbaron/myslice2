#!/usr/bin/env python3.5

import json
import requests
import time
import unittest

from pprint import pprint
from random import randint

from myslice.tests import LocalTestCase
from myslice.tests.config import s, authority, server
from datetime import datetime

class TestProjects(LocalTestCase):

    created_project = None

    def setUp(self):

        self.automateTest = s['automate_test']
        self.startTimer()
        self.timeout = 10

        self.cookies = s['cookies']

        r = requests.get('http://'+server+':8111/api/v1/profile', cookies=self.cookies)
        result = json.loads(r.text)
        self.user = result['result']

    def tearDown(self):
        # self.tock = datetime.now()
        # diff = self.tock - self.tick
        # print((diff.microseconds / 1000), "ms")
        self.stopTimer()

    def test_0_getNoAuth(self):
        r = requests.get('http://'+server+':8111/api/v1/projects')
        self.assertEqual(r.status_code, 400)

    def test_0_postNoAuth(self):
        r = requests.post('http://'+server+':8111/api/v1/projects')
        self.assertEqual(r.status_code, 400)

    def test_0_putNoAuth(self):
        r = requests.put('http://'+server+':8111/api/v1/projects')
        self.assertEqual(r.status_code, 400)

    def test_1_getProjects(self):
        r = requests.get('http://'+server+':8111/api/v1/projects', cookies=self.cookies)
        self.assertEqual(r.status_code, 200)


    def test_2_postWrongProject(self):
        payload = {}
        r = requests.post('http://'+server+':8111/api/v1/projects', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), cookies=self.cookies, timeout=self.timeout)
        self.assertEqual(r.status_code, 400)
        res = json.loads(r.text)
        self.assertEqual("Project name must be specified", res['error'])


    # TODO: SimpleUser Request New Project

    #def test_2_postProjectSimpleUser(self):
    #    payload = { 'authority': authority, 'name': 'project_auto', 'description': 'this is an automated project', 'pi_users':[self.user['id']] }
    #    r = requests.post('http://'+server+':8111/api/v1/projects', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), timeout=self.timeout)
    #    self.assertEqual(r.status_code, 200)

    #    result = json.loads(r.text)
    #    self.assertEqual(result['result'], "success")
    #    # Event status = PENDING
    #    pprint(r.text)
    #    for event in result['events']:
    #        res = self.checkEvent(event)
    #        self.assertEqual(res['status'], "PENDING")

    #        deny = {'action':'deny', 'message':'automated test denied this request'}
    #        rRequest = requests.put('http://'+server+':8111/api/v1/requests/'+event, headers={str('Content-Type'):'application/json'}, data=json.dumps(deny), cookies=self.cookies)
    #        self.assertEqual(rRequest.status_code, 200)

    def test_2_postProject(self):
        tock = datetime.now()
        name = 'autotest_' + str(randint(0,10000))
        payload = {'authority': {"id": authority}, 'name': name, 'description': 'this is an automated project', 'pi_users':[self.user['id']] }
        r = requests.post('http://'+server+':8111/api/v1/projects', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), cookies=self.cookies, timeout=self.timeout)
        self.assertEqual(r.status_code, 200)
        # Event status = SUCCESS
        pprint(r.text)
        result = json.loads(r.text)
        self.assertEqual(result['result'], "success")
        for event in result['events']:
            res = self.checkEvent(event)
            self.assertEqual(res['status'], "SUCCESS")
            self.__class__.created_project = res['data']['id']
        pprint(self.__class__.created_project)
        print(datetime.now()-tock)

    def test_3_getProjectId(self):
        id = self.__class__.created_project

        if not id:
            self.assertEqual(id, "expected created_project, but got non")
        # print(id)
        r = requests.get('http://'+server+':8111/api/v1/projects/'+id, cookies=self.cookies)
        #pprint(r.text)
        self.assertEqual(r.status_code, 200)
        res = json.loads(r.text)
        self.assertGreater(len(res['result']),0)

    def test_4_putProject(self):
        id = self.__class__.created_project

        if not id:
            self.assertEqual(id, "Project was not created in previous test, we cannot continue this test")
        rGet = requests.get('http://'+server+':8111/api/v1/projects/'+id, cookies=self.cookies)
        res = json.loads(rGet.text)
        self.assertGreater(len(res['result']),0)
        project = res['result'][0]
        self.assertEqual(rGet.status_code, 200)

        rGetUser = requests.get('http://'+server+':8111/api/v1/users', cookies=self.cookies)
        res = json.loads(rGetUser.text)
        otherUser = res['result'][0]
        self.assertEqual(rGet.status_code, 200)

        payload = project
        payload['pi_users'].append(otherUser['id'])
        rPut = requests.put('http://'+server+':8111/api/v1/projects/'+id, headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), cookies=self.cookies, timeout=self.timeout)
        pprint(rPut.text)
        self.assertEqual(rPut.status_code, 200)
        result = json.loads(rPut.text)
        self.assertEqual(result['result'], "success")
        for event in result['events']:
            res = self.checkEvent(event)
            self.assertEqual(res['status'], "SUCCESS")

        rUpdated = requests.get('http://'+server+':8111/api/v1/projects/'+id, cookies=self.cookies)
        res = json.loads(rUpdated.text)
        projectUpdated = res['result'][0]
        self.assertEqual(rUpdated.status_code, 200)

        self.assertNotEqual(project, projectUpdated)
        self.assertEqual(projectUpdated['pi_users'], payload['pi_users'])

    def test_5_deleteProject(self):
        id = self.__class__.created_project
        if not id:
            self.assertEqual(id, "Project was not created in previous test, we cannot continue this test")
        rDelete = requests.delete('http://'+server+':8111/api/v1/projects/'+id, cookies=self.cookies)
        pprint(rDelete.text)
        self.assertEqual(rDelete.status_code, 200)

        result = json.loads(rDelete.text)
        self.assertEqual(result['result'], "success")
        for event in result['events']:
            res = self.checkEvent(event)
            self.assertEqual(res['status'], "SUCCESS")

        rGet = requests.get('http://'+server+':8111/api/v1/projects/'+id, cookies=self.cookies)
        res = json.loads(rGet.text)
        project = res['result']
        self.assertEqual(rGet.status_code, 200)
        pprint(project)
        #self.assertEqual(len(project), 0)

if __name__ == '__main__':
    unittest.main()
