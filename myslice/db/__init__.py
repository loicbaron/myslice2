import logging
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from myslice import settings as s

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

def slices(c=None, data=None):
    if not c:
        c = connect()

    if (data):
        r.db(s.db.name).table('slices').insert(data, conflict='update').run(c)

def resources(c=None, filter=None):

    if not c:
        #print("connecting")
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


def select(id=None, filter=None, c=None):
    if not c:
        c = connect()
    x = r.db(Config.rethinkdb["db"]).table('resources')
    if id:
        x = r.get(id)
    if filter:
        pass
    return x.run(c)


def update(data, c=None):
    if not c:
        c = connect()
    r.db(Config.rethinkdb["db"]).table('resources').insert(data, conflict='update').run(c)

def changes(c=None):
    if not c:
        c = connect()
    return r.db(Config.rethinkdb["db"]).table('resources').changes().run(c)
