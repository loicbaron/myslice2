import json
import logging
from email.utils import parseaddr
import uuid

import rethinkdb as r
import myslice.db as db
from myslice.db import dispatch, changes
from myslice.lib.util import myJSONEncoder
from myslice.db.activity import Event, EventAction, ObjectType
from myslice.db.user import User
from myslice.web.rest import Api
from myslice.web.controllers.login import check_password, crypt_password

from tornado import gen, escape

logger = logging.getLogger('myslice.rest.password')

class PasswordHandler(Api):

    @gen.coroutine
    def put(self):
        """
        PUT /password
        :return:
        """
        if not self.request.body:
            self.userError("empty request")
            return

        try:
            data = escape.json_decode(self.request.body)
        except json.decoder.JSONDecodeError as e:
            self.userError("Malformed request", e)
            return
        except Exception as e:
            self.userError("Malformed request", e)
            return

        if 'old_password' in data:
            p = bytes(data['old_password'], 'latin-1')

            if not check_password(data['old_password'], user['password']):
                self.userError("password does not match")
                return

        if not data['new_password']:
            self.userError("Malformed request")
            return        

        user_id = self.get_current_user()['id']
        try:
            user = yield r.table('users').get(user_id).run(self.application.dbconnection)
        except Exception as e:
            self.userError("User does not exists")
            return

        # Directly modify the database, no need to go through Events
        user['password'] = crypt_password(data['new_password'])
        yield r.table('users').update(user).run(self.dbconnection)

        #event = Event({
        #    'action': EventAction.UPDATE,
        #    'user': user_id,
        #    'object': {
        #        'type': ObjectType.USER,
        #        'id': user_id
        #    },
        #    'data': {
        #        "password": crypt_password(data['new_password']),
        #        "generate_keys": False
        #    }
        #})
        #yield dispatch(self.dbconnection, event)

        self.write(json.dumps(
                {
                    "result": "success",
                    "error": None,
                    "debug": None
                }, cls=myJSONEncoder))

    @gen.coroutine
    def post(self, hashing=None):
        """
        POST /password[/<hashing>]
        :return:
        """
        if not self.request.body:
            self.userError("empty request")
            return

        try:
            data = escape.json_decode(self.request.body)
        except json.decoder.JSONDecodeError as e:
            self.userError("Malformed request", e)
            return
        except Exception as e:
            self.userError("Malformed request", e)
            return

        try:
            # NEW Event UPDATE PASSWORD
            if not hashing:
                if not 'email' in data:
                    self.userError("Email not specified")
                    return

                if not 'hashing' in data:
                    data['hashing'] = str(uuid.uuid4())

                user = None
                cursor = yield r.table('users').filter({'email':data['email']}).run(self.dbconnection)
                while (yield cursor.fetch_next()):
                    user = yield cursor.next()
                if not user:
                    self.userError("no user found or permission denied")
                    return
                event = Event({
                    'action': EventAction.CREATE,
                    'user': None,
                    'object': {
                        'type': ObjectType.PASSWORD,
                        'id': user['id'] 
                    },
                    'data': data
                })

            # APPROVE Event UPDATE PASSWORD
            else:
                if not 'password' in data:
                    self.userError("Password not specified")
                    return

                # Find the Event based on the hashing
                cursor = yield r.table('activity').filter(lambda ev:
                                                           ev["data"]["hashing"] == hashing
                                                           ).run(self.application.dbconnection)
                while (yield cursor.fetch_next()):
                    ev = yield cursor.next()
                event = Event(ev)
               
                user = None
                cursor = yield r.table('users').filter({'email':event.data['email']}).run(self.dbconnection)
                while (yield cursor.fetch_next()):
                    user = yield cursor.next()
                if not user:
                    self.userError("user not found or permission denied")
                    return

                #user = User(user)
                # Crypt password
                new_password = crypt_password(data['password'])
                event.data['password'] = new_password
                event.setApproved()

        except Exception as e:
            self.userError("Can't create request", e)
            return
        else:
            result = yield dispatch(self.dbconnection, event)
            self.write(json.dumps(
                {
                    "result": "success",
                    "error": None,
                    "debug": None
                 }, cls=myJSONEncoder))
