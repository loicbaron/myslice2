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
        },
        {
            'name' : 'sessions',
            'pkey' : 'id'
        },
        {
            'name' : 'messages',
            'pkey' : 'id'
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

def syncTestbeds(testbeds):
    """
    With the testbeds parameter specified syncs the db
    testbeds parameter is of type mysliceslib.model.Entity

    :param testbeds:
    :return:
    """

    dbconnection = connect()

    localTestbeds = r.db(s.db.name).table('testbeds').run(dbconnection)

    # sync
    for t in localTestbeds:
        u = testbeds.get(t['id'])
        if u is not None:
            # update
            try:
                logger.info('updating testbed {} ({})'.format(u.name, u.type))
                r.db(s.db.name).table('testbeds').update(u.dict()).run(dbconnection)
            except Exception as e:
                logger.error('{}'.format(str(e)))
            # remove the element from the working set
            testbeds.remove(u)
        else:
            # delete
            try:
                logger.info('deleting testbed {} ({})'.format(t['name'], t['type']))
                r.db(s.db.name).table('testbeds').get(t['id']).delete().run(dbconnection)
            except Exception as e:
                logger.error('{}'.format(str(e)))

    # check new testbeds with the remaining elements
    for n in testbeds:
        # new
        try:
            logger.info('new testbed {} ({})'.format(n.name, n.type))
            r.db(s.db.name).table('testbeds').insert(n.dict(), conflict='update').run(dbconnection)
        except Exception as e:
            logger.error('{}'.format(str(e)))

def getTestbeds():
    """
    Returns the list of testbeds
    :return:
    """
    pass

def syncResources(resources):
    """
    With the resources parameter specified syncs the db
    resources parameter is of type mysliceslib.model.Entity

    :param resources:
    :return:
    """

    dbconnection = connect()

    localResources = r.db(s.db.name).table('resources').run(dbconnection)

    # sync
    for t in localResources:
        u = resources.get(t['id'])
        if u is not None:
            # update
            logger.info('updating resource {} ({})'.format(u.name, u.testbed))
            r.db(s.db.name).table('resources').update(u.dict()).run(dbconnection)
            # remove the element from the working set
            resources.remove(u)
        else:
            # delete
            logger.info('deleting resource {} ({})'.format(t['name'], t['testbed']))
            r.db(s.db.name).table('resources').get(t['id']).delete().run(dbconnection)

    # check new resources with the remaining elements
    for n in resources:
        # new
        logger.info('new resource {} ({})'.format(n.name, n.testbed))
        r.db(s.db.name).table('resources').insert(n.dict(), conflict='update').run(dbconnection)

def getResources():
    """
    Returns the list of resources
    :return:
    """
    pass


def syncLeases(leases):
    """
    With the leases parameter specified syncs the db
    leases parameter is of type mysliceslib.model.Entity

    :param leases:
    :return:
    slices: a list of slice to be Synchronized
    """

    slices = []

    dbconnection = connect()

    localLeases = r.db(s.db.name).table('leases').run(dbconnection)

    # clear the leases table
    r.db(s.db.name).table("leases").delete().run(dbconnection)

    # sync
    # we need to keep the local leases that match existing leases
    # as some testbeds don't provide the slice_id related to the Lease
    keep = False
    for ll in localLeases:
        for l in leases:
            if not isinstance(l, dict):
                l = l.dict()

            if matchLeases(l, ll):
                keep = True
        # This lease does not exist anymore
        if not keep:
            # Synchronize the Slice if we have it locally
            if 'slice_id' in ll and r.db(s.db.name).table('slices').get(ll['slice_id']).run(dbconnection):
                slices.append(ll['slice_id'])

    for l in leases:
        if not isinstance(l, dict):
            l = l.dict()
        # insert the lease
        r.db(s.db.name).table('leases').insert(l, conflict='update').run(dbconnection)
        # Synchronize the Slice if we have it locally
        if 'slice_id' in l and r.db(s.db.name).table('slices').get(l['slice_id']).run(dbconnection):
            slices.append(l['slice_id'])

    return slices

def matchLeases(l1, l2):
    """
    Check if 2 Leases parameters are matching
    used to determine if 2 Leases have the same resources at the same time
    indeed some AMs don't tag Leases with id...
    :return:
    boolean
    """
    if not isinstance(l1, dict):
        l1 = l1.dict()
    if not isinstance(l2, dict):
        l2 = l2.dict()
    if l1 == l2:
        return True
    if l1['resources'] == l2['resources']:
        if l1['start_time'] == l2['start_time'] and l1['duration'] == l2['duration']:
            return True
    return False

def getLeases():
    """
    Returns the list of leases
    :return:
    """
    pass


def get(dbconnection=None, table=None, id=None, filter=None, limit=None):
    if not table:
        raise NotImplementedError('table must be specified')

    if not dbconnection:
        dbconnection = connect()

    if id:
        return r.db(s.db.name).table(table).get(id).run(dbconnection)

    if filter:
        if limit:
            cursor = r.db(s.db.name).table(table).filter(filter).limit(limit).run(dbconnection)
        else:
            # return somthing with filter
            cursor = r.db(s.db.name).table(table).filter(filter).run(dbconnection)

    elif limit:
        cursor = r.db(s.db.name).table(table).limit(limit).run(dbconnection)
    else:
        cursor = r.db(s.db.name).table(table).run(dbconnection)
    res = list(cursor)
    #process_results(res)
    return res


def users(dbconnection=None, data=None, id=None, email=None, hashing=None):

    logger.debug("users function called in db/__init__.py")
    logger.debug("with parameters: data={}, id={}, email={}, hashing={}".format(data,id,email,hashing))

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
        return r.db(s.db.name).table('users').filter({'email':email}).run(dbconnection)

    ##
    # Search user by hashing when reset passord
    if hashing:
        return r.db(s.db.name).table('users').filter({'hashing':hashing}).run(dbconnection)

    return r.db(s.db.name).table('users').run(dbconnection)

def authorities(dbconnection=None, data=None, id=None):
    if not dbconnection:
        dbconnection = connect()

    if id and data:
        r.db(s.db.name).table('authorities').get(id).update(data).run(dbconnection)

    if id:
        return r.db(s.db.name).table('authorities').get(id).run(dbconnection)

    if data:
        r.db(s.db.name).table('authorities').insert(data, conflict='update').run(dbconnection)

    return r.db(s.db.name).table('authorities').run(dbconnection)


def projects(dbconnection=None, data=None, id=None):
    if not dbconnection:
        dbconnection = connect()

    if id and data:
        r.db(s.db.name).table('projects').get(id).update(data).run(dbconnection)

    if id:
        return r.db(s.db.name).table('projects').get(id).run(dbconnection)

    if data:
        r.db(s.db.name).table('projects').insert(data, conflict='update').run(dbconnection)

    return r.db(s.db.name).table('projects').run(dbconnection)


def slices(dbconnection=None, data=None, id=None):
    if not dbconnection:
        dbconnection = connect()

    if id and data:
        r.db(s.db.name).table('slices').get(id).update(data).run(dbconnection)

    if id:
        return r.db(s.db.name).table('slices').get(id).run(dbconnection)

    if data:
        r.db(s.db.name).table('slices').insert(data, conflict='update').run(dbconnection)

    return r.db(s.db.name).table('slices').run(dbconnection)

def resources(dbconnection=None, data=None, id=None):
    if not dbconnection:
        dbconnection = connect()

    if id and data:
        r.db(s.db.name).table('resources').get(id).update(data).run(dbconnection)

    if id:
        return r.db(s.db.name).table('resources').get(id).run(dbconnection)

    if data:
        r.db(s.db.name).table('resources').insert(data, conflict='update').run(dbconnection)

    return r.db(s.db.name).table('resources').run(dbconnection)

def leases(dbconnection=None, data=None, id=None):
    if not dbconnection:
        dbconnection = connect()

    if id and data:
        r.db(s.db.name).table('leases').get(id).update(data).run(dbconnection)

    if id:
        return r.db(s.db.name).table('leases').get(id).run(dbconnection)

    if data:
        r.db(s.db.name).table('leases').insert(data, conflict='update').run(dbconnection)

    return r.db(s.db.name).table('leases').run(dbconnection)

def events(dbconnection=None, event=None, user=None, status=None, action=None, obj_type=None):
    if not dbconnection:
        dbconnection = connect()

    if isinstance(event, Event):
        # update event on db
        r.db(s.db.name).table('activity').insert(event.dict(), conflict='update').run(dbconnection)
    
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

    req = r.db(s.db.name).table(table)

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

    return req.changes().run(dbconnection)
