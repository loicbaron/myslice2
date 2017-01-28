#!/usr/bin/env python3.5
import sys, getopt
from pprint import pprint
import rethinkdb as r

from myslice import db

def main(argv):
    try:
       opts, args = getopt.getopt(argv,"ht:c:i:f:",["table=","command=","id=","filter="])
    except getopt.GetoptError:
       print('rethink.py -t <table> -c <command> -i <id> -f <filter>')
       sys.exit(2)

    t = None
    command = None
    id = None
    filter = None

    for opt, arg in opts:
       if opt == '-h':
        print('rethink.py -t <table> -c <command> -i <id> -f <filter>')
        sys.exit()
       elif opt in ("-t", "--table"):
         t = arg
       elif opt in ("-c", "--command"):
         command = arg
       elif opt in ("-i", "--id"):
         id = arg
       elif opt in ("-f", "--filter"):
         filter = arg

    if not t:
        print('please specify the table you want to query')
        print('rethink.py -t <table> -c <command> -i <id> -f <filter>')
        sys.exit()
    if not command:
        command = "get"

    dbconnection = db.connect()
    if command in ["select", "SELECT", "get", "GET"]:
        if id:
            print("yes we have the id")
            result = r.db('myslice').table(t).get(id).run(dbconnection)
        elif filter:
            print("yes we have a filter")
            result = r.db('myslice').table(t).filter(f).run(dbconnection)
        else:
            print("neither id nor filter")
            result = r.db('myslice').table(t).run(dbconnection)

    pprint(result)

if __name__ == '__main__':
    main(sys.argv[1:])
