from tornado import web
from tornado import gen, escape
import rethinkdb as r
import myslice.db as db
from myslice.web.controllers import BaseController

class Index(BaseController):

    #@web.authenticated
    @gen.coroutine
    def get(self, hashing):
        msg = ''
        # If user not authenticated
        # compare the hash of the url with the hash in the users table
        #if not self.get_current_user():
        if not self.get_current_user():
            try:
                feed = yield r.table('users').filter({"hashing": hashing}).run(self.application.dbconnection)
                yield feed.fetch_next()
                user = yield feed.next()
                #msg = "hashing=%s" % hashing
                #msg='compare hash user=%s' % user
                # Update the hashing of the user
                # For security reason, link sent by email can be used only once
                # Updating the hashing with a new one to perfom the Update Query onSubmit
                #feed = yield r.table('users').filter({"hashing": hashing}).update({'hashing':'yyy'}).run(self.application.dbconnection)
            except Exception as e:
                    msg = "This link is not valid, please generate a new one."

        self.render(self.application.templates + "/password.html", message=msg, new_hashing='yyy')
