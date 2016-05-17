##
#   MySlice version 2
#
#   Requests thread workers
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

import logging

from pprint import pprint

from myslice import db
from myslice import settings as s
from myslice.db import connect, dispatch
from myslice.db.activity import Event, RequestUser, RequestAuth, ObjectType
from myslice.db.authority import Authority
from myslice.db.user import User

from myslice.email.message import Message, Mailer, build_subject_and_template
from myslice.lib.sfa import get_authority



logger = logging.getLogger('myslice.service.emails')

def request_run(qRequests):
    """
    Process Requests and send Emails accordingly
    """

    logger.info("Worker Requests starting") 

    # db connection is shared between threads
    dbconnection = connect()

    while True:
        try:
            event = Event(qRequests.get())
        except Exception as e:
            logger.error("Problem with event: {}".format(e))
        else:
            try:
                if not event.creatingObject():
                    raise Exception('only creation is allowed with non pi-user')

                pis_email = []
                # Find the authoirty of the event object
                # Then according the authority, put the pi_emails in pis_email
                auth_id, entity = get_authority(event.object.id, event.object.type)
                authority = Authority(db.get(dbconnection, table=entity, id=auth_id))
                for pi_user in authority.pi_users:
                    pis = User(db.get(dbconnection, table='users', id=pi_user))
                    if pis.id != "urn:publicid:IDN+onelab:upmc+user+loic_baron":
                        pis_email.append(pis.email)
                
                if not pis_email:
                    raise Exception('Emails cannot be sent because no one is the PI of {}'.format(event.object.id))

                subject, template = build_subject_and_template('request', event.object.type)
                rich = template.generate(
                                title = subject,
                                entity = str(event.object.type),
                                theme = s.email.theme,
                                first_name = 'Admin',
                                last_name = '',
                                url = "http://theseus.noc.onelab.eu:80/api/v1/activity/{}".format(event.id),
                                )
                
                m = Message(mail_from=('OneLab Support', 'zhouquantest16@gmail.com'),
                            mail_to = pis_email,
                            subject = subject,
                            rich = rich
                            )
                Mailer().send(m)

            except Exception as e:
                import traceback
                traceback.print_exc()
                event.setError()
                event.logError(str(e))
                logger.error("There is something wrong with email system {}".format(e))
                # dispatch the error event
                dispatch(dbconnection, event)

def approve_run(qApproved):
    """
    Process Requests and send Emails accordingly
    """

    # db connection is shared between threads
    dbconnection = connect()

    while True:
        try:
            event = Event(qApproved.get())
        except Exception as e:
            logger.error("Problem with event: {}".format(e))
        else:
            try:
                # USER REQEUST in body
                if event.object.type == ObjectType.USER:
                    request_user = RequestUser(event.data)
                
                # AUTH REQEUST in body
                elif event.object.type == ObjectType.AUTHORITY:
                    request_user = RequestAuth(event.data).pi

                # SLICE/ PROJECT REQUEST
                else:
                    request_user = User(db.get(dbconnection, table='users', id=event.user))
                
                subject, template = build_subject_and_template('approve', event.object.type)
                rich = template.generate(
                                title = subject,
                                entity = str(event.object.type),
                                theme = s.email.theme,
                                first_name = request_user.first_name,
                                last_name = request_user.last_name,
                                )
                
                m = Message(mail_from=('OneLab Support', 'zhouquantest16@gmail.com'),
                            mail_to = request_user.email,
                            subject = subject,
                            rich = rich
                            )
                
                Mailer().send(m)

            except Exception as e:
                import traceback
                traceback.print_exc()

                event.setError()
                event.logError(str(e))
                logger.error("There is something wrong with email system {}".format(e))


def deny_run(qDenied):
    """
    Process Requests and send Emails accordingly
    """

    # db connection is shared between threads
    dbconnection = connect()

    while True:
        try:
            event = Event(qDenied.get())
        except Exception as e:
            logger.error("Problem with event: {}".format(e))
        else:
            try:
                # USER REQEUST
                if event.object.type == ObjectType.USER:
                    request_user = RequestUser(event.data)
                
                # AUTH REQEUST
                elif event.object.type == ObjectType.AUTH:
                    request_user = RequestAuth(event.data).pi

                # SLICE/ PROJECT REQUEST
                else:
                    request_user = User(db.get(dbconnection, table='users', id=event.user))

                subject, template = build_subject_and_template('deny', event.object.type)
                rich = template.generate(
                                title = subject,
                                entity = str(event.object.type),
                                theme = s.email.theme,
                                first_name = request_user.first_name,
                                last_name = request_user.last_name,
                                )
                
                m = Message(mail_from=('OneLab Support', 'zhouquantest16@gmail.com'),
                            mail_to = request_user.email,
                            subject = subject,
                            rich = rich
                            )
                
                Mailer().send(m)

            except Exception as e:
                import traceback
                traceback.print_exc()
                event.setError()
                event.logError(str(e))
                logger.error("There is something wrong with email system {}".format(e))
