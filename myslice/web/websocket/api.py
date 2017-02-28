from enum import Enum
import json
from myslice.lib.util import myJSONEncoder

class Object(Enum):
    authorities = "authorities"
    projects = "projects"
    slices = "slices"
    users = "users"
    resources = "resources"
    activities = "activities"

    def __str__(self):
        return str(self.value)

class Command(Enum):
    authenticate = "authenticate"
    watch = "watch"
    unwatch = "unwatch"
    count = "count"

class Event(Enum):
    created = "created"
    updated = "updated"
    deleted = "deleted"

class Message(dict):

    def __init__(self, request):
        self._payload = json.loads(request)

        try:
            self.command = self._payload['command']
        except KeyError:
            raise Exception("Command not specified")

        if not self.command == Command.authenticate:
            try:
                self.object = self._payload['object']
            except KeyError:
                raise Exception("Object not specified")

    def dict(self):
        ret = {}
        for k in self.keys():
            if isinstance(self[k], Enum):
                ret[k] = self[k].value
            elif isinstance(self[k], Object):
                ret[k] = self[k].dict()
            elif isinstance(self[k], Command):
                ret[k] = self[k].dict()
            elif isinstance(self[k], Event):
                ret[k] = self[k].dict()
            else:
                ret[k] = self[k]
        return ret

    def json(self):
        return json.dumps(self.dict(), ensure_ascii=False, cls=myJSONEncoder)

    ##
    # Command
    @property
    def command(self):
        return self['command']

    @command.setter
    def command(self, value):
        if isinstance(value, Command):
            self['command'] = value
        elif value in Command.__members__:
            self['command'] = Command[value]
        else:
            raise Exception("Command not valid")

    ##
    # Object
    @property
    def object(self):
        return self['object']

    @object.setter
    def object(self, value):
        if isinstance(value, Object):
            self['object'] = value
        elif value in Object.__members__:
            self['object'] = Object[value]
        else:
            raise Exception("Object not valid")


class Request(Message):

    def __init__(self, request):
        super().__init__(request)

        if self.command == Command.authenticate:
            try:
                self.token = self._payload['token']
            except KeyError:
                raise Exception("Missing authentication token")

    ##
    # Authentication token
    @property
    def token(self):
        return self['token']

    @token.setter
    def token(self, value):
        self['token'] = value

    def isAuthenticating(self):
        return self.command == Command.authenticate

    def isWatching(self):
        return self.command == Command.watch

    def isUnwatching(self):
        return self.command == Command.unwatch

    def isCounting(self):
        return self.command == Command.count


class Response(Message):

    def __init__(self, request, message=None, code=1):

        if not isinstance(request, Request):
            raise Exception("Wrong Request type")

        self.request = request

        # defaults to code 1 OK
        self.result = {
            "code": code,
            "message": message
        }

    def json(self):
        return json.dumps({
            "command": self.request.command,
            "result": self.result
        }, ensure_ascii=False, cls=myJSONEncoder)

class ResponseError(Response):

    def __init__(self, request, message=None, code=0):
        super().__init__(request, message, code)

class Stream(Message):

    def __init__(self, command, object, data, event):
        try:
            self.command = command
        except KeyError:
            raise Exception("Command not specified")

        try:
            self.object = object
        except KeyError:
            raise Exception("Object not specified")

        try:
            self.data = data
        except KeyError:
            raise Exception("Data not specified")

        try:
            self.event = event
        except KeyError:
            raise Exception("Event not specified")

    ##
    # Data
    @property
    def data(self):
        return self['data']

    @data.setter
    def data(self, value):
        if not isinstance(value, dict) and not isinstance(value, list):
            raise Exception("Invalid format for data (must be a dict)")

        self['data'] = value

    ##
    # Event
    @property
    def event(self):
        return self['event']

    @event.setter
    def event(self, value):
        if isinstance(value, Event):
            self['event'] = value
        elif value in Event.__members__:
            self['event'] = Event[value]
        else:
            raise Exception("Event not valid")