from tornado import web
from tornado import gen, escape
import rethinkdb as r
from myslice.web.controllers import BaseController
from myslice.db.activity import Event
from myslice.db import dispatch

class Index(BaseController):

    @gen.coroutine
    def get(self, id):
        msg = ""
        try:
            ev = yield r.table('activity').get(id).run(self.application.dbconnection)
            if ev is None:
                raise ValueError("event id is not valid")
            event = Event(ev)
            event.setPending()
            msg = "Your email is confirmed. "
            msg += "A request has been sent to a manager. "
            msg += "You will be informed as soon as your account will be validated."
            # dispatch the updated event
            dispatch(self.application.dbconnection, event)
        except Exception as e:
            import traceback
            traceback.print_exc()
            msg = "This link is not valid"
        self.render(self.application.templates + "/confirm.html", message=msg)
