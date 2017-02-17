import json
import logging

import rethinkdb as r
from tornado import gen, escape

from myslice.web.rest import Api
from myslice.lib.util import myJSONEncoder
from myslice.db import dispatch, changes
from myslice.db.activity import Event, EventStatus, EventAction, ObjectType

'''
    API practice follows 
    https://github.com/WhiteHouse/api-standards#responses
'''

logger = logging.getLogger('myslice.rest.activity')

class ActivityHandler(Api):


    @gen.coroutine
    def get(self, id=None):
        """
            GET /activity/[<id>[/(users|slices)]]

            filter: {
                action : [ <create|update|delete|add|remove>, ... ],
                status : [ <new|pending|denied|approved|waiting|running|success|error|warning>, ... ],
                object : [ <authority|user|project|slice|resource>, ... ]
            }

            :return:
        """
        activity = []

        self.filter = {}

        # User has to be authenticated
        current_user = self.get_current_user()
        if not current_user:
            self.userError("not authenticated")
            return

        # TODO: User's right to see an event
        # User that has send the event OR PI of the authority OR Admin


        # TODO: id must be a valid UUID
        if id:
            result = yield r.table('activity').get(id).run(self.dbconnection)
            activity.append(result)
            # return status code
            if not activity:
                self.NotFoundError('No such activity is found')
        else:

            filter = json.loads(self.get_argument("filter", default={}, strip=False))

            # status are uppercase
            filter['status'] = list(status.upper() for status in filter['status'])
            filter['action'] = list(action.upper() for action in filter['action'])
            filter['object'] = list(object.upper() for object in filter['object'])

            # user's activities
            # user's requests
            current_user = self.get_current_user()
            current_user_id = current_user['id']

            if self.isAdmin():
                pi_auth = []
                cursor = yield r.table('authorities').pluck('id').run(self.dbconnection)
                
                while (yield cursor.fetch_next()):
                    authority = yield cursor.next()
                    pi_auth.append(authority['id'])
            else:
                pi_auth = current_user['pi_authorities']


            # get all the activities when user is a PI or admin over
            cursor = yield r.table('activity').filter(lambda activity:

                (len(filter['action']) == 0 or r.expr(filter['action']).contains(activity['action']))
                                                        ).filter(lambda activity:

                (len(filter['status']) == 0 or r.expr(filter['status']).contains(activity['status']))
                                                        ).filter(lambda activity:

                (len(filter['object']) == 0 or r.expr(filter['object']).contains(activity['object']['type']))
                                                        ).filter(lambda activity:
                                                        
                (r.expr(pi_auth).contains(activity['data']['authority']))
                                                        ).filter(lambda activity:
                    
                (activity['user'] != current_user_id)
                )\
                .merge(lambda activity: {
                    'user': r.table('users').get(activity['user']) \
                                                        .default({'id' : activity['user']})
                }) \
                .run(self.dbconnection)
                                                        
            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                activity.append(item)

            # get all the activities that are triggered by user
            cursor = yield r.table('activity').filter(lambda activity:

                (len(filter['action']) == 0 or r.expr(filter['action']).contains(activity['action']))
                                                        ).filter(lambda activity:

                (len(filter['status']) == 0 or r.expr(filter['status']).contains(activity['status']))
                                                        ).filter(lambda activity:

                (len(filter['object']) == 0 or r.expr(filter['object']).contains(activity['object']['type']))

                                                        ).filter(lambda activity:
                (activity['user'] == current_user_id)
                )\
                .merge(lambda activity: {
                    'user': r.table('users').get(activity['user']) \
                                                        .default({'id' : activity['user']})
                }) \
                .run(self.dbconnection)

            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                activity.append(item)

        self.finish(json.dumps({"result": activity}, cls=myJSONEncoder))

            

    @gen.coroutine
    def post(self, id=None):
        """
        ONLY FOR DEBUG
        """

        # TODO: get user id from user logged in

        # NOTE: checks are done by the service, here we only dispatch the event

        try:
            data = escape.json_decode(self.request.body)['event']
        except json.decoder.JSONDecodeError as e:
            logger.error(self.request.body)
            logger.exception("malformed request")
            self.set_status(400)
            self.finish(json.dumps({"return": {"status": "error", "messages": "malformed request"}}))
            
        try:
            event = Event(data)
        except Exception as e:
            logger.exception("error in post activity")
            import traceback
            traceback.print_exc()
            self.set_status(500)
            self.finish(json.dumps({"return": {"status":"error","messages":e.message}}))
        else:
            try:
                # XXX If watching all events, is scalability an issue?
                # changes sends back all the events that occured since it started...
                feed = yield changes(dbconnection = self.dbconnection, table='activity')

                # We need to watch the changes before dispatch, because the service writing into the DB is faster than this process
                result = yield dispatch(self.dbconnection, event)
                event_id = result['generated_keys'][0]
                while (yield feed.fetch_next()):
                    item = yield feed.next()
                    # items are piling up...
                    ev = Event(item['new_val'])
                    if ev.id == event_id:
                        if ev.isError() or ev.isWarning():
                            self.set_status(500)
                            # XXX trying to cleanup the Cursor, but it is not Working
                            # <class 'rethinkdb.net_tornado.TornadoCursor'>
                            # https://github.com/rethinkdb/rethinkdb/blob/next/drivers/python/rethinkdb/tornado_net/net_tornado.py
                            # https://github.com/rethinkdb/rethinkdb/blob/next/drivers/python/rethinkdb/net.py
                            #yield feed.close()
                            self.finish(json.dumps({"return": {"status":ev.status,"messages":ev}}, cls=myJSONEncoder))
                        elif ev.isSuccess() or ev.isPending():
                            self.set_status(200)
                            #yield feed.close()
                            self.finish(json.dumps({"return": {"status":ev.status,"messages":ev}}, cls=myJSONEncoder))

            except Exception as e:
                logger.exception("error in post activity")
                import traceback
                traceback.print_exc()
                self.set_status(500)
                #yield feed.close()
                self.finish(json.dumps({"return": {"status":EventStatus.ERROR,"messages":e}}, cls=myJSONEncoder))

    @gen.coroutine
    def put(self, id):
        '''
        PUT /activity/<id>
        This method allows to update an event status
        for example to re-run after an error

        {
            status: <new_status>
        }

        '''
        # User has to be authenticated
        current_user = self.get_current_user()
        if not current_user:
            self.userError("not authenticated")
            return

        # TODO: User's right to see an event
        # User that has send the event OR PI of the authority OR Admin

        # TODO: id must be a valid UUID
        if not id:
            self.userError("no event id provided")
            return
        try:
            data = escape.json_decode(self.request.body)
        except json.decoder.JSONDecodeError as e:
            logger.error(self.request.body)
            logger.exception("malformed request")
            self.set_status(400)
            self.finish(json.dumps({"return": {"status": "error", "messages": "malformed request"}}))

        if not 'status' in data:
            self.userError("status of event is required")
            return

        try:
            activity = yield r.table('activity').get(id).run(self.dbconnection)
            event = Event(activity)
            event.previous_status = event.status
            event.status = data['status']
            result = yield dispatch(self.dbconnection, event)
            self.set_status(200)
            self.finish(json.dumps({"result": result}, cls=myJSONEncoder))
        except Exception as e:
            logger.exception("error in PUT activity")
            self.set_status(500)
            self.finish(json.dumps({"return": {"status":"error","messages":e.message}}))
            return

