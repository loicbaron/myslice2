from tornado import web, gen
from myslice.web.controllers import BaseController

class Slices(BaseController):

    @web.authenticated
    def get(self, hrn=None):

        if not hrn:
            self.redirect('/projects')

        self.render(self.application.templates + "/slices.html")

