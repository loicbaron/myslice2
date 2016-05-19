from myslice.db.activity import ObjectType

def get_authority(obj_id, obj_type):
    '''
    Return the corresponding upper admin entity and its entity type
    '''
    if not obj_id.startswith('urn:publicid:IDN+'):
        raise TypeError("Object id is not a valid id")

    if obj_type == ObjectType.USER:
        authority = obj_id.split('+')[1]
        return "urn:publicid:IDN+{}+authority+sa".format(authority), "authorities"

    if obj_type == ObjectType.SLICE:
        project = obj_id.split('+')[1]
        return "urn:publicid:IDN+{}+authority+sa".format(project), "projects"

    if obj_type in [ObjectType.PROJECT, ObjectType.AUTHORITY]:
        # get onelab:upmc:project
        authority = obj_id.split('+')[1]
        upper_authority = ":".join(authority.split(':')[:-1])
        return "urn:publicid:IDN+{}+authority+sa".format(upper_authority), "authorities"

def has_privilege(user, obj):
    '''
    Return True if user has the privlege over the object.
    '''

    # user updates its own property
    # user updates its own slices(experiments)
    # user is Pi of the obj he wants to update
    if user.id == obj.id:
        return True    
    if obj.type == ObjectType.SLICE and obj.id in user.slices:
        return True
    
    obj_auth = get_authority(obj.id, obj.type)[0]
    if obj_auth in user.pi_authorities:
        return True

    for a in user.pi_authorities:
        if object.id.split('+')[1].startswith(a.split('+')[1]):
            return True

    return False
