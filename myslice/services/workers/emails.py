##
#   MySlice version 2
#
#   Requests thread workers
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

from premailer import transform

from myslice import db
from myslice import settings as s
from myslice.db import connect, dispatch
from myslice.db.activity import Event, ObjectType
from myslice.db.authority import Authority
from myslice.db.user import User

from myslice.email.message import Message, Mailer, build_subject_and_template

import myslice.lib.log as logging

logger = logging.getLogger("emails")

def confirmEmails(qConfirmEmails):
    """
    Process Event and send an Email to the user to confirm his/her email
    """
    # db connection is shared between threads
    dbconnection = connect()

    while True:
        try:
            event = Event(qConfirmEmails.get())
        except Exception as e:
            logger.exception(e)
            logger.error("Problem with event: {}".format(e))
        else:
            try:
                # Recipients
                # Status did NOT changed
                if event.status == event.previous_status:
                    logger.warning("TODO: send specific emails with messages")
                recipients = set()

                url = s.web['url']
                if s.web['port'] and s.web['port'] != 80:
                    url = url +':'+ s.web['port']

                # Look for the user email in the Event
                if event.object.type == ObjectType.USER:
                    recipients.add(User({'email':event.data['email'], 'first_name':event.data['first_name'], 'last_name':event.data['last_name']}))
                elif event.object.type == ObjectType.AUTHORITY:
                    for user in event.data['users']:
                        if isinstance(user, dict):
                            recipients.add(User({'email':user['email'], 'first_name':user['first_name'], 'last_name':user['last_name']}))
                else:
                    for user in event.data['pi_users']:
                        if isinstance(user, dict):
                            recipients.add(User({'email':user['email'], 'first_name':user['first_name'], 'last_name':user['last_name']}))
                url = url+'/confirm/'+event.id
                subject, template = build_subject_and_template('confirm', event)
                buttonLabel = "Confirm Email"

                sendEmail(event, recipients, subject, template, url, buttonLabel)
            except Exception as e:
                import traceback
                traceback.print_exc()
                msg = "Error in event {} while trying to send a confirmation email: {}".format(event.id, e)
                logger.error(msg)
                event.logWarning(msg)
                dispatch(dbconnection, event)


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
                logger.warning("TODO: send specific emails with messages")
            recipients = set()

            url = s.web.url
            if s.web.port and s.web.port != 80:
                url = url +':'+ s.web.port
            
            buttonLabel = "View details"
            if event.object.type == ObjectType.PASSWORD:
                recipients.add(User(db.get(dbconnection, table='users', id=event.object.id)))
                url = url+'/password/'+event.data['hashing']
                subject, template = build_subject_and_template('password', event)
                buttonLabel = "Change password"
            else:
                if event.isPending():

                    # Find the authority of the event object
                    # Then according the authority, put the pi_emails in pis_email
                    try:
                        authority_id = event.data['authority']
                    except KeyError:
                        msg = 'Authority id not specified ({})'.format(event.id)
                        logger.error(msg)
                        event.logWarning('Authority not specified in event {}, email not sent'.format(event.id))
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
                        event.logWarning('No recipients could be found for event {}, email not sent'.format(event.id))
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
                    subject, template = build_subject_and_template('request', event)
                    buttonLabel = "Approve / Deny"
                    url = url+'/activity'

                elif event.isSuccess():
                    subject, template = build_subject_and_template('approve', event)

                elif event.isDenied():
                    subject, template = build_subject_and_template('deny', event)

            sendEmail(event, recipients, subject, template, url, buttonLabel)

def sendEmail(event, recipients, subject, template, url, buttonLabel):
    # db connection is shared between threads
    dbconnection = connect()
    mail_to = []
    for r in recipients:
        try:
            if hasattr(r, 'first_name') and hasattr(r, 'last_name'):
                username = "{} {}".format(r.first_name, r.last_name)
            else:
                username = r.email
                r.setAttribute('first_name','')
                r.setAttribute('last_name','')
        except:
            import traceback
            traceback.print_exc()
            username = ""

        mail_to.append("{} <{}>".format(username, r.email))

    mail_body = template.generate(
                    title = subject,
                    entity = str(event.object.type),
                    event = event,
                    theme = s.email['theme'],
                    recipients = recipients,
                    url = url,
                    buttonLabel = buttonLabel,
                    )
    # use premailer module to get CSS inline
    mail_body_inline = transform(mail_body.decode())

    m = Message(mail_from=['OneLab Support', s.email['sender']],
                mail_to = mail_to,
                subject = subject,
                html_content = mail_body_inline
                )
    try:
        Mailer().send(m)
        # TODO: better handle email cases

        #event.logInfo("The PIs of {} have been contacted".format(authority.name))
        #logger.info("The PIs of {} have been contacted".format(authority.name))
    except Exception as e:
        msg = '{} {}'.format(e, event.object.id)
        logger.error(msg)
        event.logWarning('Could not send email to PI users in event {}'.format(event.id))
    finally:
        event.notify = False
        dispatch(dbconnection, event)
