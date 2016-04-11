import logging
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from myslice import settings as s
from myslice.db.activity import Event, Request

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

def get(c=None, table=None, id=None, filter=None):
    if not table:
        raise NotImplementedError('table must be specified')
def users(dbconnection=None, data=None):
    if not dbconnection:
        dbconnection = connect()

    if not c:
        c = connect()

    if id:
        return r.db(s.db.name).table(table).get(id).run(c)

    if filter:
        pass 
        # return somthing with filter

    return r.db(s.db.name).table(table).run(c)



    if data:
        r.db(s.db.name).table('users').insert(data, conflict='update').run(dbconnection)

    return r.db(s.db.name).table('users').run(dbconnection)

def projects(dbconnection=None, data=None):
    if not dbconnection:
        dbconnection = connect()

    if data:
        r.db(s.db.name).table('projects').insert(data, conflict='update').run(dbconnection)

    return r.db(s.db.name).table('projects').run(dbconnection)


def slices(dbconnection=None, data=None):
    if not dbconnection:
        dbconnection = connect()

    if (data):
        r.db(s.db.name).table('slices').insert(data, conflict='update').run(dbconnection)

    return r.db(s.db.name).table('slices').run(dbconnection)

def resources(dbconnection=None, filter=None):

    if not dbconnection:
        dbconnection = connect()

    if filter:
        # not yet implemented
        pass
    else:
        for res in r.table('resources').run(dbconnection):
            pass
            #print res
        return {"hello":"bye"}


def resource(dbconnection, resource=None):

    if resource:
        # updating

        # timestamp is stored as a rethinkdb expression,
        # will be retrieved as a native python dateobject
        #resource['timestamp'] = r.expr(datetime.now())
        resource['timestamp'] = r.now()

        r.table('resources').insert(resource, conflict='update').run(dbconnection)
    else:
        return r.table('resources').run(dbconnection)

def events(dbconnection=None, event=None, user=None, status=None, action=None):
    if not dbconnection:
        dbconnection = connect()

    if isinstance(event, Event):
        # update event on db
        ret = r.db(s.db.name).table('events').insert(event.dict(), conflict='update').run(dbconnection)

    req = r.db(s.db.name).table('events')

    if user:
        req.filter({'user':user})

    if status:
        req.filter({'user':status})

    if action:
        req.filter({'user':action})

    return req.run(dbconnection)

# retrieves an event
def event(dbconnection=None, id=None):
    if not id:
        return False

    if not dbconnection:
        dbconnection = connect()

    return r.db(s.db.table).table('events').get(id).run(dbconnection)

def dispatch(dbconnection=None, event=None):
    """
    Dispatch an Event or Request
    """

    if isinstance(event, Event):
        table = 'events'
    elif isinstance(event, Request):
        table = 'requests'
    else:
        raise Exception("Only Event or Request can be dispatched")

    # connect to db if connection is not specified
    if not dbconnection:
        dbconnection = connect()

    if event.id:
        ##
        # updating existing event/request
        ret = r.db(s.db.name).table(table).get(event.id).update(event.dict()).run(dbconnection)
    else:
        ##
        # dispatching new event/request
        ret = r.db(s.db.name).table(table).insert(event.dict()).run(dbconnection)

    # # import pprint
    # # pprint.pprint(ret)
    # if ret['errors'] > 0:
    #     event.message = ret['first_error']
    #     event.status = RequestStatus.ERROR
    #
    # if ret['errors'] > 0:
    #     self.message = ret['first_error']
    #     self.status = EventStatus.ERROR
    # elif ret['inserted'] > 0:
    #     self.id = ret['generated_keys'][0]

    return ret

    # return event


def delete(dbconnection=None, table=None, id=None):
    if not dbconnection:
        dbconnection = connect()

    if id and table:
        return r.db(s.db.name).table(table).get(id).delete().run(dbconnection)

    return False

def changes(dbconnection=None, table=None):
    if not table:
        return False

    if not dbconnection:
        dbconnection = connect()

    return r.db(s.db.name).table(table).changes().run(dbconnection)