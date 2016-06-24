import json
from email.utils import parseaddr
import crypt
from hmac import compare_digest as compare_hash
import uuid

import rethinkdb as r
from myslice.db import dispatch, changes
from myslice.lib.util import myJSONEncoder
from myslice.db.activity import Event, EventAction, ObjectType
from myslice.db.user import User
from myslice.web.rest import Api

from tornado import gen, escape

class PasswordHandler(Api):

    @gen.coroutine
    def put(self, hashing=None):
        """
        PUT /password[/<hashing>]
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
                #print(user.password)
                # Crypt password
                new_password = crypt.crypt(data['password'], crypt.mksalt())
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



