import json

import rethinkdb as r

from myslice.lib.util import myJSONEncoder
from myslice.web.rest import Api

from myslice import db
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

        # convert resources as string to dict
        # we need resources as dict to get the configuration of resources
        if any(isinstance(n, str) for n in data['resources']):
            try:
                resources = []
                for x in data['resources']:
                    if isinstance(x, str):
                        resource = yield self.getResource(x)
                    else:
                        resource = x
                    resources.append(resource)
                data['resources'] = resources
            except Exception as e:
                import traceback
                traceback.print_exc()
                self.userError("resource id wrong or unknown")
                return

        # All the logic happens in services.workers.slices
        # Worker compares the current Slice in DB and the event.data sent

        ## adding users
        ## removing users
        ## adding resources
        ## removing resources

        # update slice
        event = self.update_slice(data, slice)
        result = yield dispatch(self.dbconnection, event)

        # Leases: handled by POST /leases and DELETE /leases/<id>

        self.write(json.dumps(
            {
                "result": "success",
                "events": result['generated_keys'],
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
            # Check if the user isAdmin 
            admin = self.isAdmin()
            if not admin:
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
    # get a resource from its id
    @gen.coroutine
    def getResource(self, id):
        print(id)
        resource = yield r.table('resources').get(id).run(self.dbconnection)
        print("getResource = ")
        from pprint import pprint
        pprint(resource)
        if not resource:
            raise Exception("Resource %s not found" % id)
        return resource

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
