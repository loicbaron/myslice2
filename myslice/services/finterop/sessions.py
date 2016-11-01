#!/usr/bin/env python3.5
import logging
import pika

logger = logging.getLogger('myslice.service.finterop.sessions')

def start(queue_name):
    logger.info("finterop session %s start" % queue_name) 
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
    # TODO: add to DB
    print(" [x] Received %r" % body)
    logger.info('Received %r' % body)

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
