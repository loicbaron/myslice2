#!/usr/bin/env python3.5

import json
import requests
import sys
from datetime import datetime
from pprint import pprint
from tornado import gen

from myslice.tests import LocalTestCase
from myslice.tests.config import s, server

from myslicelib.model.authority import Authority
from myslicelib.model.project import Project
from myslicelib.model.user import User
from myslicelib.model.slice import Slice
from myslicelib.query import q

def cleanRegistry(objects):
    for o in objects:
        if "autotest" in o.id:
            print("Deleting %s in Registry" % o.id)
            o.delete()

@gen.coroutine
def main(argv):
    try:
        if len(argv) != 1:
            print("Help: use the command with one of the parameters")
            print("clean.py all|authorities|projects|users|slices")
            sys.exit(2)

        if argv[0].startswith('auth') or argv[0] == 'all':
            print("clean authorities...")
            objects = q(Authority).get()
            cleanRegistry(objects)

        if argv[0].startswith('p') or argv[0] == 'all':
            print("clean projects...")
            objects = q(Project).get()
            cleanRegistry(objects)

        if argv[0].startswith('u') or argv[0] == 'all':
            print("clean users...")
            objects = q(User).get()
            cleanRegistry(objects)

        if argv[0].startswith('s') or argv[0] == 'all':
            print("clean slices...")
            objects = q(Slice).get()
            cleanRegistry(objects)

    except Exception as e:
        import traceback
        traceback.print_exc()
        print("Help: use the command with one of the parameters")
        print("clean.py all|authorities|projects|users|slices")
        sys.exit(2)

if __name__ == '__main__':
    main(sys.argv[1:])
