from tornado import web
from myslice.web.controllers import BaseController

class Projects(BaseController):
    def get(self):
        self.set_current_user("test")
        self.render(self.application.templates + "/projects.html")