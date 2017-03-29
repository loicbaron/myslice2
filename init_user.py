#!/usr/bin/env python3.5

import json
import sys, getopt
import rethinkdb as r
import threading
from myslice import db
from myslice.db.user import User
from myslicelib.query import q
from myslice.web.controllers.login import crypt_password
from pprint import pprint
from myslice.services.workers.users import syncUsers

from tornado import gen, escape

@gen.coroutine
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
   

    dbconnection = db.connect()

    lock = threading.Lock()
    # Synchronize the users from SFA Registry into the DB
    if sync:
        print("sync user %s" % email)
        syncUsers(lock, email=email, job=False)
    else:
        try:
            # Get the user from SFA Registry
            print("get user %s from SFA Reg" % email)
            remote_user = q(User).filter('email', email).get().first()
            pprint(remote_user)
            # merge fields from script with remote_user
            remote_user.setAttribute('password', password)
            remote_user.setAttribute('private_key', private_key)
            remote_user.setAttribute('generate_keys', False)
            remote_user.setAttribute('public_key', public_key)
            remote_user.setAttribute('keys', [public_key])
            r.db('myslice').table('users').insert(remote_user.dict()).run(dbconnection)
            result = r.db('myslice').table('users').get(remote_user.id).run(dbconnection)
            #result = remote_user.save(dbconnection)
            if result:
                print("User saved")
            else:
                print("Error during save")
                pprint(result)
            # if user has private key
            # update its Credentials
            #if 'private_key' in updated_user:
            #    updated_user = update_credentials(updated_user)
        except Exception as e:
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    main(sys.argv[1:])
