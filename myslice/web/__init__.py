import os, logging

from tornado import web, gen, httpserver
from rethinkdb import r
from myslice import settings as s
from myslice.web.rest.resource import ResourceHandler
from myslice.web.controllers import home, jobs

logger = logging.getLogger(__name__)

@gen.coroutine
def server():
    """ Async main method. It needed to be async due to r.connect is async . """
    logger.info("Connecting to db {} on {}:{}".format(s.db.name,s.db.host,s.db.port))
    try :
        r.set_loop_type("tornado")
        dbconnection = yield r.connect(host=s.db.host, port=s.db.port, db=s.db.name)
    except r.RqlDriverError :
        logger.error("Can't connect to RethinkDB")
        raise SystemExit("Can't connect to RethinkDB")

    http_server = httpserver.HTTPServer(Application(dbconnection))
    http_server.listen(8111)

class Application(web.Application):

    def __init__(self, dbconnection):
        self.templates = os.path.join(os.path.dirname(__file__), "templates")
        self.static = os.path.join(os.path.dirname(__file__), "static")

        handlers = [
            (r'/', home.Index),
            (r'/static/(.*)', web.StaticFileHandler, {'path': self.static}),
            (r'/jobs', jobs.Log),

            (r'/api/resource', ResourceHandler),
            (r'/api/resource/(.*)', ResourceHandler),
        ]

        settings = dict(cookie_secret="_asdfasdaasdfasfas",
                        template_path=self.templates,
                        static_path=self.static,
                        xsrf_cookies=True,
                        debug=True)


        self.dbconnection = dbconnection

        web.Application.__init__(self, handlers, **settings)