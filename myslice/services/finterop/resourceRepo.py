#!/usr/bin/env python3.5
import logging
import pika
import json
import config as cfg

# Connect to RabbitMQ and create channel

credentials = pika.PlainCredentials('f-interop', 'Cowabunga')
parameters = pika.ConnectionParameters('f-interop.rennes.inria.fr',
                                       5672,
                                       '/',
                                       credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare queue to send data
channel.queue_declare(queue=cfg.QUEUE_TOPIC)

data = {
"_type": "resource_repository.insert_resource",
"resource": {
        "resource_id": "resource-001-unique-id",
        "owner_id": "user-001-unique-id",
        "privacy_flag": "public",

}
}

message = json.dumps(data)

# Send data
channel.basic_publish(exchange='', routing_key=cfg.QUEUE_TOPIC, body=message)
print(" [x] Sent data to RabbitMQ")
connection.close()