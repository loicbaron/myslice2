#!/usr/bin/env python3.5

import json
import rethinkdb as r
import sqlite3

from myslice import db
from myslice.db.user import User

from pprint import pprint

def hrn_to_urn(hrn, type):
    #urn:publicid:IDN+onelab+user+myslice
    urn = "urn:publicid:IDN+"
    shortname = hrn.split('.')[-1]
    hierarchy = hrn.split('.')[:-1]

    if type=="authority":
        hierarchy = hrn.split('.')
        shortname = "sa" 

    urn += ':'.join(hierarchy)
    urn += "+"+type+"+"+shortname

    return urn

def map_dict(config):
    data = {}
    credentials = []
    name_map = {
        'gid':'certificate',
        'user_hrn':'hrn',
        'user_private_key':'private_key',
        'user_public_key':'public_key',
        'authority_list':'pi_authorities', # convert hrn to urn
        'slice_list':'slices', # convert hrn to urn
    }
    #new_config = [dict(zip(map(lambda x: name_map[x] if x in name_map else x, config.keys()), config.values()))]
    for key, val in config.items():
        if 'credential' in key:
            lk = key.split('_')
            if len(lk)>2:
                key = lk[1]
                delegated_to = "onelab.myslice"

                if isinstance(val, dict):
                    for hrn, cred in val.items():
                        credentials.append({
                            'type': key,
                            'id': hrn_to_urn(hrn,key),
                            'xml': cred,
                            'delegated_to': delegated_to
                        })
                else:
                    credentials.append({
                        'type': key,
                        'id': hrn_to_urn(config['user_hrn'], 'user'),
                        'xml': val,
                        'delegated_to': delegated_to
                    })
        else:
            if key in name_map:
                if '_list' in key:
                    type = key.split('_')[0]
                    val = [hrn_to_urn(x, type) for x in val]
                data[name_map[key]] = val
    data['credentials'] = credentials
    return data

def main():
    conn = sqlite3.connect('/var/manifold/db.sqlite')
    dbconnection = db.connect()

    cursor = conn.cursor()
    cursor.execute('''SELECT email, password, config, user_id from user''')

    cursor2 = conn.cursor()
    # XXX TODO: get the account config of the user
    #           generate a private key if necessary

    for row in cursor:
        user_info = json.loads(row[2])
        data = {'email':row[0], 'password': row[1], 'last_name': user_info['lastname'], 'first_name': user_info['firstname']}
        if row[0] == 'admin':
            data['email'] = 'support@myslice.info'

        cursor2.execute('''SELECT config, auth_type from account where platform_id=5 AND user_id=%s''' % row[3])
        for c in cursor2:
            config = json.loads(c[0])
            pprint(data)
            data.update(map_dict(config))
            data['id'] = hrn_to_urn(data['hrn'], 'user')
            data['authority'] = hrn_to_urn(('.').join(data['hrn'].split('.')[:-1]), 'authority')
            # We don't handle manual delegation in MySlice v2
            # Let's generate a new key pair
            if c[1] != "managed" or not 'private_key' in data or data['private_key']=='N/A':
                data['generate_keys'] = True 
                print("Generate key for user %s" % data['hrn'])
            else:
                data['generate_keys'] = False 
            try:
                user = User(data)
                isSuccess = user.save(dbconnection)
            except Exception as e:
                import traceback
                traceback.print_exc()
                print("user will be ignored")
                continue

        #query = r.db('myslice').table('users').filter(r.row['email'] == row[0], default=False)
        #for u in query.run(dbconnection):
        #    r.db('myslice').table('users').get(u['id']).update(data).run(dbconnection)
        #    break

if __name__ == '__main__':
    main()
