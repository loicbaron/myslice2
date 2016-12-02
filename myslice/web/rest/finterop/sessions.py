import json
import logging
import threading
from pprint import pprint
from multiprocessing import Process

import rethinkdb as r
from rethinkdb.errors import ReqlNonExistenceError
import myslice.db as db
from myslice import settings as s

from myslice.lib.util import myJSONEncoder, format_date
from myslice.web.rest import Api

from myslice.db.activity import Event, EventAction, ObjectType, DataType
from myslice.db import dispatch

from myslice.services.finterop.sessions import start as startSession, stop as stopSession

from myslice.services.finterop.fakeinterop import FakeInterop

from tornado import gen, escape

logger = logging.getLogger('myslice.rest.finterop.sessions')

class SessionsHandler(Api):

    # DB connection
    dbconnection = db.connect()

    @gen.coroutine
    def getSession(self, slice_id):
        try:
            data = yield r.db(s.db.name).table('sessions')\
            .filter({'slice_id':slice_id,'status':'started'})\
            .max('start_date').run(self.dbconnection)
        except ReqlNonExistenceError:
            return None
        return data

    @gen.coroutine
    def startFakeInterop(self, session_id, slice_id):
        fi = FakeInterop(session_id)
        msg = 'Periodic message from FakeInterop'
        for y in range(1):
            ts = Process(target=fi.fake, args=(msg,))
            self.threads[slice_id].append(ts)
            ts.start()

    @gen.coroutine
    def listenSession(self, session_id, slice_id):
        for y in range(1):
            t = Process(target=startSession, args=(session_id,))
            self.threads[slice_id].append(t)
            t.start()


    @gen.coroutine
    def get(self, id=None, p=None):
        """
            - GET /finterop/sessions/<id|hrn>/(start|stop)

            :return:
            """

        response = []
        current_user = self.get_current_user()
        logger.info('get session')

        if not current_user:
            self.userError('not authenticated ')
            return

        # Security: only allow to watch sessions for which the user has rights (one of his slices)
        # --------------------------------------
        # XXX DISABLED for development
        # --------------------------------------
        #if id not in current_user['slices']:
        #    self.userError('permission denied')
        #    return

        if id and p == 'start':
            # TODO: Check the status of the session in DB
            print(self.threads)
            if id in self.threads:
                print('this session has alredy started')
                self.userError('this session has already started')
                return
            else:
                data = {'slice_id':id, 'status':'started', 'start_date':format_date()}
                # Create a session in DB
                session = yield r.db(s.db.name).table('sessions').insert(data, conflict='update').run(self.dbconnection)
                session_id = session['generated_keys'][0]
                # Add the session to the threads
                self.threads[id] = []

                # TODO: F-Interop Orchestrator Integration
                # send a call to the F-Interop Orchestrator

                # XXX Meanwhile start the FakeInterop session
                yield self.startFakeInterop(session_id, id)

                # listen to the session
                print('Listen to the session %s' % session_id)
                yield self.listenSession(session_id, id)

        elif id and p == 'stop':
            # TODO: Check the status of the session in DB
            print(self.threads)
            # Get session in DB
            data = yield self.getSession(id)
            print("DATA")
            pprint(data)
            if data:
                data['status']='stopped'
                data['end_date']=format_date()
                # Update session in DB
                r.db(s.db.name).table('sessions').get(data['id']).update(data).run(self.dbconnection)

            if id in self.threads:

                # TODO: send a call to the F-Interop Orchestrator

                # XXX Meanwhile stop FakeInterop process

                # Stop Listening process
                for t in self.threads[id]:
                    t.terminate()
                del self.threads[id]
                print('Stop listening to the session')
                stopSession(id)

            else:
                print('this session is not running')
                self.userError('this session is not running')
                return
        else:
            self.userError('not supported by the REST API')
            return

        # TODO: send back the result success with data about the session
        self.write(json.dumps(
        {
            "result": "success",
            "data": [],
            "error": None,
            "debug": None
        }, cls=myJSONEncoder))
