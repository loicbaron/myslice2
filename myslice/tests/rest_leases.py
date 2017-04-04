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

class TestLeases(LocalTestCase):

    created_slice = None
    project = None
    testbeds = None
    testbedsLeases = None
    resource = None

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
        r = requests.get('http://'+server+':8111/api/v1/leases')
        self.assertEqual(r.status_code, 400)

    def test_0_postNoAuth(self):
        payload = {}
        r = requests.post('http://'+server+':8111/api/v1/leases', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), timeout=self.timeout)
        self.assertEqual(r.status_code, 400)

    def test_1_getLeases(self):
        r = requests.get('http://'+server+':8111/api/v1/leases', cookies=self.cookies)
        self.assertEqual(r.status_code, 200)
        print("Found %s Leases" % len(json.loads(r.text)['result']))
        for l in json.loads(r.text)['result']:
            if 'resources' in l and len(l['resources']) > 0:
                self.__class__.resource = l['resources'][0]
                break

    def test_1_getLeasesTs(self):
        # 2h before now
        ts_start = int(time.time()) - 7200
        # 2h after now
        ts_end = int(time.time()) + 7200
        r = requests.get('http://'+server+':8111/api/v1/leases?timestamp_start='+str(ts_start)+'&timestamp_end='+str(ts_end), cookies=self.cookies)
        self.assertEqual(r.status_code, 200)
        print("Found %s Leases" % len(json.loads(r.text)['result']))
        for l in json.loads(r.text)['result']:
            self.assertGreaterEqual(l['start_time'], ts_start)
            self.assertLessEqual(l['end_time'], ts_end)

    def test_2_getTestbeds(self):
        r = requests.get('http://'+server+':8111/api/v1/testbeds', cookies=self.cookies)
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

    # /testbeds/<id>/leases[?timestamp_start=<XXX>&timestamp_end=<XXX>]
    def test_3_getTestbedLeases(self):
        testbedsLeases = self.__class__.testbedsLeases
        self.assertGreater(len(testbedsLeases), 0)
        r = requests.get('http://'+server+':8111/api/v1/testbeds/'+testbedsLeases[0]+'/leases', cookies=self.cookies)
        print("Found %s Leases" % len(json.loads(r.text)['result']))
        self.assertEqual(r.status_code, 200)

    def test_3_getTestbedLeasesTs(self):
        # 2h before now
        ts_start = int(time.time()) - 7200
        # 2h after now
        ts_end = int(time.time()) + 7200
        testbedsLeases = self.__class__.testbedsLeases
        self.assertGreater(len(testbedsLeases), 0)
        r = requests.get('http://'+server+':8111/api/v1/testbeds/'+testbedsLeases[0]+'/leases?timestamp_start='+str(ts_start)+'&timestamp_end='+str(ts_end), cookies=self.cookies)
        self.assertEqual(r.status_code, 200)
        print("Found %s Leases" % len(json.loads(r.text)['result']))
        for l in json.loads(r.text)['result']:
            self.assertGreaterEqual(l['start_time'], ts_start)
            self.assertLessEqual(l['end_time'], ts_end)

    #    /resources/<id>/leases
    def test_4_getResourceLeses(self):
        resource = self.__class__.resource
        if not resource:
            self.assertEqual(resource, "expected resource but got none")
        r = requests.get('http://'+server+':8111/api/v1/resources/'+resource+'/leases', cookies=self.cookies)
        self.assertEqual(r.status_code, 200)
        print("Found %s Leases" % len(json.loads(r.text)['result']))
        for l in json.loads(r.text)['result']:
            if 'resources' in l and len(l['resources']) > 0:
                self.assertIn(resource, l['resources'])

    # /resources[?timestamp_start=<XXX>&timestamp_end=<XXX>]
    def test_5_postLease(self):
        # now
        ts_start = int(time.time())
        # 1h after now
        ts_end = int(time.time()) + 3600
        # Get resources available in the coming 1h
        testbedsLeases = self.__class__.testbedsLeases
        self.assertGreater(len(testbedsLeases), 0)
        # 1 testbed per lease
        # -----------------------------------
        # TODO: post a lease with resources from different testbeds (without testbed optional param)
        # -----------------------------------
        r = requests.get('http://'+server+':8111/api/v1/testbeds/'+testbedsLeases[0]+'/resources?timestamp_start='+str(ts_start)+'&timestamp_end='+str(ts_end), cookies=self.cookies)
        self.assertEqual(r.status_code, 200)
        resources = json.loads(r.text)['result']
        # Check if resources are available
        self.assertGreater(len(resources), 0)
        selectedResources = [x['id'] for x in resources[:2]]
        print("Reservation of the following nodes:")
        pprint(selectedResources)
        # -----------------------------------
        # TODO: test the optional params
        # TODO: test with list of leases
        # -----------------------------------
        #{
        #   "slice_id": self.getSliceId() 
        #   "resources": selectedResources, 
        #   "testbed": "urn:publicid:IDN+iotlab+authority+am",
        #   "duration": 300,
        #   "start_time": 1475718144,
        #   "end_time": 1475718194,
        #}
        # Create a Lease for 5 minutes starting now
        payload = {
           "slice_id": self.getSliceId(), 
           "resources": selectedResources, 
           "testbed": testbedsLeases[0],
           "duration": 300,
        }
        r = requests.post('http://'+server+':8111/api/v1/leases', headers={str('Content-Type'):'application/json'}, data=json.dumps(payload), cookies=self.cookies, timeout=self.timeout)
        pprint(r.text)
        self.assertEqual(r.status_code, 200)
        result = json.loads(r.text)
        self.assertEqual(result['result'], "success")
        for event in result['events']:
            res = self.checkEvent(event)
            self.assertEqual(res['status'], "SUCCESS")

        # TODO: check that the selectedResources are in the Slice

if __name__ == '__main__':
    unittest.main()
