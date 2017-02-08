import logging
import uuid
import requests
from tornado import web
from tornado import gen, escape
import rethinkdb as r
from myslice import settings as s
from myslice.db import dispatch, changes
from myslice.db.activity import Event
from myslice.web.controllers import BaseController

logger = logging.getLogger("myslice.web.controller.password")

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
                logger.error(e)
                msg = "This link is not valid, please generate a new one."
                self.render(self.application.templates + "/password_forgot.html", message=msg)
                return

        self.render(self.application.templates + "/password.html", message=msg, new_hashing=new_hashing)

class Forgot(BaseController):

    #@web.authenticated
    @gen.coroutine
    def get(self):
        msg = ''
        self.render(self.application.templates + "/password_forgot.html", message=msg)

    @gen.coroutine
    def post(self):
        """
           Create an Event PASSWORD 
        """
        try:
            post_email = self.get_argument("email")
            payload = {"email":post_email}
            url = s.web.url
            if s.web.port and s.web.port != 80:
                url = url +':'+ s.web.port
            headers = {'Content-type': 'application/json'}
            url = url+"/api/v1/password"
            r = requests.put(url, data=payload, headers=headers)
        except Exception as e:
            logger.error(e)
            #import traceback
            #traceback.print_exc()
            self.render(self.application.templates + "/password_forgot.html", message="Something went wrong...")
            return

        self.redirect("/")
