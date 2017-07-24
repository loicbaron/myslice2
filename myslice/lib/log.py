import os
import logging
from myslice import config

class Log(object):

    def __init__(self):

        self._path = os.path.abspath("/var/log/myslice")

        ##
        # log path
        if not os.path.exists(self._path):
            exit("Log path {} does not exists".format(self._path))

        self.log_formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")

        ##
        # setup a default logger
        self.default_logger = logging.getLogger("myslice")

        self.default_handler = logging.FileHandler("{}/default.log".format(self._path))
        self.default_handler.setFormatter(self.log_formatter)
        self.default_logger.setLevel(logging.DEBUG)
        self.default_logger.addHandler(self.default_handler)

    @property
    def filename(self):
        pass

    @property
    def level(self):
        pass

    def getLogger(self, name=None):

        if not name or not name in config.services or not config.services[name]:
            ##
            # use the default logger
            return self.default_logger
        else:
            logger = logging.getLogger(name)
            try:
                handler = logging.FileHandler(
                    os.path.abspath("{}/{}".format(self._path, config.services[name]["log_file"], "{}.log".format(name)))
                )
            except AttributeError:
                handler = self.default_handler
                pass
            handler.setFormatter(self.log_formatter)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(handler)
            return logger

_log = Log()

def getLogger(name=None):
    return _log.getLogger(name)