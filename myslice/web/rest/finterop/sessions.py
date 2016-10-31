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

        #if id not in current_user['slices']:
        #    self.userError('permission denied')
        #    return

        if id and p == 'start':
            # send a call to the F-Interop Orchestrator
            # start the session
            fi = FakeInterop(id)
            msg = 'Periodic message from FakeInterop'

            print(self.threads)
            if not id in self.threads:
                self.threads[id] = []

            for y in range(1):
                #ts = threading.Thread(target=fi.fake, args=(msg,))
                ts = Process(target=fi.fake, args=(msg,))
                #ts.daemon = True
                self.threads[id].append(ts)
                ts.start()

            # listen to the session
            print('Listen to the session %s' % id)
            for y in range(1):
                #t = threading.Thread(target=startSession, args=(id,))
                t = Process(target=startSession, args=(id,))
                #t.daemon = True
                self.threads[id].append(t)
                t.start()

        elif id and p == 'stop':
            # stop process
            # send a call to the F-Interop Orchestrator
            print(self.threads)
            if id in self.threads:
                for t in self.threads[id]:
                    t.terminate()
                del self.threads[id]
                print('Stop listening to the session')
                stopSession(id)
            else:
                print('this session is not running')
