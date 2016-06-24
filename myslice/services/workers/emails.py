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

            # Recipients
            # TODO: Send specific emails
            # Status did NOT changed
            # Comments about an event with a message
            if event.status == event.previous_status:
                print("TODO: send specific emails with messages")
            recipients = set()

            url = s.web.url
            if s.web.port and s.web.port != 80:
                url = url +':'+ s.web.port

            if event.object.type == ObjectType.PASSWORD:
                recipients.add(User(db.get(dbconnection, table='users', id=event.object.id)))
                url = url+'/password/'+event.data['hashing']
                subject, template = build_subject_and_template('password', event.object.type)
            else:
                if event.isPending():

                    # Find the authoirty of the event object
                    # Then according the authority, put the pi_emails in pis_email
                    try:
                        authority_id = event.data['authority']
                    except KeyError:
                        msg = 'Authority id not specified ({})'.format(event.id)
                        logger.error(msg)
                        event.logDebug(msg)
                        event.logWarning('Authority not specified, email not sent')
                        event.notify = False
                        dispatch(dbconnection, event)
                        continue

                    authority = Authority(db.get(dbconnection, table='authorities', id=authority_id))
                    for pi_id in authority.pi_users:
                        pi = User(db.get(dbconnection, table='users', id=pi_id))
                        recipients.add(pi)

                    if not recipients:
                        msg = 'Emails cannot be sent because no one is the PI of {}'.format(event.object.id)
                        logger.error(msg)
                        event.logDebug(msg)
                        event.logWarning('No recipients could be found, email not sent')
                        event.notify = False
                        dispatch(dbconnection, event)
                        continue
                else:
                    # USER REQUEST in body
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
                try:
                    username = "{} {}".format(r.first_name, r.last_name)
                except:
                    r.first_name = ''
                    r.last_name = ''
                    username = "{} {}".format(r.first_name, r.last_name)

                mail_to.append("{} <{}>".format(username, r.email))

            mail_body = template.generate(
                            title = subject,
                            entity = str(event.object.type),
                            theme = s.email.theme,
                            recipients = recipients,
                            url = url,
                            )

            m = Message(mail_from=('OneLab Support', 'zhouquantest16@gmail.com'),
                        mail_to = mail_to,
                        subject = subject,
                        rich = mail_body
                        )
            try:
                Mailer().send(m)
                
                # TODO: better handle email cases

                #event.logInfo("The PIs of {} have been contacted".format(authority.name))
                #logger.info("The PIs of {} have been contacted".format(authority.name))
            except Exception as e:
                msg = '{} {}'.format(e, event.object.id)
                logger.error(msg)
                event.logDebug(msg)
                event.logWarning('could not send email to PI users')
            finally:
                event.notify = False
                dispatch(dbconnection, event)

