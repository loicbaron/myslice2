#!/usr/bin/env python3.5

'''
    MySlice Router service

    This service will run multiple threads responsible for watching for changes
    to rethinkdb and broadcast to connected clients with ZeroMQ

    (c) 2017 Radomir Klacza <radomir.klacza@lip6.fr>
'''

import myslice.lib.log as logging
import json
import signal
import threading
import zmq
from queue import Queue
from myslice.db.activity import Event, ObjectType

import rethinkdb as r

from pprint import pprint

from zmq.utils.strtypes import asbytes
import pickle

from myslice.lib.util import myJSONEncoder
from myslice.db import connect, changes, tables

logger = logging.getLogger('myslice-router')


def receive_signal(signum, stack):
    logger.info('Received signal %s', signum)
    raise SystemExit('Exiting')



def filter_channels(event):

    """
    findings all channels that message needs to be send to
    :param event: 
    :return:[] of channels that we need to send messages to 
    """

    channels = []

    if event.isNew() and event.status != event.previous_status:
        channels.append(b'activity')

    if event.isWaiting() or event.isApproved():
        if event.object.type == ObjectType.AUTHORITY:
            channels.append(b'authorities')
        elif event.object.type in [ObjectType.PROJECT, ObjectType.SLICE]:
            channels.append(b'experiments')
        elif event.object.type == ObjectType.LEASE:
            channels.append(b'leases')

    if event.isReady():
        if event.object.type in [ObjectType.USER, ObjectType.PASSWORD]:
            channels.append(b'users')

    if event.notify:
        channels.append(b'emails')

    if not channels and not event.isSuccess:
        logger.error('[myslice-router] Channel not found for the message with status {}'.format(change['new_val']['status']))

    return channels


if __name__ == '__main__':

    signal.signal(signal.SIGINT, receive_signal)
    signal.signal(signal.SIGTERM, receive_signal)
    signal.signal(signal.SIGHUP, receive_signal)

    # RethinkDB connection
    dbconnection = connect()

    logger.info("[myslice-router] Watching changes on the activity")

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
            logger.info("[myslice-router] Got the message from the Rethinkdb {}".format(change))

            try:
                event = Event(change['new_val'])
            except:
                logger.error("[myslice-router] Message was not correct event object {}".format(change))

            channels = filter_channels(event)

            # serialize for zeromq
            for channel in channels:
                # channel = asbytes(channel)
                # serialized_c = asbytes(json.dumps(change, ensure_ascii=False, cls=myJSONEncoder))

                #sending to a channel:
                sock.send_multipart([channel, pickle.dumps(change)])

    except SystemExit:
        logger.error("there was an error with router - exiting")






