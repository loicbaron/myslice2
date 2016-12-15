import os, logging

from tornado import web, gen, httpserver

from oauth2 import Provider
from oauth2.web.tornado import OAuth2Handler
from oauth2.grant import AuthorizationCodeGrant, ImplicitGrant
from oauth2.tokengenerator import Uuid4
from oauth2.store.memory import ClientStore, TokenStore

from sockjs.tornado import SockJSRouter
from rethinkdb import r
import myslice.db as db

##
# Authenticaction handler
from myslice.web.controllers.authorization import CodeGrant

##
# REST handlers
from myslice.web.rest.requests import RequestsHandler

from myslice.web.rest.testbeds import TestbedsHandler
from myslice.web.rest.authorities import AuthoritiesHandler
from myslice.web.rest.projects import ProjectsHandler
from myslice.web.rest.slices import SlicesHandler
from myslice.web.rest.users import UsersHandler, ProfileHandler, LoginHandler, UserTokenHandler
from myslice.web.rest.resources import ResourcesHandler
from myslice.web.rest.leases import LeasesHandler
from myslice.web.rest.password import PasswordHandler

from myslice.web.rest.finterop.sessions import SessionsHandler as FinteropSessionsHandler

from myslice.web.rest.activity import ActivityHandler

##
# WebSocket handler
from myslice.web.websocket import WebsocketsHandler

##
# Web controllers
from myslice.web.controllers import login, logout, password, registration, home, activity, projects, slices, users, status, addOrganization
from myslice.web.controllers import test

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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


#
# http://localhost:8111/authorize?response_type=token&client_id=abc&redirect_uri=http%3A%2F%2Flocalhost%3A8111%2Fevents&scope=scope_write

class Application(web.Application):
    urn_regex = "urn:[a-z0-9][a-z0-9-]{0,31}:[a-zA-Z0-9()+,\-.:=@;$_!*'%?#]+"
    uuid_regex = "[a-fA-F\d]{8}-[a-fA-F\d]{4}-[a-fA-F\d]{4}-[a-fA-F\d]{4}-[a-fA-F\d]{12}"
    hrn_regex = "[a-zA-Z0-9\-\.\_]+"

    threads = {}

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
                                redirect_uris=["http://localhost:8111"])

        ##
        # OAuth Token Store (in memory)
        token_store = TokenStore()

        # Generator of tokens
        token_generator = Uuid4()
        #token_generator.expires_in[ClientCredentialsGrant.grant_type] = 3600

        ##
        # OAuth Provider
        provider = Provider(
            access_token_store=token_store,
            auth_code_store=token_store,
            client_store=client_store,
            token_generator=token_generator
        )

        #provider.token_path = '/oauth/token'

        # Support for the authorization code grant
        provider.add_grant(
            AuthorizationCodeGrant(site_adapter=CodeGrant(self.templates))
        )
        # provider.add_grant(
        #     ImplicitGrant(site_adapter=Authentication())
        # )

        logger.debug(provider.authorize_path)
        logger.debug(provider.token_path)
        ##
        # Auth handlers
        auth_handlers = [
            web.url(provider.authorize_path, OAuth2Handler, dict(provider=provider)),
            web.url(provider.token_path, OAuth2Handler, dict(provider=provider))
        ]

        ##
        # Web
        web_handlers = [
            web.url(r"/login", login.Index),
            web.url(r"/logout", logout.Index),
            web.url(r"/password/(.*)", password.Index),
            web.url(r"/forgot_password", password.Forgot),
            web.url(r"/registration", registration.Index),
            web.url(r'/', home.Index),
            web.url(r'/settings', home.User),
            web.url(r'/projects', projects.Projects),
            web.url(r'/slices/([a-z0-9\._\-]+)', slices.Slices),
            web.url(r'/users', users.Users),
            web.url(r'/activity', activity.Index),
            web.url(r'/status', status.Index),
            web.url(r'/static/(.*)', web.StaticFileHandler, {'path': self.static}),
            web.url(r'/test', test.Index),
            web.url(r"/addOrganization", addOrganization.Index)

        ]


        ##
        # REST API

        rest_handlers = [

            web.url(r'/api/v1/activity?([A-Za-z0-9-]+)?', ActivityHandler),
            web.url(r'/api/v1/activity/(' + self.uuid_regex + ')?', ActivityHandler),

            web.url(r'/api/v1/requests?([A-Za-z0-9-]+)?', RequestsHandler),
            web.url(r'/api/v1/requests/(' + self.uuid_regex + ')?', RequestsHandler),
            web.url(r'/api/v1/usertoken?', UserTokenHandler),

            web.url(r'/api/v1/login', LoginHandler),
            web.url(r'/api/v1/password', PasswordHandler),
            web.url(r'/api/v1/password/(.*)', PasswordHandler),

            web.url(r'/api/v1/resources$', ResourcesHandler),
            web.url(r'/api/v1/resources/(' + self.urn_regex + ')?$', ResourcesHandler),
            web.url(r'/api/v1/resources/(' + self.urn_regex + ')?/?(leases)?$', ResourcesHandler),
            web.url(r'/api/v1/resources/(' + self.urn_regex + ')?/?(slices)?$', ResourcesHandler),
            web.url(r'/api/v1/resources/(' + self.urn_regex + ')?/?(testbeds)?$', ResourcesHandler),
            # leases
            web.url(r'/api/v1/leases$', LeasesHandler),
            web.url(r'/api/v1/leases/([A-Za-z0-9-]+)?', LeasesHandler),
            web.url(r'/api/v1/profile$', ProfileHandler),
            # testbeds
            web.url(r'/api/v1/testbeds/?(' + self.urn_regex + ')?/?(resources)?$', TestbedsHandler),
            web.url(r'/api/v1/testbeds/?(' + self.urn_regex + ')?/?(leases)?$', TestbedsHandler),
            # users
            web.url(r'/api/v1/users$', UsersHandler),
            web.url(r'/api/v1/users/?(' + self.urn_regex + ')?/?(authorities|projects|slices)?$', UsersHandler),
            web.url(r'/api/v1/users/?(authorities|projects|slices)?$', UsersHandler),
            # authorities
            web.url(r'/api/v1/authorities$', AuthoritiesHandler),
            web.url(r'/api/v1/authorities/?(' + self.urn_regex + ')?/?(users|projects)?$', AuthoritiesHandler),
            # projects
            web.url(r'/api/v1/projects/?(' + self.urn_regex + ')?/?(users|slices)?$', ProjectsHandler),
            # slices
            web.url(r'/api/v1/slices/?(' + self.hrn_regex + ')?/?(users|resources)?$', SlicesHandler),
            web.url(r'/api/v1/slices/?(' + self.urn_regex + ')?/?(users|resources)?$', SlicesHandler),

            # F-Interop sessions
            # security based on the slice id
            web.url(r'/api/v1/finterop/sessions/?(' + self.urn_regex + ')?/?(start|stop)?$', FinteropSessionsHandler),
            web.url(r'/api/v1/finterop/sessions/?(' + self.hrn_regex + ')?/?(start|stop)?$', FinteropSessionsHandler),
            web.url(r'/api/v1/finterop/sessions/?([a-zA-Z0-9]+)?/?(start|stop)?$', FinteropSessionsHandler),

        ]

        ##
        # Websockets API
        # SockJSRouter: configure Websocket
        WebsocketRouter = SockJSRouter(WebsocketsHandler, '/api/v1/live')

        ##
        # URLs handlers
        handlers = auth_handlers + web_handlers + rest_handlers + WebsocketRouter.urls

        settings = dict(cookie_secret="x&7G1d2!5MhG9SWkXu",
                        login_url="/login",
                        token_secret = 'u636vbJV6Ph[EJB;Q',
                        template_path=self.templates,
                        static_path=self.static,
                        #xsrf_cookies=True,
                        debug=True)

        web.Application.__init__(self, handlers, **settings)
