##
#   MySlice version 2
#
#   Model: defines class models used for the database
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

class EventStatus(object):
    SUCCESS = 'success'
    ERROR = 'error'
    WARNING = 'warning'
    PENDING = 'pending'

class EventActions(object):
    NEW = 'new'
    DEL = 'del'

class Event(object):
    """
        {
            action: ''
            src: <id>
            dst: <id>
        }

    """

    def __init__(self, action=None, ):
        self.action
        self.status = ''

