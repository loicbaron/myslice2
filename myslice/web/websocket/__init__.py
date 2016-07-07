
import jwt
import logging, json

from tornado import gen
from sockjs.tornado import SockJSConnection
from myslice.lib.util import myJSONEncoder

##
# Setup ZMQ with tornado event loop support
import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream
ioloop.install()

logger = logging.getLogger('myslice.websocket')

class ZMQPubSub(object):

    '''
    https://github.com/svartalf/tornado-zmq-sockjs-example
    check pitfall 
    '''

    def __init__(self, context, callback):
        self.context = context
        self.callback = callback

    def connect(self):
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect('tcp://127.0.0.1:6001')
        self.stream = ZMQStream(self.socket)
        self.stream.on_recv(self.callback)

        return self

    def disconnect(self):
        self.socket.close()

    def isConnected(self):
        return not self.socket.closed

    def subscribe(self, table=''):
        self.socket.setsockopt_string(zmq.SUBSCRIBE, table)


class WebsocketsHandler(SockJSConnection):
    '''
    We are using token as user authentication(Cookie is not offically supported and not secure)
    user token is encrypted and get through rest "/api/v1/usertoken"
    
    Read more:
    http://blog.kristian.io/post/47460001334/sockjs-and-tornado-for-python-real-time-web-projects/
    https://groups.google.com/forum/#!topic/sockjs/2iyik3G0PFc
    '''

    clients = set()
    context = zmq.Context()

    def on_open(self, request):
        self.authenticated = False
        self.current_user_id = None
        self.pi_auth = []
        
        self.clients.add(self)
        self.pubsub = ZMQPubSub(self.context, None)

    def on_message(self, message):
        data = json.loads(message)
        
        if not self.authenticated:
            if not 'auth' in data:
                return

            try:
                encrypted_string = data['auth']
                json_object = jwt.decode( encrypted_string, 'u636vbJV6Ph[EJB;Q', algorithms=['HS256'])
            except Exception as e:
                logger.error('Token Decrption errors %s' % e)
                return

            else:
                self.current_user_id = json_object['id']
                self.admin = json_object['admin']
                self.pi_auth = json_object['pi_auth']
                self.authenticated = True
                logger.info("user {} connected".format(self.current_user_id))

        if self.authenticated and 'watch' in data:

            logger.info("user {} subscribed to {}".format(self.current_user_id, message))
            
            if data['watch'] == 'activity':
                self.pubsub = ZMQPubSub(self.context, self._activity).connect()
                self.pubsub.subscribe('activity')

            if data['watch'] == 'requests':
                self.pubsub = ZMQPubSub(self.context, self._requests).connect()
                self.pubsub.subscribe('activity')

            if data['watch'] == 'projects':
                self.pubsub = ZMQPubSub(self.context, self._projects).connect()
                self.pubsub.subscribe('projects')

    def on_close(self):
        if not self.pubsub.isConnected():
            self.pubsub.disconnect()

        self.clients.remove(self)
        logger.info("user {} disconnected".format(self.current_user))


    def _activity(self, message):
        change = json.loads(message[1].decode('utf-8'))
        
        if  self.admin or change['user'] == self.current_user_id or \
            ('authority' in change['data'] and ['data']['authority'] in self.pi_auth):
            
            self.send(json.dumps({ 'activity': change }, ensure_ascii=False, cls=myJSONEncoder).encode('utf8'))  

    def _requests(self, message):
        change = json.loads(message[1].decode('utf-8'))

        if change['status'] == "PENDING":

            if  self.admin or \
                ('authority' in change['data'] and ['data']['authority'] in self.pi_auth):

                # give the user the right to execute it 
                change.update({"executable": True})

                self.send(json.dumps({ 'request': change }, ensure_ascii=False, cls=myJSONEncoder).encode('utf8'))
                
            if change['user'] == self.current_user_id:

                self.send(json.dumps({ 'request': change }, ensure_ascii=False, cls=myJSONEncoder).encode('utf8'))

    def _projects(self, message):
        change = json.loads(message[1].decode('utf-8'))

        if self.current_user in change['pi_users']:
            self.send(json.dumps({ 'projects': change }, ensure_ascii=False, cls=myJSONEncoder).encode('utf8'))

            
