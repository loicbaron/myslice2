#!/usr/bin/env python3.5
import logging
import pika
import json
import time
import config as cfg



logger = logging.getLogger('myslice.service.finterop.resourceRepo')


class ResourceRepo():
    def __init__(self, queue_name=cfg.QUEUE_TOPIC):
        self._alive = True
        logger.info("Initialize Queue %s" % queue_name)
        self.queue = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=cfg.RABBIT_HOST))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

        data = {

               "description": "This is description about URR"
        }
        message = json.dumps(data)

    def publish(self, msg):
        self.channel.basic_publish(exchange='', routing_key=cfg.QUEUE_TOPIC, body=self.message)
        logger.debug(" [x] Sent %r" % msg)
        self.connection.close()

