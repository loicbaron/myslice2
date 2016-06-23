from tornado import web
from myslice.web.controllers import BaseController

class Index(BaseController):

    @web.authenticated
    def get(self):
        self.render(self.application.templates + "/index.html")

class User(BaseController):

    @web.authenticated
    def get(self):
        self.render(self.application.templates + "/settings.html")
