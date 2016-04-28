#!/usr/bin/env python3.5
import sys
import unittest

from pprint import pprint

import requests

from tests import s

class TestProject(unittest.TestCase):

    #def setUp(self):

    def test_invalidRequest(self):
        payload = {'key1': 'value1', 'key2': 'value2'}
        r = requests.post("http://localhost:8111/api/v1/activity", data=payload)
        self.assertEqual(r.status_code, 500)

if __name__ == '__main__':
    unittest.main()
