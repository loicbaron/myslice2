##
#   MySlice version 2
#
#   Activity model: defines Event and Request classes
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

import logging
from enum import Enum
from myslice.lib.util import format_date

logger = logging.getLogger("myslice.activity")

class ObjectType(Enum):
    AUTHORITY = "AUTHORITY"
    PROJECT = "PROJECT"
    SLICE = "SLICE"
    USER = "USER"
    RESOURCE = "RESOURCE"

    def __str__(self):
        return str(self.value)

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

class Dict(dict):
    '''
    A Base Dict class which support slice

    ''' 
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError("Dict object has no attribute {}".format(key))

class Object(Dict):

    def __init__(self, obj):
        try:
            self.type = obj['type']
        except KeyError:
            raise Exception('Object Type not specified')

        try:
            self.id = obj['id']
        except KeyError:
            raise Exception('Object Id not specified')
    
    ##
    # ID of the object type
    @property
    def id(self):
        return self['id']

    @id.setter
    def id(self, value):
        self['id'] = value

    @property
    def type(self):
        return self['type']

    @type.setter
    def type(self, value):
        if isinstance(value, ObjectType):
            self['type'] = value
        elif value in ObjectType.__members__:
            self['type'] = ObjectType[value]
        else:
            raise Exception('Object Type {} not valid'.format(value))

    def dict(self):
        ret = {}
        for k in self.keys():
            if isinstance(self[k], Enum):
                ret[k] = self[k].value
            elif isinstance(self[k], Object):
                ret[k] = self[k].dict()
            else:
                ret[k] = self[k]
        return ret


class Event(Dict):
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
    
        self['messages'] = event.get('messages', [])

        self['log'] = event.get('log', [])
        
        ##
        # Default status when creating the event is NEW
        self.status = event.get('status', EventStatus.NEW)

        try:
            self.action = event['action']
        except KeyError:
            raise Exception("Event action not specified")

        ##
        # If ID is present this is a previously
        # created event, or we don't set it
        try:
            self.id = event['id']
        except KeyError:
            pass

        ##
        # Event Request status
        if self.isRequest():
            try:
                self.request = event['request']
            except KeyError:
                self.pending()

        ##
        # User making the request
        #
        try:
            self.user = event['user']
        except KeyError:
            raise Exception("User Id not specified")

        ##
        # Object of the event
        #
        try:
            self.object = event['object']
        except KeyError:
            raise Exception("Event Object not specified")
        except Exception as e:
            raise Exception("{0}".format(e))

        ##
        # data is a dictionary of changes for the object
        # action DEL does not need it
        if not self.removingObject():
            try:
                self.data = event['data']
            except KeyError:
                raise Exception("Data not specified for action {}".format(self.action))

        try:
            self.created = format_date(event['created'])
        except KeyError:
            self.created = format_date()

        try:
            self.updated(format_date(event['updated']))
        except KeyError:
            pass

    ##
    # Id
    @property
    def id(self):
        if 'id' in self:
            return self['id']

    @id.setter
    def id(self, value):
        self['id'] = value

    ##
    # Action
    # This is only set at event creation
    @property
    def action(self):
        return self['action']

    @action.setter
    def action(self, value):
        if isinstance(value, EventAction):
            self['action'] = value
        elif value in EventAction.__members__:
            self['action'] = EventAction[value]
        else:
            raise Exception("Event Action not valid")

    ##
    # Status
    # Can change during the life of the event
    @property
    def status(self):
        return self['status']

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

        self['status'] = status

    ##
    # Request Status
    # Can change during the life of the request
    @property
    def request(self):
        return self['request']

    @request.setter
    def request(self, value):

        if value is None:
            self['request'] = None
            return

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

        self['request'] = request_status

    ##
    # User creating the Event
    @property
    def user(self):
        return self['user']

    @user.setter
    def user(self, value):
        self['user'] = value

    ##
    # Object
    @property
    def object(self):
        return self['object']

    @object.setter
    def object(self, value):
        self['object'] = Object(value)

    ##
    # Data
    @property
    def data(self):
        return self['data']

    @data.setter
    def data(self, value):
        if not isinstance(value, dict) and not isinstance(value, list):
            self.messages = "Invalid format for data (must be a dict or a list)"
            raise Exception(self.messages)
        else:
            self['data'] = value

    def updated(self, value=None):
        if value:
            self['updated'] = value
        else:
            self['updated'] = format_date()

    def dict(self):
        ret = {}
        for k in self.keys():
            if isinstance(self[k], Enum):
                ret[k] = self[k].value
            elif isinstance(self[k], Object):
                ret[k] = self[k].dict()
            else:
                ret[k] = self[k]
        return ret

    ##
    # Logging
    # Private method for managing logs of
    # the event life (info, error, messages)
    def _log(self, type='info', message=None):
        if message:
            self['log'].append({
                'type': type,
                'timestamp': format_date(),
                'message': message
            })
        else:
            return [el for el in self['log'] if el['type'] == type]

    ##
    # Log INFO
    def logInfo(self, message=None):
        if message:
            self._log('info', message)
        else:
            return self._log('info')

    ##
    # Log ERROR
    def logError(self, message=None):
        if message:
            self._log('error', message)
        else:
            return self._log('error')

    ##
    # Log DEBUG
    def logDebug(self, message=None):
        if message:
            self._log('debug', message)
        else:
            return self._log('debug')

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
