import json
import logging
import time

import rethinkdb as r
from tornado import gen, escape

from myslice.web.rest import Api
from myslice.lib.util import myJSONEncoder
import re
from myslice.db.activity import Event, EventAction, ObjectType
from myslice.db import dispatch

logger = logging.getLogger('myslice.rest.leases')

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
        if not self.get_current_user():
            self.userError('permission denied user not logged in')
            return

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
        or list of leases
        [{ testbed: string, slice_id: string, start_time: int, end_time: int, duration: int }]
        :return:
        """

        if not self.get_current_user():
            self.userError('permission denied user not logged in')
            return

        if not self.request.body:
            self.userError("empty request")
            return

        try:
            data = escape.json_decode(self.request.body)
        except json.decoder.JSONDecodeError as e:
            self.userError("malformed request", e.msg)
            return

        evData = []
        try:
            if isinstance(data, list):
                for l in data:
                    d = yield self.processLease(l)
                    evData.append(d)
            else:
                d = yield self.processLease(data)
                evData.append(d)

            event = Event({
                'action': EventAction.CREATE,
                'user': self.get_current_user()['id'],
                'object': {
                    'type': ObjectType.LEASE,
                    'id': None,
                },
                'data': evData
            })

            res = yield dispatch(self.dbconnection, event)
            result = res['generated_keys']
        except Exception as e:
            self.userError(e)

        self.write(json.dumps(
            {
                "result": "success",
                "events": result,
                "error": None,
                "debug": None,
            }, cls=myJSONEncoder))  

    @gen.coroutine
    def processLease(self, data):
        logger.info("processing lease:")
        logger.info(data)
        # start_time can not be in the past
        # but can be 0 for ASAP mode
        if 'start_time' in data and data['start_time'] != 0 and data['start_time'] < int(time.time()):
            #logger.info("start_time can not be in the past, changing start_time to Now")
            data['start_time'] = int(time.time())

        # XXX Just to debug
        if not 'start_time' in data:
            # Start 1 minute later than now
            data['start_time']=int(time.time())+1*60

        # Scheduled reservation
        if 'start_time' in data:
            if 'end_time' not in data and 'duration' in data:
                data['end_time'] = data['start_time'] + data['duration']
            elif 'duration' not in data and 'end_time' in data:
                data['duration'] = data['end_time'] - data['start_time']
            if 'duration' not in data and 'end_time' not in data:
                raise Exception('you must specify either duration or end_time')
        # ASAP reservation
        else:
            if 'duration' not in data:
                raise Exception("duration must be specified for ASAP reservation")

        try:
            u = yield r.table('users').get(self.get_current_user()['id']).run(self.dbconnection)
            if data['slice_id'] not in u['slices']:
                raise Exception("your user is not a member of this slice: %s" % data['slice_id'])
        except Exception:
            raise Exception("not authenticated")

        return data

    @gen.coroutine
    def delete(self, id, o=None):
        """
        DELETE /leases/<id>
        :return:
        """
        if not self.get_current_user():
            self.userError('permission denied user not logged in')
            return
        # Check if the user is a member of the slice
        try:
            u = yield r.table('users').get(self.get_current_user()['id']).run(self.dbconnection)
            p = yield r.table('leases').get(id).run(self.dbconnection)
            if p['slice_id'] not in u['slices']:
                self.userError("your user is not a member of this slice: %s" % p['slice_id'])
        except Exception:
            self.userError("not authenticated or project not specified")
            return

        try:
            event = Event({
                'action': EventAction.DELETE,
                'user': self.get_current_user()['id'],
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

