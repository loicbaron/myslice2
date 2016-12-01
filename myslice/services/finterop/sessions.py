#!/usr/bin/env python3.5
import logging
import pika

from pprint import pprint

import rethinkdb as r
import myslice.db as db
from myslice import settings as s
from myslice.lib.util import format_date

logger = logging.getLogger('myslice.service.finterop.sessions')

# DB connection
dbconnection = db.connect()

def start(queue_name):
    logger.info("finterop start listening session %s" % queue_name) 
    print("start listening to %s" % queue_name)
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                   'localhost'))
        channel = connection.channel()
        channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)
        channel.start_consuming()

    except Exception as e:
        import traceback
        traceback.print_exc()

def callback(ch, method, properties, body):
    print("ch = ")
    print(vars(ch))
    print("method = ")
    print(vars(method))
    print("properties = ")
    print(vars(properties))
    print(" [x] Received %r" % body)
    logger.info('Received %r' % body)

    # XXX For performance
    # slice_id should be embeded into the message instead of accessing DB
    session = r.db(s.db.name).table('sessions').get(method.routing_key).run(dbconnection)

    # TODO: add to DB
    data = {'session':method.routing_key,'message':body.decode("utf-8"),'date':format_date(), 'slice_id':session['slice_id']}

    r.db(s.db.name).table('messages').insert(data, conflict='update').run(dbconnection)

def stop(queue_name):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                   'localhost'))
        channel = connection.channel()
        channel.basic_cancel(consumer_tag=queue_name)
        connection.close
        print(" [x] Stopped listening %r" % queue_name)
        logger.info("Stopped %r" % queue_name)
    except Exception as e:
        import traceback
        traceback.print_exc()
