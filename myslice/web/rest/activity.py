import json

import rethinkdb as r
from tornado import gen, escape

from myslice.web.rest import Api
from myslice.lib.util import myJSONEncoder
from myslice.db import dispatch, changes
from myslice.db.activity import Event, EventStatus

class ActivityHandler(Api):

    @gen.coroutine
    def get(self):
        activity = []

        cursor = yield r.table('activity').run(self.dbconnection)

        while (yield cursor.fetch_next()):
            item = yield cursor.next()
            activity.append(item)

        # return status code
        if not activity:
            self.set_status(404)
            self.finish({"reason": "Not found, Please check the URI."})
        else:
            self.finish(json.dumps({"activity": activity}, cls=myJSONEncoder))

    @gen.coroutine
    def post(self):
        """
        Creates new event
        """

        # TODO: get user id from user logged in

        # NOTE: checks are done by the service, here we only dispatch the event

        print(escape.json_decode(self.request.body))
        try:
            data = escape.json_decode(self.request.body)['event']
        except json.decoder.JSONDecodeError as e:
            self.set_status(400)
            self.finish(json.dumps({"return": {"status": "error", "messages": "malformed request"}}))
            return

        try:
            event = Event(data)
        except Exception as e:
            self.set_status(500)
            self.finish(json.dumps({"return": {"status":"error","messages":e.message}}))
            #import traceback
            #traceback.print_exc()
        else:
            result = yield dispatch(self.dbconnection, event)
            #data = self.get_argument('event','no data')
            event_id = result['generated_keys'][0]
            feed = yield changes(dbconnection = self.dbconnection, table='activity')
            while (yield feed.fetch_next()):
                item = yield feed.next()
                ev = Event(item['new_val'])
                if ev.id == event_id:
                    print(ev.status)
                    if ev.status == EventStatus.ERROR or ev.status == EventStatus.WARNING:
                        self.set_status(500)
                    if ev.status == EventStatus.SUCCESS or ev.status == EventStatus.PENDING or ev.status == EventStatus.DENIED:
                        self.set_status(200)
                    self.finish(json.dumps({"return": {"status":ev.status,"messages":ev}}, cls=myJSONEncoder))



