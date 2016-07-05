import zmq
import jwt
import logging, json

from tornado import gen
from sockjs.tornado import SockJSConnection
from rethinkdb import r
from myslice.lib.util import myJSONEncoder
from myslice.db import changes, connect

logger = logging.getLogger('myslice.websocket')
r.set_loop_type("tornado")

class WebsocketsHandler(SockJSConnection):
    '''
    We are using token as user authentication(Cookie is not offically supported and not secure)
    user token is encrypted and get through rest "/api/v1/usertoken"
    
    Read more:
    http://blog.kristian.io/post/47460001334/sockjs-and-tornado-for-python-real-time-web-projects/
    https://groups.google.com/forum/#!topic/sockjs/2iyik3G0PFc
    '''

    clients = set()
    #zmq_publisher = 'tcp://127.0.0.1:6001'

    def on_open(self, request):
        self.authenticated = False
        self.current_user_id = None
        self.pi_auth = []
        self.clients.add(self)
        logger.info("WebSocket opened (%s)" % request)

    def on_message(self, message):
        logger.info("Received: {}".format(message))
        data = json.loads(message)
        print(data)
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

        if self.authenticated and 'watch' in data:
            if data['watch'] == 'activity':
                self.activity()

            if data['watch'] == 'requests':
                self.requests()

            if data['watch'] == 'projects':
                self.projects()

    def on_close(self):
        self.clients.remove(self)
        logger.info("WebSocket closed")


    @gen.coroutine
    def requests(self, obj=None):
        
        dbconnection = yield connect()
        feed = yield changes(dbconnection, table='activity')

        while (yield feed.fetch_next()):
            change = yield feed.next()

            # if obj:
            #     if change['new_val']['object']['type'] == obj:
            #         if change['new_val']['user'] == self.current_user_id:
            #             self.send(json.dumps({ 'activity': change['new_val'] }, ensure_ascii=False, cls=myJSONEncoder).encode('utf8'))
            # else:
            if change['new_val']['status'] == "PENDING":
                
                # 
                if  self.admin or \
                    change['new_val']['data']['authority'] in self.pi_auth:

                    activity = change['new_val']
                    activity.update({"executable": True})

                    self.send(json.dumps({ 'request': change['new_val'] }, ensure_ascii=False, cls=myJSONEncoder).encode('utf8'))
                    
                if change['new_val']['user'] == self.current_user_id:
 
                    self.send(json.dumps({ 'request': change['new_val'] }, ensure_ascii=False, cls=myJSONEncoder).encode('utf8'))

    @gen.coroutine
    def activity(self):

        # try:
        #     context = zmq.Context()
        #     sock = context.socket(zmq.SUB)
        #     sock.connect(self.zmq_publisher)

        # except Exception as e:
        #     logger.error('Error happens when setting a ZeroMQ client (%s)' % e)
        # else:
        #     json = sock.recv_json(ensure_ascii=False, cls=myJSONEncoder)

        #     print(json)

        
        dbconnection = yield connect()
        feed = yield changes(dbconnection, table='activity')

        while (yield feed.fetch_next()):
            change = yield feed.next()

            # if obj:
            #     if change['new_val']['object']['type'] == obj:
            #         if change['new_val']['user'] == self.current_user_id:
            #             self.send(json.dumps({ 'activity': change['new_val'] }, ensure_ascii=False, cls=myJSONEncoder).encode('utf8'))
            # else:

            if  self.admin or \
                change['new_val']['data']['authority'] in self.pi_auth or \
                change['new_val']['user'] == self.current_user_id:
                
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

    # @gen.coroutine
    # def jobs(self):
    #     conn = None
    #     try :
    #         conn = yield r.connect(host="localhost", port=28015)
    #     except r.RqlDriverError :
    #         logger.error("can't connect to RethinkDB")
    #         self.write_message(json.dumps({ "ret" : 0, "msg" : "connection error" }, ensure_ascii = False))
    #
    #     if (conn) :
    #         feed = yield r.db("myslice").table("jobs").changes().run(conn)
    #         while (yield feed.fetch_next()):
    #             change = yield feed.next()
    #             #self.write_message(json.dumps(change['new_val'], ensure_ascii = False).encode('utf8'))
    #             self.write_message(json.dumps(change['new_val']))
