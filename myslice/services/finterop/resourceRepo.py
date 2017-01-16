#!/usr/bin/env python3.5
import logging
import pika
import json
import config as cfg
import uuid

# Connect to RabbitMQ and create channel

class ResourceRepo():

    def __init__(self):
        credentials = pika.PlainCredentials(username=cfg.USERNAME, password=cfg.PASSWORD)
        parameters = pika.ConnectionParameters(host=cfg.RABBIT_HOST,
                                               port=5672,
                                               virtual_host=cfg.VHOST,
                                               credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

            # Declare queue to get response
        result = self.channel.queue_declare(exclusive=True,auto_delete=True)
        self.queue_name = result.method.queue

        # Bind queue to routing_key
        self.channel.queue_bind(queue=self.queue_name,
                                exchange='default',
                                routing_key='control.resource_repository.service.reply')

        # Register consume callback
        self.channel.basic_consume(self.on_response,
                                   no_ack=True,
                                   queue=self.queue_name)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def make_request(self, message):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        # Send message
        self.channel.basic_publish(exchange='default',
                                   routing_key='control.resource_repository.service',
                                   properties=pika.BasicProperties(
                                       reply_to='control.resource_repository.service.reply',
                                       correlation_id=self.corr_id,
                                       content_type='application/json'
                                   ),
                                   body=json.dumps(message))
        # Wait for response
        while self.response is None:
            self.connection.process_data_events()
        return self.response

if __name__ == '__main__':
    client = ResourceRepo()

    # get_filepath = 'json/query_1.json'
    insert_filepath = 'json/insert_resource_v5_1.json'
    with open(insert_filepath) as json_data:
        # Load json request from file
        json_request = json.load(json_data)
        print("Request message: {}".format(json.dumps(json_request, indent=2)))

        # Execute request
        response = client.make_request(json_request)

        # Load response as json
        json_response = json.loads(response.decode('utf8'))
        print("Response message: {}".format(json.dumps(json_response, indent=2)))


