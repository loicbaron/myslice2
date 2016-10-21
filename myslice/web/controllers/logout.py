from tornado import gen
from myslice.web.controllers import BaseController

class Index(BaseController):

    @gen.coroutine
    def get(self):
        """
        Delete the cookie and redirect to home

        :return:
        """
        self.clear_cookie("user")
        self.redirect("/")
