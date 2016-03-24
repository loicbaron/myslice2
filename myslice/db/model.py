##
#   MySlice version 2
#
#   Model: defines class models used for the database
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

from enum import Enum
import json
import pprint

class EventStatus(Enum):
    SUCCESS = 'success'
    ERROR = 'error'
    WARNING = 'warning'
    PENDING = 'pending'

class EventAction(Enum):
    NEW = 'new'
    DEL = 'del'

class Event(object):
    """
        {
            action: EventAction
            status: EventStatus
            message: String
            object: {}
            changes: {}
            user: <id>
        }

    """

    def __init__(self, event):
        self.e = {}

        self.action = event['action']

        self.status = event['status']

        if 'message' in event:
            self.message = event['message']
        else:
            self.message = ''

        if not 'user' in event:
            raise ValueError('User id must be specified')

        self.user = event['user']

        if not 'object' in event:
            raise ValueError('Object must be specified')

        if 'changes' in event:
            self.changes = event['changes']

    def __str__(self):
        return json.dumps(self.e)

    def dict(self):
        return self.e
    
    @property
    def action(self):
        return self.e['action']

    @action.setter
    def action(self, value):
        if not isinstance(value, EventAction):
            raise ValueError('Action not valid')

        self.e['action'] = value.value

    @property
    def status(self):
        return self.e['status']

    @status.setter
    def status(self, value):
        if not isinstance(value, EventStatus):
            raise ValueError('Status not valid')

        self.e['status'] = value.value

    @property
    def message(self):
        return self.e['message']

    @message.setter
    def message(self, value=''):
        self.e['message'] = value

    @property
    def user(self):
        return self.e['user']

    @user.setter
    def user(self, value):
        self.e['user'] = value

    @property
    def object(self):
        return self.e['object']

    @object.setter
    def object(self, value):
        if not all(k in value for k in ("type")):
            raise ValueError('Object must have at least type')

        self.e['object'] = value

    @property
    def changes(self):
        return self.e['changes']

    @changes.setter
    def changes(self, value):
        if not all(k in value for k in ("type")):
            raise ValueError('Changes must have at least type')

        self.e['changes'] = value