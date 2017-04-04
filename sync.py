#!/usr/bin/env python3.5

import sys
import threading
from tornado import gen

from myslice.services.workers.authorities import syncAuthorities
from myslice.services.workers.projects import syncProjects
from myslice.services.workers.users import syncUsers
from myslice.services.workers.slices import syncSlices
from myslice.services.workers.leases import syncLeases
from myslice.services.monitor.testbeds import syncTestbeds
from myslice.services.monitor.resources import syncResources

@gen.coroutine
def main(argv):
    try:
        if len(argv) != 1:
            print("Help: use the command with one of the parameters")
            print("sync.py all|authorities|projects|users|slices|testbeds|resources|leases")
            sys.exit(2)

        lock = threading.Lock()

        # Synchronize from SFA Registry into the DB

        if argv[0].startswith('auth') or argv[0] == 'all':
            print("sync authorities...")
            syncAuthorities(lock)

        if argv[0].startswith('p') or argv[0] == 'all':
            print("sync projects...")
            syncProjects(lock)

        if argv[0].startswith('u') or argv[0] == 'all':
            print("sync users...")
            syncUsers(lock)

        if argv[0].startswith('s') or argv[0] == 'all':
            print("sync slices...")
            syncSlices()

        if argv[0].startswith('t') or argv[0] == 'all':
            print("sync testbeds...")
            syncTestbeds()

        if argv[0].startswith('r') or argv[0] == 'all':
            print("sync resources...")
            syncResources()

        if argv[0].startswith('l') or argv[0] == 'all':
            print("sync leases...")
            syncLeases()

    except Exception as e:
        import traceback
        traceback.print_exc()
        print("Help: use the command with one of the parameters")
        print("sync.py all|authorities|projects|users|slices|testbeds|resources|leases")
        sys.exit(2)

if __name__ == '__main__':
    main(sys.argv[1:])
