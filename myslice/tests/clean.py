#!/usr/bin/env python3.5

import json
import requests
import sys
from datetime import datetime
from pprint import pprint
from tornado import gen

from myslice.tests import LocalTestCase
from myslice.tests.config import s, server

timeout = 10
cookies = s['cookies']
s['automate_test'] = False
test = LocalTestCase()
test.cookies = cookies

def clean(cookies, objectType):
    """Delete objectType if the id contains autotest"""
    r = requests.get('http://'+server+':8111/api/v1/'+objectType, cookies=cookies)
    result = json.loads(r.text)
    objects = result['result']
    for o in objects:
        if "autotest" in o['id']:
            print("deleting %s %s" % (objectType,o['hrn']))
            rDelete = requests.delete('http://'+server+':8111/api/v1/'+objectType+'/'+o['id'], cookies=cookies)
            pprint(rDelete.text)

            result = json.loads(rDelete.text)
            for event in result['events']:
                res = test.checkEvent(event)
                if res['status'] == "SUCCESS":
                    print("%s %s deleted" % (objectType,o['hrn']))
                else:
                    print("could not delete %s %s" % (objectType,o['hrn']))
        

@gen.coroutine
def main(argv):
    try:
        if len(argv) != 1:
            print("Help: use the command with one of the parameters")
            print("clean.py all|authorities|projects|users|slices")
            sys.exit(2)

        if argv[0].startswith('auth') or argv[0] == 'all':
            print("clean authorities...")
            clean(cookies, 'authorities')

        if argv[0].startswith('p') or argv[0] == 'all':
            print("clean projects...")
            clean(cookies, 'projects')

        if argv[0].startswith('u') or argv[0] == 'all':
            print("clean users...")
            clean(cookies, 'users')

        if argv[0].startswith('s') or argv[0] == 'all':
            print("clean slices...")
            clean(cookies, 'slices')

    except Exception as e:
        import traceback
        traceback.print_exc()
        print("Help: use the command with one of the parameters")
        print("clean.py all|authorities|projects|users|slices")
        sys.exit(2)

if __name__ == '__main__':
    main(sys.argv[1:])
