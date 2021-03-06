#!/usr/bin/env python3.5

import requests
import sys
import time
import unittest

from pprint import pprint

from myslice.tests.config import s, server

class TestDeployment(unittest.TestCase):

    def test_0_MySliceWeb(self):
        r = requests.get('http://'+server+'')
        self.assertEqual(r.status_code, 200)
        #print(r.text)

    def test_1_RethinkDBWeb(self):
        r = requests.get('http://'+server+':8080')
        self.assertEqual(r.status_code, 200)
        #print(r.text)

if __name__ == '__main__':
    # sleep 30 sec waiting that the services start
    # time.sleep(30)
    # unittest.main()

    suites = [unittest.TestLoader().loadTestsFromTestCase(TestDeployment)]
    testResult = unittest.TextTestRunner(verbosity=1).run(unittest.TestSuite(suites))

    print ('The errors: ', testResult.errors)
    print('The Failures: ', testResult.failures)
    print ('The number of runs: ', testResult.testsRun)
    print('Test were successful: ', testResult.wasSuccessful())

