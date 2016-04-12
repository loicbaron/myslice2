import logging, json
from tornado import gen, web
from sockjs.tornado import SockJSConnection
from rethinkdb import r
from myslice.lib.util import myJSONEncoder
from myslice.db import changes, connect

logger = logging.getLogger('myslice.websocket')
r.set_loop_type("tornado")

class WebsocketsHandler(SockJSConnection):
    clients = set()

    def on_open(self, request):

        self.clients.add(self)
        logger.info("WebSocket opened (%s)" % request)

    def on_message(self, message):

        logger.info("Received: {}".format(message))
        data = json.loads(message)

        if (data['watch'] == 'activity'):
            self.activity()

    def on_close(self):

        self.clients.remove(self)
        logger.info("WebSocket closed")

    @gen.coroutine
    def activity(self):

        dbconnection = yield connect()
        feed = yield changes(dbconnection, table='activity')

        while (yield feed.fetch_next()):
            change = yield feed.next()
            self.send(json.dumps({ 'activity': change['new_val'] }, ensure_ascii=False, cls=myJSONEncoder).encode('utf8'))

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
