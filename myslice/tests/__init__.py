#!/usr/bin/env python3.5

import json
import requests
import time
import unittest

from pprint import pprint
from random import randint
from myslice.tests.config import s, server
from datetime import datetime
import rethinkdb as r

from myslice.tests.config import authority

class LocalTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(LocalTestCase, self).__init__(*args, **kwargs)
        self.automateTest = False


    def startTimer(self):
        self.tick = datetime.now()

    def stopTimer(self):
        self.tock = datetime.now()
        diff = self.tock - self.tick
        print(self._testMethodName, ": ", diff, "s")
        if self.automateTest:
            r.connect("localhost", 28015).repl()
            r.table('rabbits').insert({
                "testMethodName": self._testMethodName,
                "testName": self.__class__.__name__,
                "testDurationMiliSec": diff.seconds,
                "timestamp": datetime.now(r.make_timezone('00:00')),
            }).run()

    def getProjectId(self):
        """
        Returns a project id
        one of the user's projects
        by default it takes first project on the list 
        if the user has no project, create one
        """
        r = requests.get('http://' + server + ':8111/api/v1/users/projects', cookies=self.cookies)
        data = json.loads(r.text)
        #from pprint import pprint
        #pprint(data)
        if len(data['result']) > 0:
            return data['result'][-1]['id']
        else:
            return self.createProject()['id']

    def createProject(self):
        name = 'autotest_' + str(randint(0,10000))
        payload = {'name': name, 'description': 'this is an automated project', 'authority':authority}
        r = requests.post('http://'+server+':8111/api/v1/projects', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), cookies=self.cookies, timeout=self.timeout)
        pprint(r.text)
        self.assertEqual(r.status_code, 200)
        # Event status = SUCCESS
        result = json.loads(r.text)
        self.assertEqual(result['result'], "success")
        for event in result['events']:
            res = self.checkEvent(event)
            self.assertEqual(res['status'], "SUCCESS")
            return res['data']
        return None

    def getSliceId(self):
        """
        Returns a slice id
        one of the user's slices
        by default it takes first slice on the list 
        if the user has no slice, create one
        """
        r = requests.get('http://' + server + ':8111/api/v1/users/slices', cookies=self.cookies)
        data = json.loads(r.text)
        if len(data['result']) > 0:
            return data['result'][-1]['id']
        else:
            return self.createSlice()['id']

    def createSlice(self):
        name = 'autotest_' + str(randint(0,10000))
        project = self.getProjectId()
        payload = {'shortname': name, 'name': name, 'project': {'id': project}}
        r = requests.post('http://'+server+':8111/api/v1/slices', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), cookies=self.cookies, timeout=self.timeout)
        pprint(r.text)
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.text)
        self.assertEqual(result['result'], "success")
        for event in result['events']:
            res = self.checkEvent(event)
            self.assertEqual(res['status'], "SUCCESS")
            return res['data']
        return None
      
    def getProfile(self):
        r = requests.get('http://'+server+':8111/api/v1/profile', cookies=self.cookies)
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.text)
        return result['result']

    def checkEvent(self, event, initial_status=None, expected_status= None):
        status = "INIT"
        res = None
        i = 0
        if expected_status:
            final_status = [expected_status]
        else:
            final_status = ["CONFIRM", "PENDING","SUCCESS","ERROR","WARNING","DENIED"]

        if initial_status:
            final_status = list(set(final_status) - {initial_status})

        # If processing the event takes more than 5 min = test failed
        while(i < 60 and status not in final_status):
            time.sleep(5)
            i = i + 1
            rActivity = requests.get('http://'+server+':8111/api/v1/activity/'+event, cookies=self.cookies)
            if rActivity.status_code == 200:
                resActivity = json.loads(rActivity.text)
                if 'result' in resActivity:
                    res = resActivity['result'][0]
                    status = res['status']
        return res

