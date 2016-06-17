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
from myslice.db.activity import Event, ObjectType
from myslice.db.authority import Authority
from myslice.db.user import User

from myslice.email.message import Message, Mailer, build_subject_and_template



logger = logging.getLogger('myslice.service.emails')

def emails_run(qEmails):
    """
    Process Requests and send Emails accordingly
    """

    # db connection is shared between threads
    dbconnection = connect()

    while True:
        try:
            event = Event(qEmails.get())
        except Exception as e:
            logger.error("Problem with event: {}".format(e))
        else:
            try:

                # Recipients
                # TODO: Send specific emails
                # Status did NOT changed
                # Comments about an event with a message
                if event.status == event.previous_status:
                    print("TODO: send specific emails with messages")
                recipients = set()

                if event.isPending():

                    # Find the authoirty of the event object
                    # Then according the authority, put the pi_emails in pis_email
                    authority = Authority(db.get(dbconnection, table='authorities', id=event.data['authority']))
                    for pi_user in authority.pi_users:
                        pis = User(db.get(dbconnection, table='users', id=pi_user))
                        recipients.add(pis)

                    if not recipients:
                        raise Exception('Emails cannot be sent because no one is the PI of {}'.format(event.object.id))
                else:
                    # USER REQEUST in body
                    if event.object.type == ObjectType.USER:
                        recipients.add(User(event.data))

                    # SLICE/ PROJECT REQUEST
                    else:
                        recipients.add(User(db.get(dbconnection, table='users', id=event.user)))


                if event.isPending():
                    subject, template = build_subject_and_template('request', event.object.type)

                elif event.isDenied():
                    subject, template = build_subject_and_template('approve', event.object.type)

                elif event.isApproved():
                    subject, template = build_subject_and_template('deny', event.object.type)

                mail_to = []
                for r in recipients:
                    mail_to.append("{} {} <{}>".format(r.first_name, r.last_name, r.email))

                mail_body = template.generate(
                                title = subject,
                                entity = str(event.object.type),
                                theme = s.email.theme,
                                recipients = recipients,
                                url = ''
                                )
                
                m = Message(mail_from=('OneLab Support', 'zhouquantest16@gmail.com'),
                            mail_to = mail_to,
                            subject = subject,
                            rich = mail_body
                            )
                
                Mailer().send(m)

            except Exception as e:
                import traceback
                traceback.print_exc()
                event.logError(str(e))
                dispatch(dbconnection,event)
                logger.error("There is something wrong with email system {}".format(e))
