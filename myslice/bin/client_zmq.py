import zmq

from multiprocessing import Process

import json
import pickle

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
        change = pickle.loads(msg)
        print("{0}: {1}".format(topic, change))
        print("{0}: {1}".format(type(topic), type(change)))
        print(type(change))
        print(change)


if __name__ == '__main__':
    Process(target=client,).start()