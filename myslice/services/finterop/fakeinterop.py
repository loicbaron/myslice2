#!/usr/bin/env python3.5
import logging
import pika
import signal
import threading
import time

from multiprocessing import Process

logger = logging.getLogger('myslice.service.finterop.fakeinterop')

class FakeInterop():

    def __init__(self, queue_name='hello'):
        self._alive = True 
        logger.info("Initialize Queue %s" % queue_name)
        self.queue = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                   'localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

    def publish(self, msg):
        self.channel.basic_publish(exchange='',
                              routing_key=self.queue,
                              body=msg)
        logger.debug(" [x] Sent %r" % msg)
    
    def fake(self, msg='Hello World!'):
        try:
            while self._alive:
                self.publish(msg)
                time.sleep(10)

        except Exception as e:
            import traceback
            traceback.print_exc()

class FakeInteropConsumer():

    def __init__(self, queue_name='hello'):
        self.queue = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                   'localhost'))
        self.channel = self.connection.channel()

    def subscribe(self):
        self.channel.basic_consume(self.callback,
                          queue=self.queue,
                          no_ack=True)
        self.channel.start_consuming()
    
    def callback(self, ch, method, properties, body):
        logger.debug(" [x] Received %r" % body)
