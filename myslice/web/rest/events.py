import json

import rethinkdb as r
from tornado import gen, escape

from myslice.web.rest import Api
from myslice.lib.util import DecimalEncoder, DateEncoder
from myslice.db.model import Event, EventStatus, EventAction

class EventsHandler(Api):

    @gen.coroutine
    def get(self):
        events = []

        cursor = yield r.table('events').run(self.dbconnection)

        while (yield cursor.fetch_next()):
            item = yield cursor.next()
            events.append(item)

        # return status code
        if not events:
            self.set_status(404)
            self.finish({"reason": "Not found, Please check the URI."})
        else:
            self.write(json.dumps({"events": events}, cls=DecimalEncoder, default=DateEncoder))

    @gen.coroutine
    def post(self):
        """
        Creates new event
        """

        # TODO: get user id from user logged in

        # NOTE: checks are done by the service, here we only dispatch the event

        ev = None
        try:
            ev = Event(escape.json_decode(self.request.body)['event'])
        except Exception as e:
            self.write(json.dumps({"return":"error"}))
            print(e)

        result = yield r.table('events').insert(ev.dict()).run(self.dbconnection)
        #data = self.get_argument('event','no data')

        print(ev)

        self.write(json.dumps({"return":"ok"}))