from tornado import web
from myslice.web.controllers import BaseController

class Index(BaseController):

    #@web.authenticated
    def get(self):
        self.render(self.application.templates + "/activity.html")