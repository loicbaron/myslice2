import os, logging

from tornado import web, gen, httpserver
from oauth2 import Provider
from oauth2.error import UserNotAuthenticated
from oauth2.grant import AuthorizationCodeGrant
from oauth2.tokengenerator import Uuid4
from oauth2.store.memory import ClientStore, TokenStore
from oauth2.web import AuthorizationCodeGrantSiteAdapter
from oauth2.web.tornado import OAuth2Handler
from sockjs.tornado import SockJSRouter
from rethinkdb import r
import myslice.db as db
from myslice.web.rest.resources import ResourcesHandler
from myslice.web.rest.slices import SlicesHandler
from myslice.web.rest.users import UsersHandler
from myslice.web.rest.activity import ActivityHandler
from myslice.web.websocket import WebsocketsHandler

from myslice.web.controllers import login, home, activity

logger = logging.getLogger(__name__)

@gen.coroutine
def server():
    """ Async main method. It needed to be async due to r.connect is async . """
    r.set_loop_type("tornado")
    dbconnection = yield db.connect()

    http_server = httpserver.HTTPServer(Application(dbconnection))
    http_server.listen(80)
    #http_server.start(num_processes=None)

    # drop root privileges
    # TODO

class TestSiteAdapter(AuthorizationCodeGrantSiteAdapter):
    """
    This adapter renders a confirmation page so the user can confirm the auth
    request.
    """

    CONFIRMATION_TEMPLATE = """
<html>
    <body>
        <p>
            <a href="{url}&confirm=1">confirm</a>
        </p>
        <p>
            <a href="{url}&confirm=0">deny</a>
        </p>
    </body>
</html>
    """

    def render_auth_page(self, request, response, environ, scopes, client):
        url = request.path + "?" + request.query_string
        response.body = self.CONFIRMATION_TEMPLATE.format(url=url)

        return response

    def authenticate(self, request, environ, scopes, client):
        if request.method == "GET":
            if request.get_param("confirm") == "1":
                return
        raise UserNotAuthenticated

    def user_has_denied_access(self, request):
        if request.method == "GET":
            if request.get_param("confirm") == "0":
                return True
        return False

class Application(web.Application):

    _rest_handlers = ['user', 'project', 'slice']

    def __init__(self, dbconnection):
        self.templates = os.path.join(os.path.dirname(__file__), "templates")
        self.static = os.path.join(os.path.dirname(__file__), "static")

        ##
        # OAuth authentication service (token provider)
        client_store = ClientStore()
        client_store.add_client(client_id="abc", client_secret="xyz",
                                redirect_uris=["http://localhost:8081/callback"])

        token_store = TokenStore()

        provider = Provider(access_token_store=token_store,
                            auth_code_store=token_store, client_store=client_store,
                            token_generator=Uuid4())
        provider.add_grant(AuthorizationCodeGrant(site_adapter=TestSiteAdapter()))

        ##
        # Web
        web_handlers = [
            (provider.authorize_path, OAuth2Handler, dict(provider=provider)),
            (provider.token_path, OAuth2Handler, dict(provider=provider)),

            #(r"/login", login.Index),
            (r'/', home.Index),
            (r'/activity', activity.Index),
            (r'/static/(.*)', web.StaticFileHandler, {'path': self.static}),


        ]

        ##
        # REST API
        rest_handlers = [
            (r'/api/v1/activity$', ActivityHandler),
            (r'/api/v1/activity/([a-z0-9\-]*)$', ActivityHandler),
            (r'/api/v1/resources$', ResourcesHandler),
            (r'/api/v1/resources/()$', ResourcesHandler),
        ]

        ##
        # Websockets API
        # SockJSRouter: configure Websocket
        WebsocketRouter = SockJSRouter(WebsocketsHandler, '/api/v1/live')

        ##
        # URLs handlers
        handlers = web_handlers + rest_handlers + WebsocketRouter.urls

        settings = dict(cookie_secret="x&7G1d2!5MhG9SWkXu",
                        template_path=self.templates,
                        static_path=self.static,
                        #xsrf_cookies=True,
                        debug=True)


        self.dbconnection = dbconnection

        web.Application.__init__(self, handlers, **settings)
