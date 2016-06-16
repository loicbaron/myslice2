from tornado import web
from myslice.web.controllers import BaseController

class Projects(BaseController):
    def get(self):
        self.render(self.application.templates + "/projects.html")