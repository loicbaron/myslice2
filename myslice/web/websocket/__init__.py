import logging, json
from tornado import gen
from sockjs.tornado import SockJSConnection
from myslice.lib.util import myJSONEncoder
from myslice.db import changes, connect, tables

##
# Setup ZMQ with tornado event loop support
import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream
ioloop.install()

logger = logging.getLogger('myslice.websocket')

class ZMQPubSub(object):

    def __init__(self, callback):
        self.callback = callback

    def connect(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)

        self.socket.connect('tcp://127.0.0.1:6001')
        self.stream = ZMQStream(self.socket)
        self.stream.on_recv(self.callback)

    def disconnect(self):
        self.socket.close()

    def isConnected(self):
        return not self.socket.closed

    def subscribe(self, channel_id=b''):
        self.socket.setsockopt(zmq.SUBSCRIBE, channel_id)


class WebsocketsHandler(SockJSConnection):
    clients = set()
    current_user = 'urn:publicid:IDN+onelab:upmc+user+loic_baron'

    def on_open(self, request):
        self.clients.add(self)
        self.pubsub = ZMQPubSub(self.on_data)
        self.pubsub.connect()
        logger.info("user {} connected".format(self.current_user))

    def on_message(self, message):
        logger.info("user {} subscribed to {}".format(self.current_user, message))
        data = json.loads(message)

        # watch is a list of tables to watch
        try:
            self.watch = data['watch']
        except Exception:
            self.send(
                json.dumps({
                    'error': 'malformed request',
                    'debug': None,
                    'result': []
                })
            )
            # close websocket
            self.close()

        # check if all the specified entities exist
        for w in self.watch:
            if w not in tables:
                self.send(
                    json.dumps({
                        'error': '{} not supported'.format(w),
                        'debug': None,
                        'result': []
                    })
                )
                # close websocket
                self.close()

        # subscribe to the zmq socket
        if self.pubsub.isConnected():
            self.pubsub.subscribe()

    def on_close(self):
        if not self.pubsub.isConnected():
            self.pubsub.disconnect()

        self.clients.remove(self)
        logger.info("user {} disconnected".format(self.current_user))

    def on_data(self, data):
        for d in data:
            o = json.loads(str(d, "utf-8"))

            #for k in o:

            # filter by user (current_user)


            # only send relevant info
            if self.watch in o:
                self.send(json.dumps(o[self.watch], ensure_ascii=False, cls=myJSONEncoder))

    def _activity(self):
        pass

    def _projects(self):
        pass




    @gen.coroutine
    def activity(self, obj=None):

        dbconnection = yield connect()
        feed = yield changes(dbconnection, table='activity')

        while (yield feed.fetch_next()):
            change = yield feed.next()
            print('--->  websocket activity()')
            print(change)
            print(obj)
            if obj:
                if change['new_val']['object']['type'] == obj:
                    if change['new_val']['user'] == self.current_user:
                        self.send(json.dumps({ 'activity': change['new_val'] }, ensure_ascii=False, cls=myJSONEncoder).encode('utf8'))
            else:
                if change['new_val']['user'] == self.current_user:
                    self.send(json.dumps({ 'activity': change['new_val'] }, ensure_ascii=False, cls=myJSONEncoder).encode('utf8'))

    @gen.coroutine
    def projects(self):

        dbconnection = yield connect()
        feed = yield changes(dbconnection, table='projects')

        while (yield feed.fetch_next()):
            change = yield feed.next()
            # public projects
            # protected projects where user is memberi/PI of the authority
            # projects where user is PI (including private)
            if self.current_user in change['new_val']['pi_users']:
                self.send(json.dumps({ 'projects': change['new_val'] }, ensure_ascii=False, cls=myJSONEncoder).encode('utf8'))