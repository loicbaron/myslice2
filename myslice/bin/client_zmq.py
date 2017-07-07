import zmq

from multiprocessing import Process

import json

def on_message(message):
    print(message)


def client():
    # create context
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt_string(zmq.SUBSCRIBE, 'activity')
    socket.connect("tcp://localhost:6002")

    print("Collecting updates from weather server…")
    should_continue = True
    while should_continue:
        topic, msg = socket.recv_multipart()
        print("{0}: {1}".format(topic, msg.decode('utf-8')))
        change = json.loads(msg.decode('utf-8'))
        print(type(change))
        print(change)


if __name__ == '__main__':
    Process(target=client,).start()