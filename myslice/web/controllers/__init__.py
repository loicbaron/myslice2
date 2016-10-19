import logging
import json
from tornado import web, escape


logger = logging.getLogger(__name__)

class BaseController(web.RequestHandler):

    def get_current_user(self):

        cookie = self.get_secure_cookie("user")
        if not cookie:
            return False

        user = json.loads(str(cookie, "utf-8"))

        if not isinstance(user, dict):
            self.clear_cookie('user')
            self.redirect('/login')

        return user
