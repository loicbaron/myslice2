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
from myslice.lib.util import format_date, myJSONEncoder

logger = logging.getLogger("myslice.activity")

class ObjectType(Enum):
    AUTHORITY = "AUTHORITY"
    PROJECT = "PROJECT"
    SLICE = "SLICE"
    USER = "USER"
    RESOURCE = "RESOURCE"

    def __str__(self):
        return str(self.value)

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
        return json.dumps(self.dict(), cls=myJSONEncoder)

    def dict(self):
        ret = {}
        for k in self.e:
            if isinstance(self.e[k], Enum):
                ret[k] = self.e[k].value
            else:
                ret[k] = self.e[k]
        return ret

    ##
    # Object Type
    @property
    def type(self):
        return self.e['type']

    @type.setter
    def type(self, value):
        if isinstance(value, ObjectType):
            self.e['type'] = value
        elif value in ObjectType.__members__:
            self.e['type'] = ObjectType[value]
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
    # RUNNING the operation is running
    RUNNING = "RUNNING"
    # SUCCESSfully terminated
    SUCCESS = "SUCCESS"
    # ERROR or WARNING occurred during processing
    ERROR = "ERROR"
    WARNING = "WARNING"

    def __str__(self):
        return str(self.value)

class EventRequest(Enum):
    ##
    # If Event is REQ (Request)
    PENDING = "PENDING"
    DENIED = "DENIED"
    APPROVED = "APPROVED"

    def __str__(self):
        return str(self.value)

class EventAction(Enum):
    """

    """
    # add an object
    ADD = "ADD"
    # delete an object
    DEL = "DEL"
    # modify an object
    MOD = "MOD"
    # event will be a request
    REQ = "REQ"

    def __str__(self):
        return str(self.value)

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

        if 'log' in event:
            self.log = event['log']
        else:
            self.log = []

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
        # Event Request status
        if 'request' in event:
            self.request = event['request']
        elif self.isRequest():
            self.pending()
        else:
            self.request = None

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
        return json.dumps(self.dict(), cls=myJSONEncoder)

    def dict(self):
        ret = {}
        for k in self.e:
            if isinstance(self.e[k], Enum):
                ret[k] = self.e[k].value
            elif isinstance(self.e[k], Object):
                ret[k] = self.e[k].dict()
            else:
                ret[k] = self.e[k]
        return ret

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
            self.e['action'] = value
        elif value in EventAction.__members__:
            self.e['action'] = EventAction[value]
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
            status = value
        elif value in EventStatus.__members__:
            status = EventStatus[value]
        else:
            raise Exception("Event Status not valid")

        # update date of the request
        self.updated()

        self.e['status'] = status

    ##
    # Request Status
    @property
    def request(self):
        return self.e['request']

    @request.setter
    def request(self, value):

        if not self.isRequest():
            raise Exception('Only Event of type REQUEST can have a PENDING/APPROVED/DENIED status')

        if isinstance(value, EventRequest):
            request_status = value
        elif value in EventRequest.__members__:
            request_status = EventRequest[value]
        else:
            raise Exception("Event Request Status not valid")

        # update date of the request
        self.updated()

        self.e['request'] = request_status


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
    # Log
    # This is a list of log messages that get added during
    # the event life (info, error, messages)
    @property
    def log(self):
        return self.e['log']

    @log.setter
    def log(self, value=None):
        if isinstance(value, str):
            self.e['log'].append(value)
        else:
            self.e['log'] = value
    ##
    # User creating the Event
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
        self.e['object'] = Object(value)

    ##
    # Data
    @property
    def data(self):
        return self.e['data']

    @data.setter
    def data(self, value):
        if not isinstance(value, dict) and not isinstance(value, list):
            self.messages = "Invalid format for data (must be a dict or a list)"
            raise Exception(self.messages)
        else:
            self.e['data'] = value

    def updated(self, value=None):
        if value:
            self.e['updated'] = value
        else:
            self.e['updated'] = format_date()

    ##
    # Action
    def _checkAction(self, action):
        if (self.action == action):
            return True
        return False

    def isRequest(self):
        return self._checkAction(EventAction.REQ)

    def addingObject(self):
        return self._checkAction(EventAction.ADD)

    def modifyingObject(self):
        return self._checkAction(EventAction.MOD)

    def removingObject(self):
        return self._checkAction(EventAction.DEL)

    ##
    # Status
    def _checkStatus(self, status):
        if self.status == status:
            return True
        return False

    def isNew(self):
        return self._checkStatus(EventStatus.NEW)

    def isWaiting(self):
        return self._checkStatus(EventStatus.WAITING)

    def isRunning(self):
        return self._checkStatus(EventStatus.RUNNING)

    def isSuccess(self):
        return self._checkStatus(EventStatus.SUCCESS)

    def hasErrors(self):
        return self._checkStatus(EventStatus.ERROR)

    def hasWarnings(self):
        return self._checkStatus(EventStatus.WARNING)

    ##
    # RequestStatus
    def _checkRequestStatus(self, status):
        if self.request == status:
            return True
        return False

    def isPending(self):
        return self._checkRequestStatus(EventRequest.PENDING)

    def isApproved(self):
        return self._checkRequestStatus(EventRequest.APPROVED)

    def isDenied(self):
        return self._checkRequestStatus(EventRequest.DENIED)

    ##
    # Ready for being processed
    def isReady(self):
        if (self.isRequest() and self.isApproved()):
            return True

        if (not self.isRequest() and self.isWaiting()):
            return True

        return False


    def waiting(self):
        '''
        Set the event to waiting
        :return:
        '''
        if not self.id:
            raise Exception('Missing required Id')

        self.status = EventStatus.WAITING

    def running(self):
        '''
        Set the event to running
        :return:
        '''
        if not self.id:
            raise Exception('Missing required Id')

        self.status = EventStatus.RUNNING

    def success(self):
        '''
        Set the event to success
        :return:
        '''
        if not self.id:
            raise Exception('Missing required Id')

        self.status = EventStatus.SUCCESS

    def error(self):
        '''
        Set the event to error
        :return:
        '''
        self.status = EventStatus.ERROR

    def warning(self):
        '''
        Set the event to warning
        :return:
        '''
        self.status = EventStatus.WARNING

    def pending(self):
        '''
        Set the event request to pending
        :return:
        '''

        self.request = EventRequest.PENDING

    # Approves the request
    def approve(self):
        '''
        Set the event request to approved
        :return:
        '''
        if not self.id:
            raise Exception('Missing required Id')

        self.request = EventRequest.APPROVED

    ##
    # Denies the request
    def deny(self):
        '''
        Set the event request to denied
        :return:
        '''
        if not self.id:
            raise Exception('Missing required Id')

        self.request = EventRequest.DENIED