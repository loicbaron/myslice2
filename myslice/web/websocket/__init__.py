
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

    def subscribe(self, table=''):
        self.socket.setsockopt_string(zmq.SUBSCRIBE, table)
        return self

    def disconnect(self):
        self.socket.close()

    def isConnected(self):
        return not self.socket.closed


class WebsocketsHandler(SockJSConnection):
    '''
    We are using token as user authentication(Cookie is not offically supported and not secure)
    user token is encrypted and get through rest "/api/v1/usertoken"
    
    Read more for sockjs Auth:
    http://blog.kristian.io/post/47460001334/sockjs-and-tornado-for-python-real-time-web-projects/
    https://groups.google.com/forum/#!topic/sockjs/2iyik3G0PFc

    Example for zeromq:
    https://github.com/svartalf/tornado-zmq-sockjs-example
    https://gist.github.com/abhinavsingh/6378134
    '''

    clients = set()
    context = zmq.Context()
    watch = ['projects', 'activity', 'requests']

    def on_open(self, request):
        self.authenticated = False
        self.clients.add(self)

    def on_message(self, message):
        data = json.loads(message)
        
        if not self.authenticated:
            
            try:
                encrypted_string = data['auth']
            except KeyError as e:
                self.send(
                        json.dumps({
                            'error': 'malformed request',
                            'debug': None,
                            'result': []
                        })
                )
                # close websocket
                self.close()
                return

            try:
                self.auth_user = jwt.decode( encrypted_string, 'u636vbJV6Ph[EJB;Q', algorithms=['HS256'])
            except Exception as e:
                logger.error('Token Decrption errors %s' % e)
                self.send(
                        json.dumps({
                            'error': 'Token Decrption errors',
                            'debug': None,
                            'result': []
                        })
                )
                # close websocket
                self.close()
                return

            else:
                self.authenticated = True
                logger.info("user {} connected".format(self.auth_user['id']))
                return

        if self.authenticated and 'watch' in data:

            logger.info("user {} subscribed to {}".format(self.auth_user['id'], message))
            
            # check if all the specified entities exist
            try:
                watch = data['watch']
            except KeyError as e:
                self.send(
                        json.dumps({
                            'error': 'malformed request',
                            'debug': None,
                            'result': []
                        })
                )
                # close websocket
                self.close()
                return

            # check if all the specified watch exist
            if not watch in self.watch:
                
                self.send(
                     json.dumps({
                         'error': '{} not supported'.format(watch),
                         'debug': None,
                         'result': []
                     })
                 )
                 # close websocket
                self.close()
                return

            if watch == 'activity':
                self.pubsub = ZMQPubSub(self.context, self._activity).connect().subscribe('activity')

            if watch == 'requests':
                self.pubsub = ZMQPubSub(self.context, self._requests).connect().subscribe('activity')

            if watch == 'projects':
                self.pubsub = ZMQPubSub(self.context, self._projects).connect().subscribe('projects')

    def on_close(self):

        # disconnect if watch exists
        if hasattr(self, "pubsub"):
            if not self.pubsub.isConnected():
                self.pubsub.disconnect()

        self.clients.remove(self)
        logger.info("user {} disconnected".format(self.auth_user['id']))


    def _activity(self, message):
        change = json.loads(message[1].decode('utf-8'))

        if  self.auth_user['admin'] or change['user'] == self.auth_user['id'] or \
                ('authority' in change['data'] and ['data']['authority'] in self.auth_user['pi_auth']):
            
            self.send(json.dumps({ 'activity': change }, ensure_ascii=False, cls=myJSONEncoder).encode('utf8'))  


    def _requests(self, message):
        change = json.loads(message[1].decode('utf-8'))

        if change['status'] == "PENDING":

            if  self.auth_user['admin'] or \
                    ('authority' in change['data'] and ['data']['authority'] in self.auth_user['pi_auth']):

                # give the user the right to execute it 
                change.update({"executable": True})

                self.send(json.dumps({ 'request': change }, ensure_ascii=False, cls=myJSONEncoder).encode('utf8'))
                
            if change['user'] == self.auth_user['id']:

                self.send(json.dumps({ 'request': change }, ensure_ascii=False, cls=myJSONEncoder).encode('utf8'))


    def _projects(self, message):
        change = json.loads(message[1].decode('utf-8'))

        if self.auth_user['id'] in change['pi_users']:
            self.send(json.dumps({ 'projects': change }, ensure_ascii=False, cls=myJSONEncoder).encode('utf8'))

            
