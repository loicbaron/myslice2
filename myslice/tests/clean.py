#!/usr/bin/env python3.5

import json
import requests
import sys
from pprint import pprint
from tornado import gen

from myslice.tests import LocalTestCase
from myslice.tests.config import s

from myslicelib.model.authority import Authority
from myslicelib.model.project import Project
from myslicelib.model.user import User
from myslicelib.model.slice import Slice
from myslicelib.query import q

timeout = 10
s['automate_test'] = False

def clean(objectType, server):
    """Delete objectType if the id contains autotest"""
    LocalTestCase.SERVER = server
    test = LocalTestCase()
    r = requests.get('http://'+server+':8111/api/v1/'+objectType, cookies=test.cookies)
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


def cleanRegistry(objects):
    for o in objects:
        if "autotest" in o.id:
            print("Deleting %s in Registry" % o.id)
            o.delete()

@gen.coroutine
def main(argv):

    try:
        if len(argv) != 2:
            print("Help: use the command with one of the parameters and server name")
            print("clean.py all|authorities|projects|users|slices <server.fqdn.or.ip>")
            print("EXAMPLE: clean.py all zeus.noc.onelab.eu")

            sys.exit(2)

        if argv[0].startswith('auth') or argv[0] == 'all':
            print("clean authorities...")
            clean('authorities', argv[1])
            # clean(cookies, 'authorities', argv[1])
            objects = q(Authority).get()
            cleanRegistry(objects)

        if argv[0].startswith('p') or argv[0] == 'all':
            print("clean projects...")
            clean( 'projects', argv[1])
            # clean(cookies, 'projects', argv[1])
            objects = q(Project).get()
            cleanRegistry(objects)

        if argv[0].startswith('u') or argv[0] == 'all':
            print("clean users...")
            clean( 'users', argv[1])
            # clean(cookies, 'users', argv[1])
            objects = q(User).get()
            cleanRegistry(objects)

        if argv[0].startswith('s') or argv[0] == 'all':
            print("clean slices...")
            clean('slices', argv[1])
            # clean(cookies, 'slices', argv[1])
            objects = q(Slice).get()
            cleanRegistry(objects)

    except Exception as e:
        import traceback
        traceback.print_exc()
        print("Help: use the command with one of the parameters and server name")
        print("clean.py all|authorities|projects|users|slices <server.fqdn.or.ip>")
        print("EXAMPLE: clean.py all zeus.noc.onelab.eu")
        sys.exit(2)

if __name__ == '__main__':
    main(sys.argv[1:])