#!/usr/bin/env python3.5
import logging
import pika
import json
import config as cfg

# Connect to RabbitMQ and create channel
connection = pika.BlockingConnection(pika.ConnectionParameters(host=cfg.RABBIT_HOST))
channel = connection.channel()

# Declare queue to send data
channel.queue_declare(queue=cfg.QUEUE_TOPIC)

data = {
"routing_key": "resource.repository",
"src_id": "amqp://gui@finterop.org",
"msg_id": "9b70cd6b-4a2e-45f7-bb28-12cfd9788f16",
"token": "9b70cd6b-4a2e-45f7-bb28-12cfd9788f16",
"timestamp": "1469806702",
"payload":
    {
    "_type": "rr_insert",
    "owner_id": "Mandat",
    "privacy_flag": "false",
    "manufacturer": "Advanticsys",
    "model": "CM5000",
    "hw_platform": "TelosB",
    "mac_id": "00-00-00-00-12-34",
    "power_supply": "1",
    "iut_version": "1.0.0",
    "reference_status": "1",
    "availability_status": "1",
    "ipv6_address": "2001:620:607:5800::2e",
    "media": "IEEE 802.15.4",
    "protocol_name": "CoAP",
    "protocol_version": "18",
    "latitude": "46.2",
    "longitude": "6.15",
    "x": "1",
    "y": "2",
    "z": "3",
    "characteristics_value": "char_value_1",
    "characteristics_unit": "char_unit_1",
    "parameter_name": "param"
    }
}

message = json.dumps(data)

# Send data
channel.basic_publish(exchange='', routing_key=cfg.QUEUE_TOPIC, body=message)
print(" [x] Sent data to RabbitMQ")
connection.close()