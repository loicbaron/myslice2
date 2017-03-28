import json

import rethinkdb as r

from myslice.lib.util import myJSONEncoder
from myslice.web.rest import Api

from myslice.db.activity import Event, EventAction, ObjectType, DataType
from myslice.db import dispatch

from tornado import gen, escape

class SlicesHandler(Api):

    @gen.coroutine
    def get(self, id=None, o=None):
        """
            - GET /slices
                (public) Slices list

            - GET /slices/<urn|hrn>
                (public) Slice with <urn|hrn>

            - GET /slices/<id|hrn>/(users|resources)
                (auth) Users/Resources list of the slice with <id|hrn>

            :return:
            """

        slice = None
        response = []

        if not self.get_current_user():
            self.userError('permission denied user not logged in')
            return
        ##
        # if id (hrn|urn) is set we get the slice with id <urn|hrn>
        #
        if id:
            if self.isUrn(id):
                filter = {'id': id}

            elif self.isHrn(id):
                filter = {'hrn': id}

            else:
                self.userError('id or hrn format error')
                return

            cursor = yield r.table('slices') \
                .filter(filter) \
                .merge(lambda slice: {
                    'authority': r.table('authorities').get(slice['authority']) \
                       .pluck(self.fields_short['authorities']) \
                       .default({'id': slice['authority']})
                }) \
                .merge(lambda slice: {
                    'project': r.table('projects').get(slice['project']) \
                       .pluck(self.fields_short['projects']) \
                       .default({'id': slice['project']})
                }) \
                .merge(lambda slice: {
                    'users': r.table('users').get_all(r.args(slice['users']), index="id") \
                           .pluck(self.fields_short['users']).coerce_to('array')
                }) \
                .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                slice = yield cursor.next()

        ##
        # GET /slices
        #
        # returns list of slices
        #
        if not id and not o:
            cursor = yield r.table('slices') \
                .pluck(self.fields['slices']) \
                .merge(lambda slice: {
                    'authority': r.table('authorities').get(slice['authority']) \
                           .pluck(self.fields_short['authorities']) \
                           .default({'id': slice['authority']})
                }) \
                .merge(lambda slice: {
                    'project': r.table('projects').get(slice['project']) \
                           .pluck(self.fields_short['projects']) \
                           .default({'id': slice['project']})
                }) \
                .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                slice = yield cursor.next()
                response.append(slice)
        ##
        # GET /slices/<urn|hrn>
        #
        # returns slice with <hrn|urn>
        #
        elif not o and id:
            if not self.get_current_user():
                self.userError('permission denied user not logged in')
                return

            response.append(slice)


        ##
        # GET /slice/<urn|hrn>/users
        #
        # returns a list of users of slice with id urn|hrn
        #
        elif id and slice and o == 'users':

            response = yield r.table('users') \
                .get_all(r.args(slice['users']), index='id') \
                .pluck(self.fields['users']) \
                .merge(lambda user: {
                    'authority': r.table('authorities').get(user['authority']) \
                           .pluck(self.fields_short['authorities']) \
                           .default({'id': user['authority']})
                }) \
                .coerce_to('array').run(self.dbconnection)

        ##
        # GET /slice/<urn|hrn>/resources
        #
        # returns a list of resources in the slice with id urn|hrn
        #
        elif id and slice and o == 'resources':

            response = yield r.table('resources') \
                .get_all(r.args(slice['resources']), index='id') \
                .pluck(self.fields['resources']) \
                .merge(lambda resource: {
                    'testbeds': r.table('testbeds').get(resource['testbed']) \
                           .pluck(self.fields_short['testbeds']) \
                           .default({'id': resource['testbed']})
                }) \
                .coerce_to('array').run(self.dbconnection)

        else:
            self.userError("invalid request")
            return

        self.finish(json.dumps({'result': response}, cls=myJSONEncoder))

    @gen.coroutine
    def post(self, id=None, o=None):
        """
        POST /slices
        { shortname: string, project: string }
        :return:
        """
        if not self.get_current_user():
            self.userError('permission denied user not logged in')
            return

        if not self.request.body:
            self.userError("empty request")
            return

        try:
            data = escape.json_decode(self.request.body)
        except json.decoder.JSONDecodeError as e:
            self.userError("malformed request", e.msg)
            return

        try:
            # Check if the user has the right to create a slice under this project
            u = yield r.table('users').get(self.get_current_user()['id']).run(self.dbconnection)
            if isinstance(data['project'], dict):
                project_id = data['project']['id']
                data['project'] = project_id
            if data['project'] in u['pi_authorities']:
                    data['authority'] = data['project']
            else:
                self.userError("your user has no rights on project: %s" % data['project'])
                return
        except Exception:
            self.userError("not authenticated or project not specified")
            return

        try:
            event = Event({
                'action': EventAction.CREATE,
                'user': self.get_current_user()['id'],
                'object': {
                    'type': ObjectType.SLICE,
                    'id': None,
                },
                'data': data
            })
        except AttributeError as e:
            self.userError("Can't create request", e)
            return
        except Exception as e:
            self.userError("Can't create request", e)
            return
        else:
            result = yield dispatch(self.dbconnection, event)

            self.write(json.dumps(
                {
                    "result": "success",
                    "events": result['generated_keys'],
                    "error": None,
                    "debug": None,
                }, cls=myJSONEncoder))

    @gen.coroutine
    def put(self, id=None, o=None):
        """
        PUT /slices/<id>
        :return:
        """

        events = []
        response = []

        if not self.get_current_user():
            self.userError('permission denied user not logged in')
            return

        if not self.request.body:
            self.userError("empty request")
            return

        if self.isUrn(id):
            filter = {'id': id}
        elif self.isHrn(id):
            filter = {'hrn': id}
        else:
            self.userError('id or hrn format error')
            return

        try:
            data = escape.json_decode(self.request.body)
        except json.decoder.JSONDecodeError as e:
            self.userError("malformed request", e.msg)
            return

        cursor = yield r.table('slices') \
            .filter(filter) \
            .run(self.dbconnection)

        while (yield cursor.fetch_next()):
            slice = yield cursor.next()

        if not slice:
            self.userError("problem with db")
            return

        # handle authority as dict
        if "authority" in data and type(data["authority"]) is dict:
            data["authority"] = data["authority"]["id"]

        # handle project as dict
        if "project" in data and type(data["project"]) is dict:
            data["project"] = data["project"]["id"]

        # handle user as dict
        if all(isinstance(n, dict) for n in data['users']):
            data['users'] = [x['id'] for x in data['users']]

        ## adding users
        #events += self.add_users(data, slice)

        ## removing users
        #events += self.remove_users(data, slice)

        ## adding resources
        #e = self.add_resources(data, slice)
        #if e:
        #    events.append(e)

        ## removing resources
        #e = self.remove_resources(data, slice)
        #if e:
        #    events.append(e)

        # update slice
        e = self.update_slice(data, slice)
        if e:
            events.append(e)

        for e in events:
            result = yield dispatch(self.dbconnection, e)
            response.append(result['generated_keys'])

        # Leases: handled by POST /leases and DELETE /leases/<id>

        self.write(json.dumps(
            {
                "result": "success",
                "events": response,
                "error": None,
                "debug": None,
            }, cls=myJSONEncoder))

    @gen.coroutine
    def delete(self, id, o=None):
        """
        DELETE /slices/<id>
        :return:
        """
        if not self.get_current_user():
            self.userError('permission denied user not logged in')
            return
        try:
            # Check if the user has the right to delete a slice
            s = yield r.table('slices').get(id).run(self.dbconnection)
            u = yield r.table('users').get(self.get_current_user()['id']).run(self.dbconnection)
            if not self.get_current_user()['id'] in s['users'] and s['authority'] not in u['pi_authorities']:
                self.userError("your user has no rights on slice: %s" % id)
                return
        except Exception:
            self.userError("not authenticated or project not specified")
            return

        try:
            event = Event({
                'action': EventAction.DELETE,
                'user': self.get_current_user()['id'],
                'object': {
                    'type': ObjectType.SLICE,
                    'id': id,
                }
            })
        except AttributeError as e:
            self.userError("Can't create request", e)
            return
        except Exception as e:
            self.userError("Can't create request", e)
            return
        else:
            result = yield dispatch(self.dbconnection, event)

            self.write(json.dumps(
                {
                    "result": "success",
                    "events": result['generated_keys'],
                    "error": None,
                    "debug": None,
                }, cls=myJSONEncoder))

    ##
    # generates an event for adding users
    def add_users(self, data, slice):
        events = []

        # check if the users in the request are in the slice
        for data_user in data['users']:
            if isinstance(data_user, dict):
                data_user = data_user['id']
            if data_user not in slice['users']:
                # create event add user to slices
                try:
                    event = Event({
                        'action': EventAction.ADD,
                        'user': self.get_current_user()['id'],
                        'object': { 'type': ObjectType.SLICE, 'id': slice['id'] },
                        'data': { 'type': DataType.USER, 'values': data_user }
                    })
                except Exception as e:
                    # TODO: we should log here
                    #log.error("Can't create request....")
                    pass
                else:
                    events.append(event)

        return events

    ##
    # generates an event for removing users
    def remove_users(self, data, slice):
        events = []

        data_users = [d['id'] if isinstance(d,dict) else d for d in data['users']]
        # check if we need to remove users from the slice
        for user in slice['users']:
            if user not in data_users:
                # create event remove user from slice
                try:
                    event = Event({
                        'action': EventAction.REMOVE,
                        'user': self.get_current_user()['id'],
                        'object': { 'type': ObjectType.SLICE, 'id': slice['id'] },
                        'data': { 'type': DataType.USER, 'values': user }
                    })
                except Exception as e:
                    # TODO: we should log here
                    # log.error("Can't create request....")
                    pass
                else:
                    events.append(event)

        return events

    ##
    # generates an event for adding resources
    def add_resources(self, data, slice):
        resources = []

        # XXX Resource as a dict should be handled
        for data_resource in data['resources']:
            if isinstance(data_resource, dict):
                data_resource = data_resource['id']
            if data_resource not in slice['resources']:
                resources.append(data_resource)

        if not resources:
            return False

        # dispatch event add resource to slices
        try:
            event = Event({
                'action': EventAction.ADD,
                'user': self.get_current_user()['id'],
                'object': { 'type': ObjectType.SLICE, 'id': slice['id'] },
                'data': { 'type': DataType.RESOURCE, 'values': resources }
            })
        except Exception as e:
            # TODO: we should log here
            # log.error("Can't create request....")
            return False
        else:
            return event

    ##
    # generates an event for removing resources
    def remove_resources(self, data, slice):
        resources = []

        data_resources = [d['id'] if isinstance(d,dict) else d for d in data['resources']]
        # XXX Resource as a dict should be handled
        for data_resource in slice['resources']:
            if data_resource not in data_resources:
                resources.append(data_resource)

        if not resources:
            return False

        # dispatch event remove resource from slice
        try:
            event = Event({
                'action': EventAction.REMOVE,
                'user': self.get_current_user()['id'],
                'object': { 'type': ObjectType.SLICE, 'id': slice['id'] },
                'data': { 'type': DataType.RESOURCE, 'values': resources }
            })
        except Exception as e:
            # TODO: we should log here
            # log.error("Can't create request....")
            return False
        else:
            return event

    def update_slice(self, data, slice):
        # update slice data only if it has changed
        # TODO: check what we can change

        # Update slice properties
        try:
            event = Event({
                'action': EventAction.UPDATE,
                'user': self.get_current_user()['id'],
                'object': {
                    'type': ObjectType.SLICE,
                    'id': slice['id']
                },
                'data': data
            })
        except Exception as e:
            # TODO: we should log here
            log.error("Can't create event")
            log.errpr(e)
            return False
        else:
            return event
