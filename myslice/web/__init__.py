import os, logging

from tornado import web, gen, httpserver
from rethinkdb import r
import myslice.db as db
from myslice.web.rest.resource import ResourceHandler
from myslice.web.rest.slice import SliceHandler
from myslice.web.controllers import home

logger = logging.getLogger(__name__)

@gen.coroutine
def server():
    """ Async main method. It needed to be async due to r.connect is async . """
    r.set_loop_type("tornado")
    db_connection = yield db.connect()

    http_server = httpserver.HTTPServer(Application(db_connection))
    http_server.listen(8111)
    #http_server.start(num_processes=None)

    # drop root privileges
    # TODO

class Application(web.Application):

    def __init__(self, dbconnection):
        self.templates = os.path.join(os.path.dirname(__file__), "templates")
        self.static = os.path.join(os.path.dirname(__file__), "static")

        handlers = [
            (r'/', home.Index),
            (r'/static/(.*)', web.StaticFileHandler, {'path': self.static}),

            # REST API
            (r'/api/v1/resource', ResourceHandler),
            (r'/api/v1/resource/(.*)', ResourceHandler),

            (r'/api/v1/slice', SliceHandler),
            (r'/api/v1/slice/(.*)', SliceHandler),

            # WEBSOCKET
        ]

        settings = dict(cookie_secret="x&7G1d2!5MhG9SWkXu",
                        template_path=self.templates,
                        static_path=self.static,
                        xsrf_cookies=True,
                        debug=True)


        self.dbconnection = dbconnection

        web.Application.__init__(self, handlers, **settings)