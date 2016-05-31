import json
import logging
import tornado_cors as cors
from rethinkdb import r
from tornado import web, escape

from myslice.db.user import User


logger = logging.getLogger(__name__)

class Api(cors.CorsMixin, web.RequestHandler):

    def initialize(self):
        self.dbconnection = self.application.dbconnection
        #self.set_current_user(None)

    def set_current_user(self, user=None):
        # XXX To be Removed
        user = 'urn:publicid:IDN+onelab:upmc+user+loic_baron'
        if user:
            self.set_secure_cookie("user", escape.json_encode(user))
        else:
            self.clear_cookie("user")

    def get_current_user_id(self):
        #cookie = self.get_secure_cookie("user").decode("utf-8")
        #logger.debug("COOKIE USER ID: {}".format(cookie))
        return None

    def get_current_user(self):
        ret = yield r.table('user').get(self.get_current_user_id()).run(self.dbconnection)
        if not ret:
            self.serverError("Access Denied")

        user = User(ret)

        yield user

    def set_default_headers(self):
        # Allow CORS
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json")

    def userError(self, message, debug = None):
        self.set_status(400)
        self.finish({"error": message, "debug": debug})

    def serverError(self, message, debug = None):
        self.set_status(500)
        self.finish({"error": message, "debug": debug})