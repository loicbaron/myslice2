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
from myslice.db import connect, users
from myslice.db.activity import Event 
from myslice.db.authority import Authority
from myslice.db.user import User
from myslice.db.message import PortalMessage
from myslice.db.message import Mailer

logger = logging.getLogger('myslice.service.requests')

def get_authority_id(usr_id):
    if usr_id.startswith('urn:publicid:IDN+'):
        authority = usr_id.split('+')[1]
        return "urn:publicid:IDN+{}+authority+sa".format(authority)

    raise TypeError("Object id is not a valid id")

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
                if event.user is None:
                    auth_id = get_authority_id(event.object.id)
                    authority = Authority(db.get(dbconnection, table='authorities', id=auth_id))
                    for pi_user in authority.pi_users:
                        user = User(db.get(dbconnection, table='users', id=pi_user))
                        pis_email.append(user.email)

                    m = PortalMessage(author=('OneLab Support', 'zhouquantest16@gmail.com'),
                                    to = pis_email,
                                    entity = event.object.type.lower(),
                                    action = 'request',
                                    loader_path = s.email.dirpath,
                                    theme = s.email.theme,
                                    )
                    m.generate_message(
                                url = "http://oneLab.eu",
                                first_name = event.data['first_name'],
                                last_name = event.data['last_name'],
                                email = event.data['email']
                                )
                    mailer = Mailer().send(m)

            except Exception as e:
                event.setError()
                logger.error("Unable to fetch the user from db {}".format(e))
