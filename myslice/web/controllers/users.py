from tornado import web
from myslice.web.controllers import BaseController

class Users(BaseController):
    def get(self, id=None):
        self.render(self.application.templates + "/users.html")
