from tornado import web

class Index(web.RequestHandler):
    def get(self):
        self.render(self.application.templates + "/index.html")

class Project(web.RequestHandler):
    def get(self):
        self.render(self.application.templates + "/project.html")
