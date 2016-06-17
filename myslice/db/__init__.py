import logging
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from myslice import settings as s
from myslice.db.activity import Event

logger = logging.getLogger(__name__)

tables = [
        {
            'name' : 'testbeds',
            'pkey' : 'id'
        },
        {
            'name' : 'resources',
            'pkey' : 'id'
        },
        {
            'name' : 'leases',
            'pkey' : 'id'
        },

        {
            'name' : 'slices',
            'pkey' : 'id'
        },
        {
            'name' : 'authorities',
            'pkey' : 'id'
        },
        {
            'name' : 'projects',
            'pkey' : 'id'
        },
        {
            'name' : 'users',
            'pkey' : 'id'
        },
        {
            'name' : 'activity',
            'pkey' : 'id'
        }
    ]

def connect():
    logger.info("Connecting to db {} on {}:{}".format(s.db.name,s.db.host,s.db.port))
    try :
        return r.connect(host=s.db.host, port=s.db.port, db=s.db.name)
    except RqlDriverError :
        logger.error("Can't connect to RethinkDB")
        raise SystemExit("Can't connect to RethinkDB")

def setup():
    dbconnection = connect()

    try:
        r.db_create(s.db.name).run(dbconnection)
        logger.info('MyOps2 database created successfully')
    except RqlRuntimeError:
        logger.info('MyOps2 database already exists')

    for t in tables:
        try:
            r.db(s.db.name).table_create(t['name'], primary_key=t['pkey']).run(dbconnection)
            logger.info('table %s setup completed', t['name'])
        except RqlRuntimeError:
            logger.info('table %s already exists', t['name'])

    dbconnection.close()


def testbeds(testbeds=None):

    c = connect()

    if not testbeds:
        # query testbeds
        pass
    else:
        # update testbeds

        r.table('endpoints').insert(
        {
            "id": "ple",
            "name": "PlanetLab Europe",
            "short": "PLE",
        }, conflict='update').run(c)

    c.close()


def get(dbconnection=None, table=None, id=None, filter=None):
    if not table:
        raise NotImplementedError('table must be specified')

    if not dbconnection:
        dbconnection = connect()

    if id:
        return r.db(s.db.name).table(table).get(id).run(dbconnection)

    if filter:
        # return somthing with filter
        return r.db(s.db.name).table(table).filter(filter).run(dbconnection)

    return r.db(s.db.name).table(table).run(dbconnection)


def users(dbconnection=None, data=None, id=None, email=None):
    if not dbconnection:
        dbconnection = connect()

    ##
    # Updating an existing user
    if id and data:
        r.db(s.db.name).table('users').get(id).update(data).run(dbconnection)

    ##
    # Adding a new user
    if data:
        r.db(s.db.name).table('users').insert(data, conflict='update').run(dbconnection)

    ##
    # Return the user
    if id:
        return r.db(s.db.name).table('users').get(id).run(dbconnection)

    ##
    # Search user by email
    if email:
        return r.db(s.db.name).table('users').filter(email).run(dbconnection)

    return r.db(s.db.name).table('users').run(dbconnection)

def authorities(dbconnection=None, data=None, id=None):
    if not dbconnection:
        dbconnection = connect()

    if id and data:
        r.db(s.db.name).table('authorities').get(id).update(data).run(dbconnection)

    if data:
        r.db(s.db.name).table('authorities').insert(data, conflict='update').run(dbconnection)

    return r.db(s.db.name).table('authorities').run(dbconnection)


def projects(dbconnection=None, data=None, id=None):
    if not dbconnection:
        dbconnection = connect()

    if id and data:
        r.db(s.db.name).table('projects').get(id).update(data).run(dbconnection)

    if data:
        r.db(s.db.name).table('projects').insert(data, conflict='update').run(dbconnection)

    return r.db(s.db.name).table('projects').run(dbconnection)


def slices(dbconnection=None, data=None, id=None):
    if not dbconnection:
        dbconnection = connect()

    if id and data:
        r.db(s.db.name).table('slices').get(id).update(data).run(dbconnection)

    if (data):
        r.db(s.db.name).table('slices').insert(data, conflict='update').run(dbconnection)

    return r.db(s.db.name).table('slices').run(dbconnection)

def resources(dbconnection=None, data=None, id=None):
    if not dbconnection:
        dbconnection = connect()

    if id and data:
        r.db(s.db.name).table('resources').get(id).update(data).run(dbconnection)

    if (data):
        r.db(s.db.name).table('resources').insert(data, conflict='update').run(dbconnection)

    return r.db(s.db.name).table('resources').run(dbconnection)

def leases(dbconnection=None, data=None):
    if not dbconnection:
        dbconnection = connect()

    if id and data:
        r.db(s.db.name).table('leases').get(id).update(data).run(dbconnection)

    if (data):
        r.db(s.db.name).table('leases').insert(data, conflict='update').run(dbconnection)

    return r.db(s.db.name).table('leases').run(dbconnection)

def events(dbconnection=None, event=None, user=None, status=None, action=None, obj_type=None):
    if not dbconnection:
        dbconnection = connect()

    if isinstance(event, Event):
        # update event on db
        ret = r.db(s.db.name).table('activity').insert(event.dict(), conflict='update').run(dbconnection)
    
    req = r.db(s.db.name).table('activity')

    if user:
        req = req.filter({'user':user})

    if status:
        if isinstance(status, str) or len(status) == 1:
            req = req.filter({'status': status})
        elif isinstance(status, list) and len(status) == 2:
            req = req.filter(lambda event: (event['status'] == status[0]) | (event['status'] == status[1]))
        else:
            raise Exception('status filter fields too much')

    if action:
        req = req.filter({'action':action})

    if obj_type:
        req = req.filter(lambda event: event['object']['type'] == obj_type)

    return req.run(dbconnection)

# retrieves an event
def event(dbconnection=None, id=None):
    if not id:
        return False

    if not dbconnection:
        dbconnection = connect()

    return r.db(s.db.table).table('activity').get(id).run(dbconnection)

def dispatch(dbconnection=None, activity=None):
    """
    Dispatches an Activity (Event or Request object)
    """
    table = 'activity'

    if not isinstance(activity, Event):
        raise Exception("Only Events can be dispatched")

    # connect to db if connection is not specified
    if not dbconnection:
        dbconnection = connect()

    if activity.id:
        ##
        # updating existing event/request
        ret = r.db(s.db.name).table(table).get(activity.id).update(activity.dict()).run(dbconnection)
    else:
        ##
        # dispatching new event/request
        ret = r.db(s.db.name).table(table).insert(activity.dict()).run(dbconnection)

    return ret

    # return event


def delete(dbconnection=None, table=None, id=None):
    if not dbconnection:
        dbconnection = connect()

    if id and table:
        return r.db(s.db.name).table(table).get(id).delete().run(dbconnection)

    return False

def changes(dbconnection=None, table=None, status=None, action=None, obj_type=None, id=None):
    if not table:
        return False

    if not dbconnection:
        dbconnection = connect()

    req = r.db(s.db.name).table(table).changes()

    if status:
        if isinstance(status, str) or len(status) == 1:
            req = req.filter(lambda change: change['new_val']['status'] == status)
        elif isinstance(status, list) and len(status) == 2:
            req = req.filter(lambda event: (event['new_val']['status'] == status[0]) | (event['new_val']['status'] == status[1]))
        else:
            raise Exception('status filter fields too much')

    if action:
        req = req.filter(lambda change: change['new_val']['action'] == action)

    if id:
        req = req.filter(lambda change: change['new_val']['id'] == id)

    return req.run(dbconnection)
