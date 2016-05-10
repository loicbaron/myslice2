##
#   MySlice version 2
#
#   Requests thread workers
#
#   (c) 2016 Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
##

import logging

from myslice import db
from myslice import settings as s
from myslice.db import connect, dispatch
from myslice.db.activity import Event, ObjectType 
from myslice.db.authority import Authority
from myslice.db.user import User
from myslice.email.message import Message, Mailer, build_subject_and_template

logger = logging.getLogger('myslice.service.requests')

def get_authority_id(event_id, object_type):
    '''
    Get the corresponding upper admin entity and its entity type
    '''
    if not event_id.startswith('urn:publicid:IDN+'):
        raise TypeError("Object id is not a valid id")

    if object_type == ObjectType.USER:
        authority = event_id.split('+')[1]
        return "urn:publicid:IDN+{}+authority+sa".format(authority), "authorities"

    if object_type == ObjectType.SLICE:
        project = event_id.split('+')[1]
        return "urn:publicid:IDN+{}+authority+sa".format(project), "projects"

    if object_type in [ObjectType.PROJECT, ObjectType.AUTHORITY]:
        # get onelab:upmc:project
        authority = event_id.split('+')[1]
        upper_authority = ":".join(authority.split(':')[:-1])
        return "urn:publicid:IDN+{}+authority+sa".format(upper_authority), "authorities"
   
def run(qRequests):
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
                pis_email = []
                # Find the authoirty of the event object
                # Then according the authority, put the pi_emails in pis_email
                auth_id, entity = get_authority_id(event.object.id, event.object.type)
                authority = Authority(db.get(dbconnection, table=entity, id=auth_id))            
                for pi_user in authority.pi_users:
                    pis = User(db.get(dbconnection, table='users', id=pi_user))
                    pis_email.append(pis.email)
                
                subject, template = build_subject_and_template('request', event.object.type)
                rich = template.generate(
                                title = subject,
                                entity = event.object.type,
                                theme = s.email.theme,
                                first_name = 'Quan',
                                last_name = 'Zhou',
                                url = "http://oneLab.eu",
                                items_with_buttons = dict(
                                                            name = 'TEST'
                                                        )
                                )
                
                m = Message(mail_from=('OneLab Support', 'zhouquantest16@gmail.com'),
                            mail_to = pis_email,
                            subject = subject,
                            rich = rich
                            )
                Mailer().send(m)

            except Exception as e:
                import traceback
                print(traceback.print_exc(e))
                event.setError()
                logger.error("There is something wrong with email system {}".format(e))
                # dispatch the error event
                dispatch(dbconnection, event)
