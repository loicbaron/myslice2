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
                timeout = int(endpoint["timeout"]),
                name = endpoint["name"],
                technologies = endpoint["technologies"],
                hasLeases = endpoint["hasLeases"],
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
pkey = config.auth['pkey']
cert = config.auth['cert']
hrn = config.auth['hrn']
email = config.auth['email']

myslicelibsetup.authentication = Authentication(hrn=hrn, email=email, certificate=cert, private_key=pkey)

## override with configuration file
#parser = SafeConfigParser()
#s = parser.read(self.files)
#parser.get(section, key)

settings = config
