import os, logging

from tornado import web, gen, httpserver
from oauth2 import Provider
from oauth2.grant import ClientCredentialsGrant
from oauth2.tokengenerator import Uuid4
from oauth2.store.memory import ClientStore, TokenStore
from sockjs.tornado import SockJSRouter
from rethinkdb import r
import myslice.db as db
from myslice.web.authentication import OAuth2Handler, AuthHandler
from myslice.web.rest.resource import ResourceHandler
from myslice.web.rest.slice import SliceHandler
from myslice.web.rest.user import UserHandler
from myslice.web.rest.activity import ActivityHandler
from myslice.web.websocket import WebsocketsHandler

from myslice.web.controllers import login, home, activity

import json

logger = logging.getLogger(__name__)

class FooHandler(AuthHandler):
    def get(self):
        self.finish(json.dumps({'msg': 'This is Foo!'}))

@gen.coroutine
def run():
    """
    Tornado Web Server launcher
    :return:
    """
    # Rethinkdb setting for tornado
    r.set_loop_type("tornado")
    dbconnection = yield db.connect()

    http_server = httpserver.HTTPServer(Application(dbconnection))
    http_server.listen(8111)
    #http_server.start(num_processes=None)

    # drop root privileges
    # TODO

class Application(web.Application):

    def __init__(self, dbconnection):
        self.templates = os.path.join(os.path.dirname(__file__), "../templates")
        self.static = os.path.join(os.path.dirname(__file__), "../static")

        # DataBase connection
        self.dbconnection = dbconnection

        ##
        # OAuth authentication service (token provider)
        # Client Store (will be taken from db)
        client_store = ClientStore()
        client_store.add_client(client_id="abc",
                                client_secret="xyz",
                                redirect_uris=["http://localhost:8081/callback"])

        ##
        # OAuth Token Store (in memory)
        token_store = TokenStore()

        # Generator of tokens
        token_generator = Uuid4()
        token_generator.expires_in[ClientCredentialsGrant.grant_type] = 3600

        ##
        # OAuth Provider
        provider = Provider(access_token_store=token_store,
                            auth_code_store=token_store,
                            client_store=client_store,
                            token_generator=token_generator)
        provider.token_path = '/oauth/token'
        provider.add_grant(ClientCredentialsGrant())

        ##
        # Auth handlers
        auth_handlers = [
            #(provider.authorize_path, OAuth2Handler, dict(provider=provider)),
            #(provider.token_path, OAuth2Handler, dict(provider=provider)),

            (r'/oauth/token', OAuth2Handler, dict(controller=provider)),
            (r'/foo', FooHandler, dict(controller=provider))
        ]

        ##
        # Web
        web_handlers = [

            (r"/login", login.Index),
            (r'/', home.Index),
            (r'/activity', activity.Index),
            (r'/static/(.*)', web.StaticFileHandler, {'path': self.static}),


        ]

        ##
        # REST API
        rest_handlers = [
            (r'/api/v1/activity', ActivityHandler),

            (r'/api/v1/project', ProjectHandler),
            (r'/api/v1/projects', ProjectsHandler),
        ]

        ##
        # Websockets API
        # SockJSRouter: configure Websocket
        WebsocketRouter = SockJSRouter(WebsocketsHandler, '/api/v1/live')

        ##
        # URLs handlers
        handlers = auth_handlers + web_handlers + rest_handlers + WebsocketRouter.urls

        settings = dict(cookie_secret="x&7G1d2!5MhG9SWkXu",
                        template_path=self.templates,
                        static_path=self.static,
                        #xsrf_cookies=True,
                        debug=True)

        web.Application.__init__(self, handlers, **settings)