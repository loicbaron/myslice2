from tornado import gen
from myslice.web.controllers import BaseController


class Index(BaseController):

    def get(self):

        self.render(self.application.templates + "/AddOrganization.html")

