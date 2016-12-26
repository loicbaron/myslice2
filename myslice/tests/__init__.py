#!/usr/bin/env python3.5

import json
import requests
import time
import unittest

from myslice.tests.config import s

class Tests(unittest.TestCase):

    def setUp(self):
        self.timeout = 10
        self.cookies = s['cookies']

    def checkEvent(self, event):
        status = "INIT"
        res = None
        i = 0
        while(i < 30 and status not in ["PENDING","SUCCESS","ERROR","WARNING","APPROVED","DENIED"]):
            time.sleep(2)
            i = i + 1
            rActivity = requests.get('http://localhost:8111/api/v1/activity/'+event, cookies=self.cookies)
            resActivity = json.loads(rActivity.text)
            res = resActivity['result'][0]
            status = res['status']
        return res

