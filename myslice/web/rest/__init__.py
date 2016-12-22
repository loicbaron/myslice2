import json
import re
import logging
import tornado_cors as cors
from tornado import web
import re

from myslice.lib.util import myJSONEncoder

logger = logging.getLogger(__name__)

class Api(cors.CorsMixin, web.RequestHandler):

    def initialize(self):
        self.dbconnection = self.application.dbconnection

        self.fields_short = {
            'authorities': [ 'id', 'hrn', 'name', 'shortname', 'status' ],
            'users': [ 'id', 'hrn', 'email', 'first_name', 'last_name', 'shortname', 'authority', 'status' ],
            'projects': [ 'id', 'hrn', 'name', 'shortname', 'authority', 'status' ],
            'slices': [ 'id', 'hrn',  'name', 'shortname', 'project', 'status'],
            'testbeds': ['id', 'name', 'status', 'type'],
            'resources': ['id', 'name']
        }

        self.fields = {
            'authorities': self.fields_short['authorities'] + [ 'authority', 'pi_users', 'users', 'projects', 'slices', 'created', 'updated', 'enabled'],
            'users': self.fields_short['users'] + [ 'projects', 'slices', 'pi_authorities', 'status', 'created', 'updated', 'enabled'],
            'projects': self.fields_short['projects'] + [ 'pi_users', 'users', 'slices', 'created', 'updated', 'enabled'],
            'slices': self.fields_short['slices'] + [ 'authority', 'users', 'created', 'updated', 'enabled'],
            'profile': ['id', 'email','first_name', 'last_name', 'bio', 'url', 'public_key', 'private_key', 'authority', 'url', 'pi_authorities', 'projects', 'slices'],
            'testbeds': ['id', 'name', 'hostname', 'status', 'type', 'api', 'url', 'version'],
            'resources': ['id', 'name']
        }

        self.fields['profile'] = self.fields['users'] + ['bio', 'url', 'public_key', 'private_key']

        self.threads = self.application.threads

    def get_current_user(self):

        cookie = self.get_secure_cookie("user")
        if not cookie:
            return False

        user = json.loads(str(cookie, "utf-8"))

        return user

    def set_current_user(self, user):
        is_root = False
        is_pi = False
        for auth in user.get('pi_authorities',[]):
            if len(auth.split('+')[1].split(':'))==1:
                is_root = True
                is_pi = True
                break
            elif len(auth.split('+')[1].split(':'))==2:
                is_pi = True

        ##
        # user finally logged in, set cookie
        self.set_secure_cookie("user", str(json.dumps({
            'id': user['id'],
            'email': user['email'],
            'first_name': user.get('first_name', ''),
            'last_name': user.get('last_name', ''),
            'authority': user['authority'],
            'slices': user.get('slices',[]),
            'pi_authorities': user.get('pi_authorities',[]),
            'is_root': is_root,
            'is_pi': is_pi,
        }, cls=myJSONEncoder)))

    def set_default_headers(self):
        # Allow CORS
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json")

    def isAdmin(self):
        auth_pattern = re.compile(r"(urn:publicid:IDN\+)(?P<hrn>[\:]*[a-zA-Z]*)(\+authority\+sa)")
        try:
            # XXX not sure if it is a clean way to decide a admin
            pi_auth = self.get_current_user()['pi_authorities']
            for auth in pi_auth:
                m = auth_pattern.match(auth)
                # User has only Projects and No Authorities under pi_authorities
                if m is None:
                    return False
                hrn_length = len(m.group('hrn').split(':'))
                if hrn_length == 1:
                    return True
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.serverError("unable to identify user permission")
        finally:
            return False

    def isUrn(self, urn):
        return re.match(self.application.urn_regex, urn)

    def isHrn(self, hrn):
        return re.match(self.application.hrn_regex, hrn)

    def userError(self, message, debug = None):
        self.set_status(400)
        self.finish({"error": message, "debug": debug})

    def serverError(self, message, debug = None):
        self.set_status(500)
        self.finish({"error": message, "debug": debug})
