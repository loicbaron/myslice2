import os, logging

from tornado import web, gen, httpserver
from rethinkdb import r
import myslice.db as db
from myslice.web.rest.resource import ResourceHandler
from myslice.web.rest.slice import SliceHandler
from myslice.web.rest.user import UserHandler
from myslice.web.controllers import home

logger = logging.getLogger(__name__)

@gen.coroutine
def server():
    """ Async main method. It needed to be async due to r.connect is async . """
    r.set_loop_type("tornado")
    db_connection = yield db.connect()

    http_server = httpserver.HTTPServer(Application(db_connection))
    http_server.listen(80)
    #http_server.start(num_processes=None)

    # drop root privileges
    # TODO

class Application(web.Application):

    _rest_handlers = ['user', 'project', 'slice']

    def __init__(self, dbconnection):
        self.templates = os.path.join(os.path.dirname(__file__), "templates")
        self.static = os.path.join(os.path.dirname(__file__), "static")

        handlers = [
            (r'/', home.Index),
            (r'/static/(.*)', web.StaticFileHandler, {'path': self.static}),
        ]

        # REST API
        for entity in self._rest_handlers:
            # import handler class
            HandlerModule = "myslice.web.rest.{}".format(entity)
            HandlerClass = "{}Handler".format(entity.title())
            module = __import__(HandlerModule, fromlist=[HandlerClass])
            Handler = getattr(module, HandlerClass)
            
            # append handler to list of handlers 
            handlers += [
                    (r'/api/v1/{}s'.format(entity), Handler),
                    (r'/api/v1/{}s/(.*)'.format(entity), Handler)
            ]

        # WEBSOCKET

        settings = dict(cookie_secret="x&7G1d2!5MhG9SWkXu",
                        template_path=self.templates,
                        static_path=self.static,
                        #xsrf_cookies=True,
                        debug=True)

        self.dbconnection = dbconnection

        web.Application.__init__(self, handlers, **settings)