#!/usr/bin/env python3.5

import json
import requests
import time
import unittest

from myslice.tests.config import s, server
from datetime import datetime
import rethinkdb as r



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
        """
        r = requests.get('http://' + server + ':8111/api/v1/users/projects', cookies=self.cookies)
        data = json.loads(r.text)
        #from pprint import pprint
        #pprint(data)
        try:
            return data['result'][0]['id']
        except:
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

