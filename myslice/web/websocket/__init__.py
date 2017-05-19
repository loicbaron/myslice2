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

##
# WebSocket MySlice protocol API
from myslice.web.websocket.api import Request, Response, ResponseError, Stream

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
        logger.info("subscribing to: {}".format(table))
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
    watch = ['projects', 'activity', 'requests', 'sessions', 'messages']
    filter = {}

    def on_open(self, request):
        logger.debug(request)
        self.authenticated = False
        self.clients.add(self)

    def api_data(self):
        pass

    def api_message(self, payload):
        self.send(payload.json())

    def api_error(self, payload):
        logger.debug("api_error: %s" % payload)
        self.send(payload)

    def api_fatal(self, payload):
        self.api_error(payload)
        #self.close()

    def on_message(self, message):
        '''
        Manage incoming messages.
        :param message:
        :return:
        '''

        try:
            request = Request(message)
        except Exception as e:
            ##
            # API protocol failure (bad command)
            # TODO: Create specific exceptions
            import traceback
            traceback.print_exc()
            self.api_fatal(json.dumps({ "result": { "code": -1, "message": "API error: {}".format(str(e)) }} ))
        else:
            if request.isAuthenticating():
                ##
                # Authentication
                try:
                    self.authenticated_user = jwt.decode(request.token, 'u636vbJV6Ph[EJB;Q', algorithms=['HS256'])
                except Exception as e:
                    self.api_fatal(
                        ResponseError(request, str(e))
                    )
                else:
                    self.authenticated = True
                    logger.info("user {} connected".format(self.authenticated_user['id']))
                    self.api_message(
                        Response(request, "connected")
                    )
            elif self.authenticated:
                ##
                # User is already authenticated
                if request.isWatching():
                    logger.info("user {} is watching {}".format(self.authenticated_user['id'], request.object))
                    logger.info(type(request.object))
                    if request.object == "activity":
                        f = {"user":self.authenticated_user['id']}
                        self.filter = {**self.filter, **f} 
                    self.pubsub = ZMQPubSub(self.context, self.on_change).connect().subscribe(request.object.__str__())
                    self.api_message(
                        Response(request, "watching {}".format(request.object))
                    )
                    pass
                elif request.isUnwatching():
                    pass
                elif request.isCounting():
                    pass
                elif request.isFiltering():
                    logger.info("user {} is filtering {}".format(self.authenticated_user['id'], request.filter))
                    self.filter = {**self.filter, **request.filter} 
            else:
                ##
                # User is not authenticated (error)
                self.api_fatal(
                    ResponseError(request, "Not authenticated")
                )


    def on_close(self):

        # disconnect if watch exists
        if hasattr(self, "pubsub"):
            if not self.pubsub.isConnected():
                self.pubsub.disconnect()

        self.clients.remove(self)
        logger.info("user {} disconnected".format(self.authenticated_user['id']))

    def on_change(self, zmqmessage):
        '''
        This is a callback function that will be called when we receive data on the ZMQ socket.
        ATM there is not filter, but the data should be filtered according to the user authorisations.

        :param message:
        :return:
        '''
        logger.debug("got message")
        logger.info(zmqmessage)
        object = zmqmessage[0].decode('utf-8')
        change = json.loads(zmqmessage[1].decode('utf-8'))

        # dirty work around to prevent processing empty
        # objects (during delete)
        if not change:
            return

        # XXX WIP FILTER 
        if self.filter:
            flag = False
            for key, value in self.filter.items():
                if key in change and change[key] == value:
                    flag = True
                    break
                else:
                    flag = False
        else:
            flag = True

        if flag:
            stream = Stream(
                command="watch",
                object=object,
                data=change,
                event="updated"
            )
            self.send(stream.json().encode('utf8'))
