import logging
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from myslice import settings as s
from myslice.db.model import Event

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
            'name' : 'slices',
            'pkey' : 'id'
        },
        {
            'name' : 'users',
            'pkey' : 'id'
        },
        {
            'name' : 'events',
            'pkey' : 'id'
        },
        {
            'name': 'requests',
            'pkey': 'id'
        },
    ]

def connect():
    logger.info("Connecting to db {} on {}:{}".format(s.db.name,s.db.host,s.db.port))
    try :
        return r.connect(host=s.db.host, port=s.db.port, db=s.db.name)
    except RqlDriverError :
        logger.error("Can't connect to RethinkDB")
        raise SystemExit("Can't connect to RethinkDB")

def setup():

    c = connect()

    try:
        r.db_create(s.db.name).run(c)
        logger.info('MyOps2 database created successfully')
    except RqlRuntimeError:
        logger.info('MyOps2 database already exists')

    for t in tables:
        try:
            r.db(s.db.name).table_create(t['name'], primary_key=t['pkey']).run(c)
            logger.info('table %s setup completed', t['name'])
        except RqlRuntimeError:
            logger.info('table %s already exists', t['name'])

    c.close()


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

def users(c=None, data=None):
    if not c:
        c = connect()

    if data:
        r.db(s.db.name).table('users').insert(data, conflict='update').run(c)

    return r.db(s.db.name).table('users').run(c)

def projects(c=None, data=None):
    if not c:
        c = connect()

    if data:
        r.db(s.db.name).table('projects').insert(data, conflict='update').run(c)

    return r.db(s.db.name).table('projects').run(c)


def slices(c=None, data=None):
    if not c:
        c = connect()

    if (data):
        r.db(s.db.name).table('slices').insert(data, conflict='update').run(c)

    return r.db(s.db.name).table('slices').run(c)

def resources(c=None, filter=None):

    if not c:
        c = connect()

    if filter:
        # not yet implemented
        pass
    else:
        for res in r.table('resources').run(c):
            pass
            #print res
        return {"hello":"bye"}


def resource(c, resource=None):

    if resource:
        # updating

        # timestamp is stored as a rethinkdb expression,
        # will be retrieved as a native python dateobject
        #resource['timestamp'] = r.expr(datetime.now())
        resource['timestamp'] = r.now()

        r.table('resources').insert(resource, conflict='update').run(c)
    else:
        return r.table('resources').run(c)

def events(c=None, event=None, user=None, status=None, action=None):
    if not c:
        c = connect()

    if isinstance(event, Event):
        # update event on db
        ret = r.db(s.db.name).table('events').insert(event.dict(), conflict='update').run(c)

    req = r.db(s.db.name).table('events')

    if user:
        req.filter({'user':user})

    if status:
        req.filter({'user':status})

    if action:
        req.filter({'user':action})

    return req.run(c)

# retrieves an event
def event(c=None, id=None):
    if not id:
        return False

    if not c:
        c = connect()

    return r.db(s.db.table).table('events').get(id).run()

def delete(c=None, table=None, id=None):
    if not c:
        c = connect()

    if id and table:
        return r.db(s.db.name).table(table).get(id).delete().run(c)

    return False

def changes(c=None, table=None, filter=None):
    if not table:
        return False

    if not c:
        c = connect()

    changes = r.db(s.db.name).table(table)

    if filter:
        changes.filter(filter)

    return changes.changes().run(c)