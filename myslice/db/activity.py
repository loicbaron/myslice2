##
#   MySlice version 2
#
#   Activity model: defines Event and Request classes
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

import json
import logging
from enum import Enum
from myslice.lib.util import format_date, DecimalEncoder, DateEncoder

logger = logging.getLogger("myslice.activity")

class ObjectType(Enum):
    AUTHORITY = "AUTHORITY"
    PROJECT = "PROJECT"
    SLICE = "SLICE"
    USER = "USER"
    RESOURCE = "RESOURCE"

class Object(object):

    def __init__(self, obj):
        self.e = {}

        try:
            self.type = obj['type']
        except KeyError:
            raise Exception('Object Type not specified')

        try:
            self.id = obj['id']
        except KeyError:
            raise Exception('Object Id not specified')

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
            raise Exception('Object Type {} not valid'.format(value))

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

class Event(object):
    """
        {
            action: EventAction
            status: EventStatus
            messages: [String]
            object: {}
            data: {}
            user: <id>
            created: <date>
            updated: <date>
        }

    """

    def __init__(self, event):
        self.e = {}

        if 'message' in event:
            self.messages = event['messages']
        else:
            self.messages = []

        ##
        # If ID is present this is a previously
        # created event, or we don't set it
        if 'id' in event:
            self.id = event['id']

        if not 'action' in event:
            self.messages = "Event action not specified"
            raise Exception(self.messages)
        else:
            self.action = event['action']

        ##
        # Default status when creating the event is NEW
        if 'status' in event:
            self.status = event['status']
        else:
            self.status = EventStatus.NEW

        ##
        # User making the request
        #
        if 'user' in event:
            self.user = event['user']
        else:
            self.messages = "User Id not specified"
            raise Exception(self.messages)

        ##
        # Object of the event
        #
        if 'object' in event:
            try:
                self.object = event['object']
            except Exception as e:
                self.messages = "{0}".format(e)
                raise Exception(self.messages)
        else:
            self.messages = "Event Object not specified"
            raise Exception(self.messages)

        ##
        # data is a dictionary of changes for the object
        # action DEL does not need it
        if 'data' in event:
            self.data = event['data']
        else:
            if not self.action == EventAction.DEL:
                self.messages = "Data not specified for action {}".format(self.action)
                raise Exception(self.messages)

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
            self.messages = "Event Action not valid"
            raise Exception(self.messages)

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
            self.messages = "Event Status not valid"
            raise Exception(self.messages)

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

    ##
    # Data
    @property
    def data(self):
        return self.e['data']

    @data.setter
    def data(self, value):
        if not isinstance(value, dict):
            self.messages = "Invalid format for data (must be a dict)"
            raise Exception(self.messages)
        else:
            self.e['data'] = value

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
    The Request object can be created in the following ways:

    - req = Request(
                {
                    object: <Object>
                    data: {}
                    user: <id>
                }
            )
    This is a new request created from scratch. Status will
    be put on PENDING by default.

    - req = Request(
                {
                    status: "STATUS"
                    message: [Strings]
                    object: {
                        type: "OTYPE",
                        id: <id>
                    }
                    data: {
                        ...
                    }
                    user: <id>
                    created: <date>
                    updated: <date>
                }
            )
    The argument is a well formed dictionary, f.i. retrieved from db.
    The request here has been created before, we are retrieving it to
    perform operations/tasks, we then change state and dispatch it.

    - req = Request(<Event>)
    Creating a Request from an Event object. This wil create a new
    request (default status PENDING) and copy over from the event object
    the following values: object, data, user.

    """

    def __init__(self, request):
        self.r = {}

        ##
        # We can pass an event directly, this will create
        # a new request based on it, otherwise we can
        # create a new request from scratch or from a dictionary
        if isinstance(request, Event):
            self.status = RequestStatus.PENDING
            self.object = request.object
            self.data = request.data
            self.user = request.user
            self.r['created'] = format_date()
        else:
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
                self.messages = "User Id not specified"
                raise Exception(self.messages)

            ##
            # Object of the request
            #
            if 'object' in request:
                try:
                    self.object = request['object']
                except Exception as e:
                    self.messages = "{0}".format(e)
                    raise Exception(self.messages)
            else:
                self.messages = "Request Object not specified"
                raise Exception(self.messages)

            ##
            # data is a dictionary of changes for the object
            # action DEL does not need it
            if 'data' in request:
                self.data = request['data']
            else:
                if not self.action == EventAction.DEL:
                    self.messages = "Data not specified for action {}".format(self.action)
                    raise Exception(self.messages)

            if 'created' in request:
                self.r['created'] = format_date(request['created'])
            else:
                self.r['created'] = format_date()


    def __str__(self):
        return json.dumps(self.r, cls=DecimalEncoder, default=DateEncoder)

    def dict(self):
        return self.r

    ##
    # Status
    @property
    def status(self):
        return self.e['status']

    @status.setter
    def status(self, value):
        if isinstance(value, RequestStatus):
            self.r['status'] = value.value
        elif value in RequestStatus.__members__:
            self.r['status'] = value
        else:
            self.messages = "Request Status not valid"
            raise Exception(self.messages)

    ##
    # Message
    # This is a list of messages that get added during
    # the request life (info, error, messages)
    @property
    def messages(self):
        return self.r['messages']

    @messages.setter
    def messages(self, value=None):
        if isinstance(value, str):
            self.r['messages'].append(value)
        else:
            self.r['messages'] = value

    ##
    # User
    @property
    def user(self):
        return self.r['user']

    @user.setter
    def user(self, value):
        self.r['user'] = value

    ##
    # Object
    @property
    def object(self):
        return self.r['object']

    @object.setter
    def object(self, value):
        self.r['object'] = Object(value).dict()

    ##
    # Data
    @property
    def data(self):
        return self.r['data']

    @data.setter
    def data(self, value):
        if not isinstance(value, dict):
            self.messages = "Invalid format for data (must be a dict)"
            raise Exception(self.messages)
        else:
            self.r['data'] = value

    def updated(self, value=None):
        if value:
            self.r['updated'] = value
        else:
            self.r['updated'] = format_date()

    ##
    # Approves the request
    def approve(self):

        if not self.id:
            return False

        # update date of the request
        self.updated()

        # update the status of the request
        self.status = RequestStatus.APPROVED

    ##
    # Denies the request
    def deny(self):

        if not self.id:
            return False

        # update date of the request
        self.updated()

        # update the status of the request
        self.status = RequestStatus.DENIED