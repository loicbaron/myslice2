import json

import rethinkdb as r

from myslice.db import dispatch
from myslice.db.activity import Event
from myslice.lib.util import myJSONEncoder
from myslice.web.rest import Api

from tornado import gen, escape

class RequestsHandler(Api):

    @gen.coroutine
    def get(self, id):
        """
        GET /requests/[<id>]

        Request list or request with <id>

        :return:
        """

        users = []

        # TODO: id must be a valid URN
        if id:
            result = yield r.table('users').get(id).run(self.dbconnection)
            users.append(result)
        else:
            cursor = yield r.table('users').run(self.dbconnection)

            while (yield cursor.fetch_next()):
                result = yield cursor.next()
                users.append(result)

        self.write(json.dumps({"result": users}, cls=myJSONEncoder))

    @gen.coroutine
    def put(self, id):
        """
        PUT /requests/<id>
        { action: <approve|deny> }
        :return:
        """

        if id is None:
            self.userError("wrong ID missing")

        try:
            action = escape.json_decode(self.request.body)['action']
        except json.decoder.JSONDecodeError as e:
            self.userError("malformed request", e.message)
            return

        if action != 'approve' or action != 'deny':
            self.userError("action must be approve or deny")
            return

        # retrieve the event from db, and see if it is in pending status
        ev = yield r.table('activity').get(id).run(self.dbconnection)
        if not ev:
            self.userError("request not found {}".format(id))
            return

        event = Event(ev)
        if not event.isPending():
            self.serverError("malformed request")
            return

        user = self.get_current_user()

        if not user.has_privilege(event):
            self.userError("Permission denied")
            return

        event.user = self.get_current_user_id()

        if action == 'approve':
            event.setApproved()

        if action == 'deny':
            event.setDenied()

        yield dispatch(self.dbconnection, event)
