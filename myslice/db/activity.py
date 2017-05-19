#
#   MySlice version 2
#
#   Activity model: defines Event and Request classes
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

import logging
from enum import Enum
from myslice.lib.util import format_date
import sys
import traceback

logger = logging.getLogger("myslice.activity")

class ObjectType(Enum):
    AUTHORITY = "AUTHORITY"
    PROJECT = "PROJECT"
    SLICE = "SLICE"
    USER = "USER"
    RESOURCE = "RESOURCE"
    PASSWORD = "PASSWORD"
    LEASE = "LEASE"

    def __str__(self):
        return str(self.value)

class DataType(Enum):
    USER = "USER"
    RESOURCE = "RESOURCE"
    PI = "PI"
    KEY = "KEY"

    def __str__(self):
        return str(self.value)
    

class EventStatus(Enum):
    """
    Event Status: new events will automatically have a NEW status,
    once dispatched a new event will be treated and its status will change
    """
    # INIT is the initial status for previous_status 
    INIT = "INIT"
    # NEW created event, this will be processed
    NEW = "NEW"
    # If the event needs an external interaction
    CONFIRM = "CONFIRM"
    PENDING = "PENDING"
    DENIED = "DENIED"
    APPROVED = "APPROVED"
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

class EventAction(Enum):
    """
    Action definitions for the event entity

    CREATE / DELETE / UPDATE for the object
    ADD / REMOVE reference/link to another object
    (e.g. add/remove user to/from slice )

    """
    # CRUD operations on objects
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

    # Modifications on objects
    ADD = "ADD"
    REMOVE = "REMOVE"

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


class DataObject(Dict):

    def __init__(self, data):
        try:
            self.type = data['type']
        except KeyError:
            raise Exception('Data Type not specified')

        try:
            self.values = data['values']
        except KeyError:
            raise Exception('Data Values not specified')
    
    @property
    def values(self):
        return self['values']

    @values.setter
    def values(self, value):
        self['values'] = value

    @property
    def type(self):
        return self['type']

    @type.setter
    def type(self, value):
        if isinstance(value, DataType):
            self['type'] = value
        elif value in DataType.__members__:
            self['type'] = DataType[value]
        else:
            raise Exception('Object Type {} not valid'.format(value))

    def dict(self):
        ret = {}
        for k in self.keys():
            if isinstance(self[k], Enum):
                ret[k] = self[k].value
            else:
                ret[k] = self[k]
        return ret


class Object(Dict):

    def __init__(self, obj):
        try:
            self.type = obj['type']
        except KeyError:
            raise Exception('Object Type not specified')

        try:
            self.id = obj['id']
        except KeyError:
            raise Exception('Object Id not specified', sys.exc_info())

    
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
            action: <EventAction>
            status: <EventStatus>
            previous_status: <EventStatus>
            log: [{
                timestamp: <timestamp>
                message: <String>
                type: <info|warning|error|debug>
            }]
            messages: [{
                timestamp: <timestamp>
                message: <String>
                from: <String>
            }]
            object: <Object>
            data: { [<mixed>] }
            user: <id>
            created: <date>
            updated: <date>
            notify: true|false (if true notify user by email)
            manager: <String>
        }

    """

    def __init__(self, event):
    
        self['messages'] = event.get('messages', [])
        self['log'] = event.get('log', [])
        
        ##
        # Default status when creating the event is NEW
        self.previous_status = event.get('previous_status', EventStatus.INIT) 
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
        #
        if 'data' in event:
            self.data = event['data']
        else:
            self.data = {}
        #try:
        #    self.data = event['data']
        #except KeyError as e:
        #    import traceback
        #    traceback.print_exc()
        #    self.data = {}

        try:
            self['created'] = format_date(event['created'])
        except KeyError:
            self['created'] = format_date()

        try:
            self.updated(format_date(event['updated']))
        except KeyError:
            pass

        ##
        # Notify the user
        try:
            self.notify = event['notify']
        except KeyError:
            self.notify = False

        try:
            self.manager = event['manager']
        except KeyError:
            self.manager = None

    @property
    def notify(self):
        return self['notify']

    @notify.setter
    def notify(self, value=True):
        self['notify'] = value
        
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
        if 'status' in self:
            self.previous_status = self['status']
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
    # Previous Status
    # Can change during the life of the event
    @property
    def previous_status(self):
        return self['previous_status']

    @previous_status.setter
    def previous_status(self, value):
        if isinstance(value, EventStatus):
            status = value
        elif value in EventStatus.__members__:
            status = EventStatus[value]
        else:
            raise Exception("Event Previous Status not valid")

        self['previous_status'] = status

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
            raise Exception("Invalid format for data (must be a dict or a list)")

        if 'type' in value:
            self['data'] = DataObject(value)
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
            elif isinstance(self[k], DataObject):
                ret[k] = self[k].dict()
            else:
                ret[k] = self[k]
        return ret

    ##
    # Send messages about an event
    # from_user
    # message
    # timestamp
    def message(self, from_user, message=None):
        self['messages'].append({
            'from': from_user,
            'message': message,
            'timestamp': format_date(),
        })

    ##
    # Manager that approve / deny the Event
    # Used to save the object using manager's credentials
    @property
    def manager(self):
        return self['manager']

    @manager.setter
    def manager(self, user_id):
        self['manager'] = user_id

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
    # Log WARNING
    def logWarning(self, message=None):
        if message:
            self._log('warning', message)
        else:
            return self._log('warning')

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

    def creatingObject(self):
        return self._checkAction(EventAction.CREATE)

    def updatingObject(self):
        return self._checkAction(EventAction.UPDATE)

    def deletingObject(self):
        return self._checkAction(EventAction.DELETE)

    def addingObject(self):
        return self._checkAction(EventAction.ADD)

    def removingObject(self):
        return self._checkAction(EventAction.REMOVE)

    ##
    # Check Status
    def _checkStatus(self, status):
        if self.status == status:
            return True
        return False

    def isNew(self):
        return self._checkStatus(EventStatus.NEW)

    def isWaiting(self):
        return self._checkStatus(EventStatus.WAITING)

    def setWaiting(self):
        '''
        Set the event to waiting
        :return:
        '''
        if not self.id:
            raise Exception('Missing required Id')

        if self.isNew() or self.isApproved():
            self.status = EventStatus.WAITING
        else:
            raise Exception('Event must be in state NEW or APPROVED before WAITING')

    def isRunning(self):
        return self._checkStatus(EventStatus.RUNNING)

    def setRunning(self):
        '''
        Set the event to running
        :return:
        '''
        if not self.id:
            raise Exception('Missing required Id')

        if not self.isReady():
            raise Exception('Event must be in WAITING or APPROVED state before RUNNING')

        self.status = EventStatus.RUNNING

    def isSuccess(self):
        return self._checkStatus(EventStatus.SUCCESS)

    def setSuccess(self):
        '''
        Set the event to success
        :return:
        '''
        if not self.id:
            raise Exception('Missing required Id')

        #if not self.isRunning():
        #    raise Exception('Event must be in RUNNING state before SUCCESS')

        self.status = EventStatus.SUCCESS

    def hasErrors(self):
        return self._checkStatus(EventStatus.ERROR)

    def isError(self):
        return self._checkStatus(EventStatus.ERROR)

    def setError(self):
        '''
        Set the event to error
        :return:
        '''
        #if not self.isRunning():
        #    raise Exception('Event must be in RUNNING state before ERROR')

        self.status = EventStatus.ERROR

    def hasWarnings(self):
        return self._checkStatus(EventStatus.WARNING)

    def isWarning(self):
        return self._checkStatus(EventStatus.WARNING)

    def setWarning(self):
        '''
        Set the event to warning
        :return:
        '''

        if not self.isRunning():
            raise Exception('Event must be in RUNNING state before WARNING')

        self.status = EventStatus.WARNING

    def isConfirm(self):
        return self._checkStatus(EventStatus.CONFIRM)

    def setConfirm(self):
        '''
        Set the event request to confirm
        used when a user needs to confirm his/her email address
        :return:
        '''
        if not self.isNew():
            raise Exception('Event must be in state NEW before CONFIRM')

        self.status = EventStatus.CONFIRM

        # notify user by default
        self.notify = True

    def isPending(self):
        return self._checkStatus(EventStatus.PENDING)

    def setPending(self):
        '''
        Set the event request to pending
        :return:
        '''
        if not self.isNew() and not self.isConfirm():
            raise Exception('Event must be in state NEW or CONFIRM before PENDING')

        self.status = EventStatus.PENDING

        # notify user by default
        self.notify = True

    def isApproved(self):
        return self._checkStatus(EventStatus.APPROVED)

    # Approves the request
    def setApproved(self):
        '''
        Set the event request to approved
        :return:
        '''
        if not self.id:
            raise Exception('Missing required Id')

        if not self.isPending():
            raise Exception('Event must be in PENDING state before APPROVED')

        self.status = EventStatus.APPROVED

    def isDenied(self):
        return self._checkStatus(EventStatus.DENIED)

    ##
    # Denies the request
    def setDenied(self):
        '''
        Set the event request to denied
        :return:
        '''
        if not self.id:
            raise Exception('Missing required Id')

        if not self.isPending():
            raise Exception('Event must be in PENDING state before DENIED')

        self.status = EventStatus.DENIED

    ##
    # Ready for being processed
    def isReady(self):
        if self.isApproved() or self.isWaiting():
            return True

        return False
