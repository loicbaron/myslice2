#!/usr/bin/env python3.5

import json
import sys, getopt
import rethinkdb as r
import threading
from myslice import db
from myslice.web.controllers.login import crypt_password
from pprint import pprint
from myslice.services.workers.users import sync as syncUsers

def main(argv):
    try:
       opts, args = getopt.getopt(argv,"he:P:k:p:s",["email=","password=","private_key=","public_key=","sync="])
    except getopt.GetoptError:
       print('init_user.py -e <email> -P <password> -k <private_key path> -p <public_key path> -s <synchronize with Registry>')
       sys.exit(2)
    if(len(opts)<4):
       print('Missing parameters:')
       print('init_user.py -e <email> -P <password> -k <private_key path> -p <public_key path> -s <synchronize with Registry>')
       sys.exit(2)

    sync = False

    for opt, arg in opts:
       if opt == '-h':
         print('init_user.py -e <email> -P <password> -k <private_key path> -p <public_key path> -s <synchronize with Registry>')
         sys.exit()
       elif opt in ("-e", "--email"):
         email = arg
       elif opt in ("-P", "--password"):
         password = crypt_password(arg)
       elif opt in ("-k", "--private_key"):
         f = open(arg, 'r')
         private_key = f.read()
       elif opt in ("-p", "--public_key"):
         f = open(arg, 'r')
         public_key = f.read()
       elif opt in ("-s", "--sync"):
         if arg.lower() in ["true", "yes", "y"]:
            sync = True
   
    # Synchronize the users from SFA Registry into the DB 
    lock = threading.Lock()
    #print("sync user %s" % email)
    if sync:
        syncUsers(lock, email=email, job=False)

    # Get the user that we want to update
    dbconnection = db.connect()
    result = r.db('myslice').table('users').filter({'email':email}, default=False).run(dbconnection)
    for u in result: 
        u['password']=password
        u['private_key']=private_key
        u['public_key']=public_key
        u['generate_keys']=False
        r.db('myslice').table('users').get(u['id']).update(u).run(dbconnection)
        break

if __name__ == '__main__':
    main(sys.argv[1:])
