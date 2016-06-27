#!/usr/bin/env python3.5

import sqlite3
import json
import rethinkdb as r
from myslice import db

def main():
    conn = sqlite3.connect('db.sqlite')
    dbconnection = db.connect()

    cursor = conn.cursor()
    cursor.execute('''SELECT email, password, config from user''')
    for row in cursor:
        user_info = json.loads(row[2])
        data = {'password': row[1], 'last_name': user_info['lastname'], 'first_name': user_info['firstname']}
        
        query = r.db('myslice_quan').table('users').filter(r.row['email'] == row[0], default=False)
        for u in query.run(dbconnection):
            r.db('myslice_quan').table('users').get(u['id']).update(data).run(dbconnection)
            break
        
if __name__ == '__main__':
    main()
