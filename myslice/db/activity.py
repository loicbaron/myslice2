##
#   MySlice version 2
#
#   Model: defines class models used for the database
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

import json
import logging
from enum import Enum
from myslice.lib.util import format_date, DecimalEncoder, DateEncoder

logger = logging.getLogger("myslice.event")

class ObjectType(Enum):
    AUTHORITY = "AUTHORITY"
    PROJECT = "PROJECT"
    SLICE = "SLICE"
    USER = "USER"
    RESOURCE = "RESOURCE"
    KEY = "KEY"

# TODO: when initializing check if object exists in rethinkdb
class Object(object):

    def __init__(self, obj):
        self.e = {}

        self.type = obj['type']

        self.id = obj['id']

    def __str__(self):
        return json.dumps(self.e, cls=DecimalEncoder, default=DateEncoder)

    def dict(self):
        return self.e

    ##
    # Object Type
    @property
    def type(self):
        return self.e['type']

    @type.setter
    def type(self, value):
        if isinstance(value, ObjectType):
            self.e['type'] = value.value
        elif value in ObjectType.__members__:
            self.e['type'] = value
        else:
            raise ValueError('Object Type {} is not valid'.format(value))

    ##
    # ID of the object type
    @property
    def id(self):
        return self.e['id']

    @id.setter
    def id(self, value):
        self.e['id'] = value

class EventStatus(Enum):
    """
    Event Status: new events will automatically have a NEW status,
    once dispatched a new event will be treated and its status will change
    """
    # NEW created event, this will be processed
    NEW = "NEW"
    # WAITING to be processed by an external service
    WAITING = "WAITING"
    # SUCCESSfully terminated
    SUCCESS = "SUCCESS"
    # ERROR or WARNING occurred during processing
    ERROR = "ERROR"
    WARNING = "WARNING"

class EventAction(Enum):
    """

    """
    # add an object
    ADD = "ADD"
    # delete an object
    DEL = "DEL"
    # modify an object
    MOD = "MOD"
    # create a reqest
    REQ = "REQ"

"""
{
"event": {
	"action":"ADD",
	"user":"XXXXXX",
	"object":{
		"type": "KEY",
		"key": "YYYYY"
		}
	}
}
"""

class Event(object):
    """
        {
            action: EventAction
            status: EventStatus
            message: String
            object: {}
            changes: {}
            user: <id>
            created: <date>
            updated: <date>
        }

    """

    def __init__(self, event):
        self.e = {}

        ##
        # If ID is present this is a previously
        # created event, or we don't set it
        if 'id' in event:
            self.id = event['id']

        if not 'action' in event:
            raise KeyError('action must be specified')
        else:
            self.action = event['action']

        ##
        # Default status when creating the event is NEW
        if 'status' in event:
            self.status = event['status']
        else:
            self.status = EventStatus.NEW

        if 'message' in event:
            self.messages = event['messages']
        else:
            self.messages = []

        ##
        # User making the request
        #
        if 'user' in event:
            self.user = event['user']
        else:
            raise ValueError('User id must be specified')

        if 'object' in event:
            self.object = event['object']
        else:
            raise ValueError('Object must be specified')

        if 'changes' in event:
            self.changes = event['changes']

        if 'created' in event:
            self.e['created'] = format_date(event['created'])
        else:
            self.e['created'] = format_date()

        if 'updated' in event:
            self.updated(format_date(event['updated']))



    def __str__(self):
        return json.dumps(self.e, cls=DecimalEncoder, default=DateEncoder)

    def dict(self):
        return self.e

    ##
    # Id
    @property
    def id(self):
        if 'id' in self.e:
            return self.e['id']

    @id.setter
    def id(self, value):
        self.e['id'] = value

    ##
    # Action
    @property
    def action(self):
        return self.e['action']

    @action.setter
    def action(self, value):
        if isinstance(value, EventAction):
            self.e['action'] = value.value
        elif value in EventAction.__members__:
            self.e['action'] = value
        else:
            raise ValueError('Event Action not valid')

    ##
    # Status
    @property
    def status(self):
        return self.e['status']

    @status.setter
    def status(self, value):
        if isinstance(value, EventStatus):
            self.e['status'] = value.value
        elif value in EventStatus.__members__:
            self.e['status'] = value
        else:
            raise ValueError('Event Status not valid')

    ##
    # Message
    # This is a list of messages that get added during
    # the event life (info, error, messages)
    @property
    def messages(self):
        return self.e['messages']

    @messages.setter
    def messages(self, value=None):
        if isinstance(value, str):
            self.e['messages'].append(value)
        else:
            self.e['messages'] = value

    ##
    # User
    @property
    def user(self):
        return self.e['user']

    @user.setter
    def user(self, value):
        self.e['user'] = value

    ##
    # Object
    @property
    def object(self):
        return self.e['object']

    @object.setter
    def object(self, value):
        self.e['object'] = Object(value).dict()

    # ##
    # # Changes
    # @property
    # def changes(self):
    #     return self.e['changes']
    #
    # @changes.setter
    # def changes(self, value):
    #     if not all(k in value for k in ("type")):
    #         raise ValueError('Changes must have at least type')
    #
    #     self.e['changes'] = value

    def updated(self, value=None):
        if value:
            self.e['updated'] = value
        else:
            self.e['updated'] = format_date()

class RequestStatus(Enum):
    """
    Status for requests
    """
    PENDING = "PENDING"
    DENIED = "DENIED"
    APPROVED = "APPROVED"
    ERROR = "ERROR"
    WARNING = "WARNING"

class Request(object):
    """
        {
            status: RequestStatus
            message: String
            object: {}
            user: <id>
            created: <date>
            updated: <date>
        }

    """

    def __init__(self, request):
        self.e = {}

        if 'status' in request:
            self.status = request['status']
        else:
            self.status = RequestStatus.PENDING

        if 'message' in request:
            self.messages = request['messages']
        else:
            self.messages = []

        ##
        # User making the request
        #
        if 'user' in request:
            self.user = request['user']
        else:
            raise ValueError('User id must be specified')

        ##
        # Object
        @property
        def object(self):
            return self.e['object']

        @object.setter
        def object(self, value):
            self.e['object'] = Object(value).dict()


    ##
    # Status
    @property
    def status(self):
        return self.e['status']

    @status.setter
    def status(self, value):
        if isinstance(value, RequestStatus):
            self.e['status'] = value.value
        elif value in RequestStatus.__members__:
            self.e['status'] = value
        else:
            raise ValueError('Request Status not valid')

    ##
    # Message
    # This is a list of messages that get added during
    # the request life (info, error, messages)
    @property
    def messages(self):
        return self.e['messages']

    @messages.setter
    def messages(self, value=None):
        if isinstance(value, str):
            self.e['messages'].append(value)
        else:
            self.e['messages'] = value

    ##
    # User
    @property
    def user(self):
        return self.e['user']

    @user.setter
    def user(self, value):
        self.e['user'] = value

    ##
    # Object
    @property
    def object(self):
        return self.e['object']

    @object.setter
    def object(self, value):
        self.e['object'] = Object(value).dict()

    def updated(self, value=None):
        if value:
            self.e['updated'] = value
        else:
            self.e['updated'] = format_date()


    # approves the request
    def approve(self):

        if not self.id:
            return False

        # update date of the request
        self.updated()

        # update the status of the request
        self.status = RequestStatus.APPROVED

    # denies the request
    def deny(self):

        if not self.id:
            return False

        # update date of the request
        self.updated()

        # update the status of the request
        self.status = RequestStatus.DENIED