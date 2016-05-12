import logging
import tornado_cors as cors
from tornado import web, escape

logger = logging.getLogger(__name__)

class Api(cors.CorsMixin, web.RequestHandler):

    def initialize(self):
        self.dbconnection = self.application.dbconnection

    def set_current_user(self, user):
        user = 'urn:publicid:IDN+onelab:upmc+user+loic_baron'
        if user:
            self.set_secure_cookie("user", escape.json_encode(user))
        else:
            self.clear_cookie("user")

    def get_current_user(self):
        cookie = self.get_secure_cookie("user").decode("utf-8")
        logger.debug("COOKIE USER ID: {}".format(cookie))
        return cookie

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