from myslice import settings as s
import json, time, decimal, logging
from datetime import date, datetime
import tornado_cors as cors
from tornado import web
import rethinkdb as r

logger = logging.getLogger(__name__)


class Api(cors.CorsMixin, web.RequestHandler):

    def initialize(self):
        self.dbconnection = self.application.dbconnection

    def set_default_headers(self):
        # Allow CORS
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json")