#!/usr/bin/env python3.5

import requests
import sys
import time
import unittest

from pprint import pprint

from myslice.tests.config import s

class TestDeployment(unittest.TestCase):

    def test_0_MySliceWeb(self):
        r = requests.get('http://localhost:8111')
        self.assertEqual(r.status_code, 200)
        #print(r.text)

    def test_1_RethinkDBWeb(self):
        r = requests.get('http://localhost:8080')
        self.assertEqual(r.status_code, 200)
        #print(r.text)

if __name__ == '__main__':
    # sleep 5 sec waiting that the services start
    time.sleep(5)
    unittest.main()
