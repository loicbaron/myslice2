import sys, os, logging
from configparser import SafeConfigParser, NoSectionError, NoOptionError, Error
from myslicelib.util import Credential, Endpoint
from myslicelib import setup as myslicelibsetup

## paths
config_path = os.path.abspath("/etc/myslice")
if not os.path.exists(config_path):
    pass

## logging
logging_path = os.path.abspath("/var/log/myslice")
if not os.path.exists(logging_path):
    try:
        os.mkdir(logging_path)
    except PermissionError as e:
        logging.error("Can't create directory {}".format(logging_path))
        exit("Can't create directory {}".format(logging_path))
logging_file = logging_path + "/myslice-web.log"
try:
    logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filename=logging_file, filemode="a")

except PermissionError as e:
        logging.error("Can't write log file {}".format(logging_file))
        exit("Can't write log file {}".format(logging_file))


## version check
try:
    assert sys.version_info >= (3,5)
except AssertionError:
    logging.error("MySlice requires Python 3.5")
    exit("MySlice requires Python 3.5")


## config file
config_file = config_path

## Setup MySliceLib
myslicelibsetup.endpoints = [
            Endpoint(url="https://sfa3.planet-lab.eu:12346",type="AM"),
            # Endpoint(url="https://194.199.16.164:12346",type="AM"),
            # Endpoint(url="https://www.wilab2.ilabt.iminds.be:12369/protogeni/xmlrpc/am/3.0",type="AM"),
            # Endpoint(url="https://fuseco.fokus.fraunhofer.de/api/sfa/am/v3",type="AM"),
            # Endpoint(url="https://griffin.ipv6.lip6.fr:8001/RPC2",type="AM"),
            Endpoint(url="https://portal.onelab.eu:6080",type="Reg"),
            #Endpoint(url="https://sfa-fed4fire.pl.sophia.inria.fr:443",type="Reg")
        ]

credential_path = "/Users/moray/Sites/upmc/"
credential_pkey = credential_path + "cscognamiglio_onelab.pkey"
credential_hrn = "onelab.upmc.cscognamiglio"
credential_email = "cscognamiglio@gmail.com"
credential_cert = credential_path + "cscognamiglio_onelab.cert"

myslicelibsetup.credential = Credential(hrn=credential_hrn, email=credential_email, certificate=credential_cert, private_key=credential_pkey)
##

class settings(object):

    ## setup db
    # @property
    # def db(self):
    #     return dbsettings()

    class db(object):
        host = "localhost"
        port = 28015
        name = "myslice"


## override with configuration file
#parser = SafeConfigParser()
#s = parser.read(self.files)
#parser.get(section, key)
