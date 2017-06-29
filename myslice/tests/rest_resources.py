#!/usr/bin/env python3.5

import json
import requests
import time
import unittest

from pprint import pprint
from random import randint

from myslice.tests import LocalTestCase
from myslice.tests.config import s
from datetime import datetime

class TestResources(LocalTestCase):

    testbed = None

    def setUp(self):
        self.automateTest = s['automate_test']
        self.startTimer()
        self.timeout = 10

    def tearDown(self):
        self.stopTimer()

    def test_0_getNoAuth(self):
        r = requests.get('http://'+self.server+':8111/api/v1/resources')
        self.assertEqual(r.status_code, 400)

    def test_1_getAllResources(self):
        r = requests.get('http://'+self.server+':8111/api/v1/resources', cookies=self.cookies)
        self.assertEqual(r.status_code, 200)

    def test_1_getTestbeds(self):
        r = requests.get('http://'+self.server+':8111/api/v1/testbeds', cookies=self.cookies)
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.text)
        self.__class__.testbed = data['result'][0]

    def test_2_getTestbedResources(self):
        testbed = self.__class__.testbed
        r = requests.get('http://'+self.server+':8111/api/v1/testbeds/'+testbed+'/resources', cookies=self.cookies)
        self.assertEqual(r.status_code, 200)

