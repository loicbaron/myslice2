import json
import re
import logging
import tornado_cors as cors
from tornado import web


logger = logging.getLogger(__name__)

class Api(cors.CorsMixin, web.RequestHandler):

    def initialize(self):
        self.dbconnection = self.application.dbconnection

        self.fields_short = {
            'authorities': [ 'id', 'hrn', 'name', 'status' ],
            'users': [ 'id', 'hrn', 'email', 'firstname', 'lastname', 'shortname', 'authority', 'status' ],
            'projects': [ 'id', 'hrn', 'name', 'shortname', 'authority', 'status' ],
            'slices': [ 'id', 'hrn',  'name', 'shortname', 'project', 'status' ]
        }

        self.fields = {
            'authorities': self.fields_short['authorities'] + [ 'authority', 'pi_users', 'users', 'projects', 'slices', 'created', 'updated', 'enabled'],
            'users': self.fields_short['users'] + [ 'projects', 'status', 'created', 'updated', 'enabled'],
            'projects': self.fields_short['projects'] + [ 'pi_users', 'users', 'slices', 'created', 'updated', 'enabled'],
            'slices': self.fields_short['slices'] + [ 'authority', 'users', 'created', 'updated', 'enabled']
        }

    def get_current_user(self):

        cookie = self.get_secure_cookie("user")
        if not cookie:
            return False

        user = json.loads(str(cookie, "utf-8"))

        return user

    def set_default_headers(self):
        # Allow CORS
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json")

    def isUrn(self, urn):
        return re.match(self.application.urn_regex, urn)

    def userError(self, message, debug = None):
        self.set_status(400)
        self.finish({"error": message, "debug": debug})

    def serverError(self, message, debug = None):
        self.set_status(500)
        self.finish({"error": message, "debug": debug})
