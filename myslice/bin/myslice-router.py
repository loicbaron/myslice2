#!/usr/bin/env python3.5

'''
    MySlice Router service

    This service will run multiple threads responsible for watching for changes
    to rethinkdb and broadcast to connected clients with ZeroMQ

    check more info: 
    http://zguide.zeromq.org/php:chapter5
    https://github.com/zeromq/pyzmq/blob/master/examples/pubsub/
    https://pyzmq.readthedocs.io/en/latest/api/index.html

    (c) 2017 Radomir Klacza <radomir.klacza@lip6.fr>
'''

import myslice.lib.log as logging
import json
import signal
import threading
import zmq
from queue import Queue

import rethinkdb as r

from pprint import pprint

from zmq.utils.strtypes import asbytes

from myslice.lib.util import myJSONEncoder
from myslice.db import connect, changes, tables

logger = logging.getLogger()


def receive_signal(signum, stack):
    logger.info('Received signal %s', signum)
    raise SystemExit('Exiting')

if __name__ == '__main__':

    signal.signal(signal.SIGINT, receive_signal)
    signal.signal(signal.SIGTERM, receive_signal)
    signal.signal(signal.SIGHUP, receive_signal)

    # RethinkDB connection
    dbconnection = connect()

    logger.info("watching changes on the activity")

    try:
        context = zmq.Context()
        sock = context.socket(zmq.PUB)
        sock.bind('tcp://127.0.0.1:6002')

    except SystemExit:
        # clean up
        sock.close()
        context.term()


    try:
        # Watch for changes on the activity table
        feed = r.db('myslice').table('activity').changes().run(dbconnection)

        for change in feed:

            channel = None
            # logger.info('change: {}'.format(change))

            #filtering
            if change['new_val']['status'] == "NEW":
                channel = 'activity'

            else:
                logger.info('Channel not found for the message with status {}'.format(change['new_val']['status']))

            # serialize for zeromq
            if channel:
                channel = asbytes(channel)
                serialized_c = asbytes(json.dumps(change, ensure_ascii=False, cls=myJSONEncoder))

                #sending to a channel:
                sock.send_multipart([channel, serialized_c])


    except SystemExit:
        logger.error("there was an error with router - exiting")





