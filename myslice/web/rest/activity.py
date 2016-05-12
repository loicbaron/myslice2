import json

import rethinkdb as r
from tornado import gen, escape

from pprint import pprint

from myslice.web.rest import Api
from myslice.lib.util import myJSONEncoder
from myslice.db import dispatch, changes
from myslice.db.activity import Event, EventStatus, PiAction, Action

'''
    API practice follows 
    https://github.com/WhiteHouse/api-standards#responses
'''


class ActivityHandler(Api):


    @gen.coroutine
    def get(self, id=None):
        activity = []

        if id:
            result = yield r.table('activity').get(id).run(self.dbconnection)
            activity.append(result)
        else:
            cursor = yield r.table('activity').run(self.dbconnection)

            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                activity.append(item)

        # return status code
        if not activity:
            self.NotFoundError('No such activity is found')
        else:
            self.finish(json.dumps({"activity": activity}, cls=myJSONEncoder))

    @gen.coroutine
    def post(self):
        """
        ONLY FOR DEBUG
        """

        # TODO: get user id from user logged in

        # NOTE: checks are done by the service, here we only dispatch the event

        #print(escape.json_decode(self.request.body))
        try:
            data = escape.json_decode(self.request.body)['event']
        except json.decoder.JSONDecodeError as e:
            pprint(self.request.body)
            import traceback
            traceback.print_exc()
            self.set_status(400)
            self.finish(json.dumps({"return": {"status": "error", "messages": "malformed request"}}))
            
        try:
            event = Event(data)
        except Exception as e:
            pprint(self.request.body)
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
                    #print(item)
                    ev = Event(item['new_val'])
                    if ev.id == event_id:
                        if ev.status == EventStatus.ERROR or ev.status == EventStatus.WARNING:
                            self.set_status(500)
                            print(ev)
                            # XXX trying to cleanup the Cursor, but it is not Working
                            # <class 'rethinkdb.net_tornado.TornadoCursor'>
                            # https://github.com/rethinkdb/rethinkdb/blob/next/drivers/python/rethinkdb/tornado_net/net_tornado.py
                            # https://github.com/rethinkdb/rethinkdb/blob/next/drivers/python/rethinkdb/net.py
                            #yield feed.close()
                            self.finish(json.dumps({"return": {"status":ev.status,"messages":ev}}, cls=myJSONEncoder))
                        if ev.status == EventStatus.SUCCESS or ev.status == EventStatus.PENDING or ev.status == EventStatus.DENIED:
                            self.set_status(200)
                            #yield feed.close()
                            self.finish(json.dumps({"return": {"status":ev.status,"messages":ev}}, cls=myJSONEncoder))

            except Exception as e:
                pprint(self.request.body)
                import traceback
                traceback.print_exc()
                self.set_status(500)
                #yield feed.close()
                pprint(e)
                self.finish(json.dumps({"return": {"status":EventStatus.ERROR,"messages":e}}, cls=myJSONEncoder))

    @gen.coroutine
    def put(self, id=None):
        '''
        This method is only used for internal use
        
        {
            action: APPROVE/ DENY
        }

        '''
        if id is None:
            self.BadRequest('Bad Request')

        # retrieve the event from db, and see if it is in pending status
        ev = yield r.table('activity').get(id).run(self.dbconnection)
        if not ev:
            self.NotFoundError("activity not found {}".format(id))

        event = Event(ev)
        if not event.isPending():
            self.BadRequest("malformed request")

        # 
        try:
            data = escape.json_decode(self.request.body)
            action = PiAction(data)
            if action == Action.APPROVE:
                event.setApproved()
            if action == Action.DENY:
                event.setDenied()
        except Exception as e:
            self.BadRequest(str(e))

        yield dispatch(self.dbconnection, event)












