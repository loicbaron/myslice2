import logging
from tornado import web, escape
from rethinkdb import r

from myslice.db.user import User

logger = logging.getLogger(__name__)

class BaseController(web.RequestHandler):

    def set_current_user(self, id):
        if id:
            self.set_secure_cookie("user", id)
        else:
            self.clear_cookie("user")

    def get_current_user(self):
        return self.get_secure_cookie("user")
        #logger.debug("COOKIE USER ID: {}".format(cookie))

    def get_current_user_obj(self):
        ret = yield r.table('user').get(self.get_current_user_id()).run(self.dbconnection)
        if not ret:
            self.redirect("/login")

        user = User(ret)

        yield user