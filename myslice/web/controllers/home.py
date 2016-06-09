from tornado import web
from myslice.web.controllers import BaseController

class Index(BaseController):
    def get(self):
        self.set_current_user("test")
        self.render(self.application.templates + "/index.html")

class Project(BaseController):
    def get(self):
        self.set_current_user("test")
        self.render(self.application.templates + "/project.html")

class User(BaseController):
    def get(self):
        self.set_current_user("test")
        self.render(self.application.templates + "/profile.html")
