import json

import rethinkdb as r

from myslice.db import dispatch
from myslice.db.activity import Event
from myslice.db.user import User
from myslice.lib.util import myJSONEncoder
from myslice.web.rest import Api
from tornado import gen, escape

class RequestsHandler(Api):

    @gen.coroutine
    def get(self, id=None):
        """
        GET /requests/[<id>]

        Request list or request with <id>

        :return:
        """

        requests = []

        #self.filter = {'status': ['pending']}
        #self.filter = {}


        # TODO: id must be a valid UUID
        if id:
            result = yield r.table('activity').get(id).run(self.dbconnection)
            requests.append(result)
            # return status code
            if not requests:
                self.NotFoundError('No such activity is found')
        else:

            # filter based on Requests
            filter = json.loads(self.get_argument("filter", default={}, strip=False))

            # status are uppercase
            filter['status'] = ["PENDING"]
            filter['action'] = list(action.upper() for action in filter['action'])
            filter['object'] = list(object.upper() for object in filter['object'])

            # user's requests
            current_user_id = self.get_current_user()['id']

            pi_auth = self.get_current_user()['pi_authorities']

            
            for auth in pi_auth:
                m = self.auth_pattern.match(auth)
                hrn_length = len(m.group('hrn').split(':'))
                
                if hrn_length == 1:
                    pi_auth = []
                    
                    cursor = yield r.table('authorities') \
                            .pluck('id') \
                            .run(self.dbconnection)
                    
                    while (yield cursor.fetch_next()):
                        authority = yield cursor.next()
                        pi_auth.append(authority['id'])

                    break

            # filter based on who is in charge of the auth
            # merge is for actions in the front-end
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
                                                        ).merge(
                {"executable": True}
                                                        ).run(self.dbconnection)
                                                        
            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                requests.append(item)

            # show the requests of user did in pending(not usual case)
            # this is based on the fact that 1. if event is in pending, and  2. user triggers the event
            #  Then user must not have prilevge over this. Check myslice/db/user

            cursor = yield r.table('activity').filter(lambda activity:
                
                (activity['user'] == current_user_id)).filter(lambda activity:

                (len(filter['status']) == 0 or r.expr(filter['status']).contains(activity['status']))
                                                        ).merge(
                {"executable": False}
                                                        ).run(self.dbconnection)
            
            while (yield cursor.fetch_next()):
                item = yield cursor.next()
                requests.append(item)

        self.finish(json.dumps({"result": requests}, cls=myJSONEncoder))

    @gen.coroutine
    def put(self, id):
        """
        PUT /requests/<id>
        { action: <approve|deny|message>, message: <string> }
        :return:
        """

        if id is None:
            self.userError("wrong ID missing")

        try:
            action = escape.json_decode(self.request.body)['action']
        except json.decoder.JSONDecodeError as e:
            self.userError("malformed request", e.message)
            return

        try:
            if 'message' in escape.json_decode(self.request.body):
                message = escape.json_decode(self.request.body)['message']
            else:
                message = None
        except json.decoder.JSONDecodeError as e:
            self.userError("malformed request", e.message)
            return

        if action != 'approve' and action != 'deny':
            self.userError("action must be approve or deny")
            return

        # retrieve the event from db, and see if it is in pending status
        ev = yield r.table('activity').get(id).run(self.dbconnection)
        if not ev:
            self.userError("request not found {}".format(id))
            return

        event = Event(ev)
        if not event.isPending():
            self.serverError("malformed request")
            return

        user = User(self.get_current_user())
        
        if not user.has_privilege(event):
            self.userError("Permission denied")
            return

        if action == 'approve':
            event.setApproved()

        if action == 'deny':
            event.setDenied()

        event.notify = True

        if message:
            event.message(self.get_current_user()['id'], message)

        yield dispatch(self.dbconnection, event)


        requests = []

        cursor = yield r.table('activity').filter(lambda activity:
                r.expr(['PENDING']).contains(activity['status'])
                                                        ).run(self.dbconnection)

        while (yield cursor.fetch_next()):
                item = yield cursor.next()
                requests.append(item)
        

        self.finish(json.dumps({"result": requests}, cls=myJSONEncoder))


