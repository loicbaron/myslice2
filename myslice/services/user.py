import logging
import myslice.db as db
from myslice.lib import Status
from myslice.lib.util import format_date

from myslicelib.model.user import User
from myslicelib.query import q

logger = logging.getLogger('myslice.service.users')

def run():
    """
    A thread that will check resource availability and information
    """
    logger.info("Process users starting")

    """
    DB connection
    """
    dbconnection = db.connect()

    """
    MySliceLib Query Slices
    """
    users = q(User).get()

    """
    update local slice table
    """
    lusers = db.users(dbconnection, users.dict())

    for ls in lusers :
        if not users.has(ls['id']) and ls['status'] is not Status.PENDING:
            # delete resourc that have been deleted elsewhere
            db.delete(dbconnection, 'users', ls['id'])
            logger.info("User {} deleted".format(ls['id']))

        # add status if not present and update on db
        if not 'status' in ls:
            ls['status'] = Status.ENABLED
            ls['enabled'] = format_date()
            db.users(dbconnection, ls)
