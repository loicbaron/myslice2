#!/usr/bin/env python3.5

import json
import requests
import time
import unittest

from myslice.tests.config import s, server

class Tests(unittest.TestCase):

    def setUp(self):
        self.timeout = 10
        self.cookies = s['cookies']

    def checkEvent(self, event, initial_status=None):
        status = "INIT"
        res = None
        i = 0
        final_status = ["PENDING","SUCCESS","ERROR","WARNING","DENIED"]
        if initial_status:
            final_status = list(set(final_status) - {initial_status})

        while(i < 30 and status not in final_status):
            time.sleep(2)
            i = i + 1
            rActivity = requests.get('http://'+server+':8111/api/v1/activity/'+event, cookies=self.cookies)
            resActivity = json.loads(rActivity.text)
            res = resActivity['result'][0]
            status = res['status']
        return res

