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
from rethinkdb import r, RqlDriverError
from myslice import settings as s
from myslice.lib.util import format_date, DecimalEncoder, DateEncoder

logger = logging.getLogger("myslice.event")

class EventStatus(Enum):
    """
        Status Class
    """
    ##
    # Status for EventAction.ADD, EventAction.MOD, EventAction.DEL
    #
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    WARNING = "WARNING"

    ##
    # Status for requests (EventAction.REQ)
    #
    PENDING = "PENDING"
    REFUSED = "REFUSED"
    APPROVED = "APPROVED"

class EventAction(Enum):
    ADD = "ADD"
    DEL = "DEL"
    MOD = "MOD"
    REQ = "REQ"

class EventObjectType(Enum):
    AUTHORITY = "AUTHORITY"
    PROJECT = "PROJECT"
    SLICE = "SLICE"
    USER = "USER"
    RESOURCE = "RESOURCE"

class EventObject(object):

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
        if isinstance(value, EventObjectType):
            self.e['type'] = value.value
        elif value in EventObjectType.__members__:
            self.e['type'] = value
        else:
            raise ValueError('Event Object Type is not valid')

    ##
    # ID of the object type
    @property
    def id(self):
        return self.e['id']

    @id.setter
    def id(self, value):
        self.e['id'] = value


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

        self.action = event['action']

        self.status = event['status']

        if 'message' in event:
            self.message = event['message']
        else:
            self.message = ''

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

    @action.setter
    def status(self, value):
        if isinstance(value, EventStatus):
            self.e['status'] = value.value
        elif value in EventStatus.__members__:
            self.e['status'] = value
        else:
            raise ValueError('Event Status not valid')

    ##
    # Message
    @property
    def message(self):
        return self.e['message']

    @message.setter
    def message(self, value=''):
        self.e['message'] = value

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
        self.e['object'] = EventObject(value).dict()

    ##
    # Changes
    @property
    def changes(self):
        return self.e['changes']

    @changes.setter
    def changes(self, value):
        if not all(k in value for k in ("type")):
            raise ValueError('Changes must have at least type')

        self.e['changes'] = value

    def updated(self, value=None):
        if value:
            self.e['updated'] = value
        else:
            self.e['updated'] = format_date()

    ##
    # Dispatches the event. This uses rethinkdb as backend
    def dispatch(self):
        # update date of the event
        self.updated()

        # connect to db
        logger.info("Connecting to db {} on {}:{}".format(s.db.name, s.db.host, s.db.port))
        try:
            c = r.connect(host=s.db.host, port=s.db.port, db=s.db.name)
        except RqlDriverError:
            logger.error("Can't connect to RethinkDB")
            raise SystemExit("Can't connect to RethinkDB")

        if self.id:
            ##
            # updating existing event
            ret = r.db(s.db.name).table('events').get(self.id).update(self.dict()).run(c)
        else:
            ##
            # dispatching new event
            ret = r.db(s.db.name).table('events').insert(self.dict()).run(c)

        import pprint
        pprint.pprint(ret)
        if ret['errors'] > 0:
            self.message = ret['first_error']
            self.status = EventStatus.ERROR
            return False
        elif ret['inserted'] > 0:
            self.id = ret['generated_keys'][0]

        return True