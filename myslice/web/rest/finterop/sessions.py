import json
import logging
import threading
from multiprocessing import Process

import rethinkdb as r

from myslice.lib.util import myJSONEncoder
from myslice.web.rest import Api

from myslice.db.activity import Event, EventAction, ObjectType, DataType
from myslice.db import dispatch

from myslice.services.finterop.sessions import start as startSession, stop as stopSession

from myslice.bin.fakeinterop import FakeInterop

from tornado import gen, escape

logger = logging.getLogger('myslice.rest.finterop.sessions')

class SessionsHandler(Api):

    @gen.coroutine
    def get(self, id=None, p=None):
        """
            - GET /finterop/sessions/<id|hrn>/(start|stop)

            :return:
            """

        response = []
        current_user = self.get_current_user()
        logger.info('get session')
        print('get session %s' % id)

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
                self.threads[id] = []
                # TODO: F-Interop Orchestrator Integration
                # send a call to the F-Interop Orchestrator

                # XXX Meanwhile start the FakeInterop session
                fi = FakeInterop(id)
                msg = 'Periodic message from FakeInterop'
                for y in range(1):
                    ts = Process(target=fi.fake, args=(msg,))
                    self.threads[id].append(ts)
                    ts.start()

                # listen to the session
                print('Listen to the session %s' % id)
                for y in range(1):
                    t = Process(target=startSession, args=(id,))
                    self.threads[id].append(t)
                    t.start()

        elif id and p == 'stop':
            # TODO: Check the status of the session in DB
            print(self.threads)
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
