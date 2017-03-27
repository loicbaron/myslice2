import os
import logging
from datetime import datetime
import pytz
import json
import decimal
from enum import Enum
from json import JSONEncoder
from configparser import ConfigParser, NoOptionError

log = logging.getLogger('server')

# def drop_privileges(uid_name='nobody', gid_name='nogroup'):
#
#     import os, pwd, grp
#
#     starting_uid = os.getuid()
#     starting_gid = os.getgid()
#
#     starting_uid_name = pwd.getpwuid(starting_uid)[0]
#
#     log.info('drop_privileges: started as %s/%s' % \
#              (pwd.getpwuid(starting_uid)[0],
#               grp.getgrgid(starting_gid)[0]))
#
#     if os.getuid() != 0:
#         # We're not root so, like, whatever dude
#         log.info('drop_privileges: already running as %s' % starting_uid_name)
#         return
#
#     # If we started as root, drop privs and become the specified user/group
#     if starting_uid == 0:
#
#         # Get the uid/gid from the name
#         running_uid = pwd.getpwnam(uid_name)[2]
#         running_gid = grp.getgrnam(gid_name)[2]
#
#         # Try setting the new uid/gid
#         try:
#             os.setgid(running_gid)
#         except OSError as e:
#             log.error('Could not set effective group id: %s' % e)
#
#         try:
#             os.setuid(running_uid)
#         except OSError as e:
#             log.error('Could not set effective user id: %s' % e)
#
#         # Ensure a very convervative umask
#         new_umask = 077
#         old_umask = os.umask(new_umask)
#         log.info('drop_privileges: Old umask: %s, new umask: %s' % \
#                  (oct(old_umask), oct(new_umask)))
#
#     final_uid = os.getuid()
#     final_gid = os.getgid()
#     log.info('drop_privileges: running as %s/%s' % \
#              (pwd.getpwuid(final_uid)[0],
#               grp.getgrgid(final_gid)[0]))

def format_date(date=None):
    if not date:
        date = datetime.now()
    if date.tzinfo is None or date.tzinfo.utcoffset(date) is None:
        tz = pytz.timezone('UTC')
        return tz.localize(date)
    else:
        return date


# handles serialization of datetime in json
DateEncoder = lambda obj: obj.isoformat() if isinstance(obj, datetime) else None

# support converting decimal in json
json.encoder.FLOAT_REPR = lambda o: format(o, '.2f')

# handles decimal numbers serialization in json
class DecimalEncoder(JSONEncoder):

    def _iterencode(self, o, markers=None):

        if isinstance(o, decimal.Decimal):
            return (str(o) for o in [o])

        return super(DecimalEncoder, self)._iterencode(o, markers)

# handles enum members json encoding
class myJSONEncoder(JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, Enum):
            return str(o.value)

        if isinstance(o, decimal.Decimal):
            return (str(o) for o in [o])

        return JSONEncoder.default(self, o)

class Config(object):

    def __init__(self):

        self._path = os.path.abspath("/etc/myslice")

        self._config = {
            "main" : None,
            "web" : None,
            "server" : None,
            "endpoints" : None
        }

        ##
        # configuration path(s)
        if not os.path.exists(self._path):
            exit("Configuration path {} does not exists".format(self._path))

        for c in self._config.keys():
            self._config[c] = ConfigParser()
            try:
                self._config[c].read_file(open("{}/{}.cfg".format(self._path, c)))
            except FileNotFoundError:
                exit("Configuration file {}.cfg not found".format(c))

    @property
    def services(self):
        services = {}
        for service in self._config["server"].sections():
            services[service] = {
                "enabled": self._config["server"].getboolean(service, "enabled", fallback=False),
                "log_file": self._config["server"].get(service, "log_file", fallback=None),
                "log_level": self._config["server"].get(service, "log_level", fallback=None)
            }


        return services

    @property
    def endpoints(self):
        endpoints = {}
        for endpoint in self._config["endpoints"].sections():
            try:
                endpoints[endpoint] = {
                    "enabled": self._config["endpoints"].getboolean(endpoint, "enabled", fallback=False),
                    "name": self._config["endpoints"].get(endpoint, "name", fallback=None),
                    "url": self._config["endpoints"].get(endpoint, "url"),
                    "type": self._config["endpoints"].get(endpoint, "type"),
                    "timeout": self._config["endpoints"].get(endpoint, "timeout", fallback=30),
                    "technologies": self._config["endpoints"].get(endpoint, "technologies", fallback=None)
                }
            except NoOptionError:
                pass

        return endpoints

    @property
    def web(self):
        if self._config["main"].has_section("web"):
            return {
                "url": self._config["main"].get("web", "url", fallback="http://localhost"),
                "port": self._config["main"].get("web", "port", fallback="80"),
                "cookie_secret": self._config["main"].get("web", "cookie_secret", fallback=""),
                "token_secret": self._config["main"].get("web", "token_secret", fallback=""),
            }
        else:
            exit("no web configuration section found")

