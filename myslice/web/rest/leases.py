import json

import rethinkdb as r
from tornado import gen, escape

from myslice.web.rest import Api
from myslice.lib.util import myJSONEncoder
import re
from myslice.db.activity import Event, EventAction, ObjectType
from myslice.db import dispatch
class LeasesHandler(Api):
    @gen.coroutine
    def get(self, o=None, t=None):
        """
        Leases list

         GET /leases
         GET /leases/id
         GET /leases/start_time¶end_time
         GET /leases/start_time/end_time


        :return:
        """
        leases = []


        #GET / leases
        if not o and not t:
            cursor = yield r.table('leases').run(self.dbconnection)

            while (yield cursor.fetch_next()):
                result = yield cursor.next()
                leases.append(result)

        #  GET / leases / start_time¶end_time
        elif o and not t:
            regexp="[0-9-]{10}"
            if re.match(regexp, o) is not None:
                cursor = yield r.table('leases').filter(
                    r.row['start_time'].eq(int(o)) | (r.row['end_time'].eq(int(o)))).run(self.dbconnection)
                while (yield cursor.fetch_next()):
                    item = yield cursor.next()
                    leases.append(item)

            else:
                # GET / leases/id
                cursor = yield r.table('leases') \
                    .filter({'id': o}).run(self.dbconnection)
                while (yield cursor.fetch_next()):
                    result = yield cursor.next()
                    leases.append(result)
        #GET / leases / start_time / end_time
        else:
            cursor = yield r.table('leases').filter(r.row['start_time'].eq(int(o)) & (r.row['end_time'].eq(int(t)))).run(self.dbconnection)
            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                leases.append(item)
        self.write(json.dumps({"result": leases}, cls=myJSONEncoder))



    @gen.coroutine
    def post(self, id=None, o=None):
        """
        POST /leases
        { testbed: string, slice_id: string, start_time: int, end_time: int }
        :return:
        """

        if not self.request.body:
            self.userError("empty request")
            return

        try:
            data = escape.json_decode(self.request.body)
        except json.decoder.JSONDecodeError as e:
            self.userError("malformed request", e.msg)
            return

        try:
            u = yield r.table('users').get(self.current_user['id']).run(self.dbconnection)
            if data['slice_id'] not in u['slices']:
                self.userError("your user is not a member of this slice: %s" % data['slice_id'])

        except Exception:
            self.userError("not authenticated")
            return

        try:
            event = Event({
                'action': EventAction.CREATE,
                'user': self.current_user['id'],
                'object': {
                    'type': ObjectType.LEASE,
                    'id': None,
                },
                'data': data
            })
        except AttributeError as e:
            self.userError("Can't create request", e)
            return
        except Exception as e:
            self.userError("Can't create request", e)
            return
        else:
            result = yield dispatch(self.dbconnection, event)

            self.write(json.dumps(
                {
                    "result": "success",
                    "error": None,
                    "debug": None,
                    "events": result['generated_keys']
                }, cls=myJSONEncoder))


    @gen.coroutine
    def delete(self, id, o=None):
        """
        DELETE /leases/<id>
        :return:
        """
        # Check if the user is a member of the slice
        try:
            u = yield r.table('users').get(self.current_user['id']).run(self.dbconnection)
            p = yield r.table('leases').get(id).run(self.dbconnection)
            if p['slice_id'] not in u['slices']:
                self.userError("your user is not a member of this slice: %s" % p['slice_id'])
        except Exception:
            self.userError("not authenticated or project not specified")
            return

        try:
            event = Event({
                'action': EventAction.DELETE,
                'user': self.current_user['id'],
                'object': {
                    'type': ObjectType.LEASE,
                    'id': id,
                }
            })
        except AttributeError as e:
            self.userError("Can't create request", e)
            return
        except Exception as e:
            self.userError("Can't create request", e)
            return
        else:
            result = yield dispatch(self.dbconnection, event)

            self.write(json.dumps(
                {
                    "result": "success",
                    "error": None,
                    "debug": None,
                    "events": result['generated_keys']
                }, cls=myJSONEncoder))

