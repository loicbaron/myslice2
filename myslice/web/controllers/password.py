import uuid
from tornado import web
from tornado import gen, escape
import rethinkdb as r
from myslice.db import dispatch, changes
from myslice.db.activity import Event
from myslice.web.controllers import BaseController

class Index(BaseController):

    #@web.authenticated
    @gen.coroutine
    def get(self, hashing):
        msg = ''
        new_hashing = ''
        # If user not authenticated
        # compare the hash of the url with the hash in the users table
        #if not self.get_current_user():
        if not self.get_current_user():
            try:
                # Find the Event based on the hashing
                cursor = yield r.table('activity').filter(lambda ev:
                                                           ev["data"]["hashing"] == hashing
                                                           ).run(self.application.dbconnection)
                while (yield cursor.fetch_next()):
                    ev = yield cursor.next()
                event = Event(ev)

                #msg = "hashing=%s" % hashing
                #msg='compare hash user=%s' % user
                # Update the hashing of the user
                # For security reason, link sent by email can be used only once
                # Updating the hashing with a new one to perfom the Update Query onSubmit
                #feed = yield r.table('users').filter({"hashing": hashing}).update({'hashing':'yyy'}).run(self.application.dbconnection)
                new_hashing = str(uuid.uuid4())
                event.data["hashing"] = new_hashing
                result = yield dispatch(self.application.dbconnection, event)
            except Exception as e:
                #import traceback
                #traceback.print_exc()
                msg = "This link is not valid, please generate a new one."

        self.render(self.application.templates + "/password.html", message=msg, new_hashing=new_hashing)
