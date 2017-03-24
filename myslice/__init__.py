import sys

from myslice.lib.util import Config
from myslicelib.util import Authentication, Endpoint
from myslicelib import setup as myslicelibsetup

##
# MySlice requires Python 3.5
try:
    assert sys.version_info >= (3,5)
except AssertionError:
    exit("MySlice requires Python 3.5")

##
# init config
config = Config()

## Setup endpoints with MySliceLib
myslicelibsetup.endpoints = []
for k,endpoint in config.endpoints.items():
    if (endpoint["enabled"]):
        myslicelibsetup.endpoints.append(
            Endpoint(
                url = endpoint["url"],
                type = endpoint["type"],
                timeout = endpoint["timeout"],
                name = endpoint["name"],
                technologies = endpoint["technologies"]
            )
        )

myslicelibsetup.registry_endpoints = [
            Endpoint(url="https://portal.onelab.eu:6080",type="Reg", timeout=30, name="OneLab Registry"),
        ]

#if os.path.exists(os.path.expanduser("~/.sfi/")):
#    path = os.path.expanduser("~/.sfi/")
#    pkey = path + "onelab.upmc.loic_baron.pkey"
#    hrn = "onelab.upmc.loic_baron"
#    email = "loic.baron@lip6.fr"
#    cert = path + "onelab.upmc.loic_baron.user.gid"
#else:
#    path = os.path.expanduser("~/")
path = "/var/myslice/"
pkey = path + "myslice.pkey"
hrn = "onelab.myslice"
email = "support@myslice.info"
cert = path + "myslice.cert"


myslicelibsetup.authentication = Authentication(hrn=hrn, email=email, certificate=cert, private_key=pkey)

class settings(object):

    ## setup db
    # @property
    # def db(self):
    #     return dbsettings()

    class db(object):
        host = "localhost"
        port = 28015
        name = "myslice"

    class email(object):
        dirpath = '/myslice/myslice/web/templates/email'
        theme = 'onelab'
        domain = 'onelab.eu'
        host = 'smtp.gmail.com'
        port = 587
        ssl = True
        user = 'zhouquantest16@gmail.com'
        password = 'zqtest123'

    class web(object):
        url = 'http://dev.myslice.info'
        port = '8111'
        cookie_secret="x&7G1d2!5MhG9SWkXu"
        token_secret = 'u636vbJV6Ph[EJB;Q'

## override with configuration file
#parser = SafeConfigParser()
#s = parser.read(self.files)
#parser.get(section, key)
