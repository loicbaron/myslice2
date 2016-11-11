import json
import time

import rethinkdb as r
from tornado import gen, escape

from myslice.web.rest import Api
from myslice.lib.util import myJSONEncoder
import re
from myslice.db.activity import Event, EventAction, ObjectType
from myslice.db import dispatch
class LeasesHandler(Api):

    @gen.coroutine
    def get(self, o=None):
        """
        Leases list

         GET /leases
         GET /leases/id
         GET /leases?timestamp_start=<xxx>&timestamp_end=<xxx>

        :return:
        """
        leases = []

        # [?timestamp_start=<XXX>&timestamp_end=<XXX>]
        ts = self.get_argument('timestamp_start',None)
        te = self.get_argument('timestamp_end',None)

        #GET / leases
        if not o and not ts and not te:
            cursor = yield r.table('leases').run(self.dbconnection)

            while (yield cursor.fetch_next()):
                result = yield cursor.next()
                leases.append(result)

        # GET / leases/id
        elif o and not ts and not te:
            cursor = yield r.table('leases') \
                .filter({'id': o}).run(self.dbconnection)
            while (yield cursor.fetch_next()):
                result = yield cursor.next()
                leases.append(result)

        # GET /leases?timestamp_start=<xxx>&timestamp_end=<xxx>
        elif ts and te:
            cursor = yield r.table('leases') \
                .filter(lambda l:
                    r.and_(l['start_time'].ge(int(ts)),l['end_time'].le(int(te)))
                ).run(self.dbconnection)
            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                leases.append(item)

        # GET /leases?timestamp_start=<XXX>
        elif ts and not te:
            cursor = yield r.table('leases') \
                .filter(lambda l:
                    l['start_time'].ge(int(ts))
                ).run(self.dbconnection)

            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                leases.append(item)

        # GET /leases?timestamp_end=<XXX>
        elif not ts and te:
            cursor = yield r.table('leases') \
                .filter(lambda l:
                    l['end_time'].le(int(te))
                ).run(self.dbconnection)

            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                leases.append(item)
        else:
            self.userError("invalid request")
            return
        self.write(json.dumps({"result": leases}, cls=myJSONEncoder))



    @gen.coroutine
    def post(self, id=None, o=None):
        """
        POST /leases
        { testbed: string, slice_id: string, start_time: int, end_time: int, duration: int }
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

        # start_time can not be in the past
        # but can be 0 for ASAP mode
        if 'start_time' in data and data['start_time'] != 0 and data['start_time'] < int(time.time()):
            self.userError("start_time can not be in the past")
            return


        # XXX Just to debug
        if not 'start_time' in data:
            # Start 5 minutes later
            data['start_time']=int(time.time())+5*60

        # Scheduled reservation
        if 'start_time' in data:
            if 'end_time' not in data and 'duration' in data:
                data['end_time'] = data['start_time'] + data['duration']
            elif 'duration' not in data and 'end_time' in data:
                data['duration'] = data['end_time'] - data['start_time']
            else:
                self.userError('you must specify either duration or end_time')
                return
        # ASAP reservation
        else:
            if 'duration' not in data:
                self.userError("duration must be specified for ASAP reservation")
                return

        try:
            u = yield r.table('users').get(self.current_user['id']).run(self.dbconnection)
            if data['slice_id'] not in u['slices']:
                self.userError("your user is not a member of this slice: %s" % data['slice_id'])
                return
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
                    "events": result['generated_keys'],
                    "error": None,
                    "debug": None,
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
                    "events": result['generated_keys'],
                    "error": None,
                    "debug": None,
                }, cls=myJSONEncoder))

