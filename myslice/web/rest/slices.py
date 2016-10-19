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

            - GET /slices/<id|hrn>
                (public) Slices with <id|hrn>

            - GET /slices/<id|hrn>/(users|resources)
                (auth) Users/Resources list of the slice with <id|hrn>

            :return:
            """

        response = []
        current_user = self.get_current_user()

        # GET /slices
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
                project = yield cursor.next()
                response.append(project)


        # GET /slices/<id>
        elif not o and id:

            if not current_user:
                self.userError('permission denied')
                return

            if self.isUrn(id):
                filter = {'id' : id}

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
                .run(self.dbconnection)
            while (yield cursor.fetch_next()):
                slice = yield cursor.next()
                response.append(slice)
        # Get /slice/id/[users/resources]
        elif id and o in ['users', 'resources']:
            if o == "users":
                cursor = yield r.table('users') \
                    .filter(lambda usr: usr['slices'].contains(id)) \
                    .run(self.dbconnection)
                while (yield cursor.fetch_next()):
                    item = yield cursor.next()
                    response.append(item)
            else:

                cursor = yield r.table('slices')\
                    .pluck('id','resources') \
                    .merge(lambda sli: {
                        'resources': r.table('resources').get_all(sli['resources'], index='id') \
                           .coerce_to('array')
                    }) \
                    .filter({'id': id})\
                    .run(self.dbconnection)
                while (yield cursor.fetch_next()):
                    item = yield cursor.next()
                    response.append(item)

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
            u = yield r.table('users').get(self.current_user['id']).run(self.dbconnection)
            if data['project'] in u['pi_authorities']:
                data['authority'] = data['project']
            else:
                self.userError("your user has no rights on project: %s" % data['project'])
        except Exception:
            self.userError("not authenticated or project not specified")
            return

        try:
            event = Event({
                'action': EventAction.CREATE,
                'user': self.current_user['id'],
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
                    "error": None,
                    "debug": None,
                    " events": result['generated_keys']
                }, cls=myJSONEncoder))

    @gen.coroutine
    def put(self, id=None, o=None):
        """
        PUT /slices/<id>
        :return:
        """

        response = []
        current_user = self.get_current_user()

        if not current_user:
            self.userError('not authenticated ')
            return

        if not self.request.body:
            self.userError("empty request")
            return
        if not current_user:
            self.userError('permission denied')
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
            # slice id from DB


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
            .run(self.dbconnection)

        while (yield cursor.fetch_next()):
            slice = yield cursor.next()

        # handle authority as dict
        if "authority" in data and type(data["authority"]) is dict:
            data["authority"] = data["authority"]["id"]

        # handle project as dict
        if "project" in data and type(data["project"]) is dict:
            data["project"] = data["project"]["id"]

        ##
        # slice user ADD
        for data_user in data['users']:
            # handle user as dict
            if type(data_user) is dict:
                data_user = data_user['id']
            # new user
            if data_user not in slice['users']:
                # dispatch event add user to slices
                try:
                    event = Event({
                        'action': EventAction.ADD,
                        'user': self.current_user['id'],
                        'object': {
                            'type': ObjectType.SLICE,
                            'id': id,
                        },
                        'data': {
                            'type': DataType.USER,
                            'values': data_user
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
                    response.append(result['generated_keys'])
        # slice remove users
        for data_user in slice['users']:
            # handle user as dict
            if type(data_user) is dict:
                data_user = data_user['id']
            if data_user not in data['users']:
                # dispatch event remove user from slice
                try:
                    event = Event({
                        'action': EventAction.REMOVE,
                        'user': self.current_user['id'],
                        'object': {
                            'type': ObjectType.SLICE,
                            'id': id,
                        },
                        'data': {
                            'type': DataType.USER,
                            'values': data_user
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
                    response.append(result['generated_keys'])
        # slices add/remove resources

        for data_resources in data['resources']:
            # new resource
            if data_resources not in slice['resources']:
                # dispatch event add resource to slices
                try:
                    event = Event({
                        'action': EventAction.ADD,
                        'user': self.current_user['id'],
                        'object': {
                            'type': ObjectType.RESOURCE,
                            'id': id,
                        },
                        'data': {
                            'type': DataType.RESOURCE,
                            'values': data_resources
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
                    response.append(result['generated_keys'])
                    ##
                    # slice remove resource
        for data_resources in slice['resources']:
            if data_resources not in data['resources']:
                # dispatch event remove resource from slice
                try:
                    event = Event({
                        'action': EventAction.REMOVE,
                        'user': self.current_user['id'],
                        'object': {
                            'type': ObjectType.RESOURCE,
                            'id': id,
                        },
                        'data': {
                            'type': DataType.RESOURCE,
                            'values': data_resources
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
                    response.append(result['generated_keys'])

        self.write(json.dumps(
            {
                "result": "success",
                "error": None,
                "debug": None,
                "events": response
            }, cls=myJSONEncoder))
        # return the id of the events
    @gen.coroutine
    def delete(self, id, o=None):
        """
        DELETE /slices/<id>
        :return:
        """
        try:
            # Check if the user has the right to delete a slice
            s = yield r.table('slices').get(id).run(self.dbconnection)
            u = yield r.table('users').get(self.current_user['id']).run(self.dbconnection)
            if not self.current_user['id'] in s['users'] and s['authority'] not in u['pi_authorities']:
                self.userError("your user has no rights on slice: %s" % id)
                return
        except Exception:
            self.userError("not authenticated or project not specified")
            return

        try:
            event = Event({
                'action': EventAction.DELETE,
                'user': self.current_user['id'],
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
                    "error": None,
                    "debug": None,
                    "events": result['generated_keys']
                }, cls=myJSONEncoder))
