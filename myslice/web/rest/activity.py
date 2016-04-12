import json

import rethinkdb as r
from tornado import gen, escape

from myslice.web.rest import Api
from myslice.lib.util import myJSONEncoder
from myslice.db import dispatch
from myslice.db.activity import Event

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
            self.finish(json.dumps({"return": {"status": "error", "messages": "malformed request"}}))
            return

        try:
            event = Event(data)
        except Exception as e:
            self.finish(json.dumps({"return": {"status":"error","messages":e.message}}))
            import traceback
            traceback.print_exc()
        else:
            result = yield dispatch(self.dbconnection, event)
            #data = self.get_argument('event','no data')
            print(event)

