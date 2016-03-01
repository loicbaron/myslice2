from configparser import SafeConfigParser, NoSectionError, NoOptionError, Error
import os
import logging
import sys

## paths
config_path = os.path.abspath("/etc/myslice")
if not os.path.exists(config_path):
    pass

## logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filename="myslice-web.log", filemode="a")



## config file
config_file = config_path

class settings(object):

    ## setup db
    class db(object):
        host = "localhost"
        port = 28015
        name = "myslice"

## override with configuration file
#parser = SafeConfigParser()
#s = parser.read(self.files)
#parser.get(section, key)
