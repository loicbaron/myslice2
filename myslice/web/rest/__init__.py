import json
import re
import logging
import tornado_cors as cors
from tornado import web
import re

import rethinkdb as r

from myslice.db.activity import Event, EventAction, ObjectType, DataType
from myslice.lib.util import myJSONEncoder

logger = logging.getLogger(__name__)

class Api(cors.CorsMixin, web.RequestHandler):

    def initialize(self):
        self.dbconnection = self.application.dbconnection

        self.fields_short = {
            'authorities': [ 'id', 'hrn', 'name', 'shortname', 'status' ],
            'users': [ 'id', 'hrn', 'email', 'first_name', 'last_name', 'shortname', 'authority', 'status' ],
            'projects': [ 'id', 'hrn', 'name', 'shortname', 'authority', 'status', 'label', 'description'],
            'slices': [ 'id', 'hrn',  'name', 'shortname', 'project', 'status', 'label'],
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

    def get_root_auth(self):
        try:
            cursor = yield r.table('authorities').limit(1).run(self.dbconnection)
            while (yield cursor.fetch_next()):
                a = yield cursor.next()
                return a['authority']
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.serverError("unable to find root authority")
            return

    def isAdmin(self):
        auth_pattern = re.compile(r"(urn:publicid:IDN\+)(?P<hrn>[\:]*[a-zA-Z]*)(\+authority\+sa)")
        flag = False
        try:
            # XXX not sure if it is a clean way to decide a admin
            pi_auth = self.get_current_user()['pi_authorities']
            for auth in pi_auth:
                m = auth_pattern.match(auth)
                # User has only Projects and No Authorities under pi_authorities
                if m is None:
                    logger.debug("%s does not match regex" % auth)
                    flag = False
                else:
                    hrn_length = len(m.group('hrn').split(':'))
                    if hrn_length == 1:
                        return True
            return flag
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.serverError("unable to identify user permission")
            return False

    def isUrn(self, urn):
        return re.match(self.application.urn_regex, urn)

    def isEmail(self, email):
        return re.match(self.application.email_regex, email)

    def isHrn(self, hrn):
        return re.match(self.application.hrn_regex, hrn)

    def userError(self, message, debug = None):
        self.set_status(400)
        self.finish({"error": message, "debug": debug})

    def serverError(self, message, debug = None):
        self.set_status(500)
        self.finish({"error": message, "debug": debug})

    def add_pi_users(self, data, object, object_type):
        events = []
        pi_users = []
        # check if the users in the request are in the object
        for data_pi in data['pi_users']:
            if data_pi not in object['pi_users']:
                if isinstance(data_pi, dict):
                    data_pi = data_pi['id']
                pi_users.append(data_pi)
        if len(pi_users)>0:
            # create event add user to object pis
            try:
                event = Event({
                    'action': EventAction.ADD,
                    'user': self.current_user['id'],
                    'object': {'type': object_type, 'id': object['id']},
                    'data': {'type': DataType.PI, 'values': pi_users}
                })
            except Exception as e:
                # TODO: we should log here
                # log.error("Can't create request....")
                logger.error("Can't create event in add_pi_users")
                logger.exception(e)
            else:
                events.append(event)

        return events


    def remove_pi_users(self, data, object, object_type):
        events = []
        pi_users = []
        # check if the users in the object are int the delete request
        for object_pi in object['pi_users']:
            if object_pi not in data['pi_users']:
                if isinstance(object_pi, dict):
                    object_pi = object_pi['id']

                pi_users.append(object_pi)

        if len(pi_users)>0:
            # dispatch event remove pi from object
            try:
                event = Event({
                    'action': EventAction.REMOVE,
                    'user': self.current_user['id'],
                    'object': { 'type': object_type, 'id': object['id'] },
                    'data': { 'type': DataType.PI, 'values': pi_users }
                })
            except Exception as e:
                # TODO: we should log here
                # log.error("Can't create request....")
                logger.error("Can't create event in add_pi_users")
                logger.exception(e)
            else:
                events.append(event)

        return events
