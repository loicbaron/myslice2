import json
import logging
import rethinkdb as r
from tornado import gen, escape

from myslice.db.activity import Event
from myslice.lib.util import myJSONEncoder
from myslice.web.rest import Api

logger = logging.getLogger('myslice.rest.confirm')

class ConfirmHandler(Api):

    @gen.coroutine
    def get(self, id):
        """
        GET /confirm/id
        it allows to confirm an email address using the event id
        :return:
        """
        try:
            ev = yield r.table('activity').get(id).run(self.application.dbconnection)
            if len(ev) != 1:
                raise ValueError("event id is not valid")
            event = Event(ev)
            event.setPending()
            event.logInfo("Event is pending, a manager will validate your request")
            self.finish(json.dumps({"result": ["your email is confirmed"]}, cls=myJSONEncoder))
        except Exception as e:
            self.userError("This link is not valid")
            return
