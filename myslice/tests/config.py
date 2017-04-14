#!/usr/bin/env python3.5
import json
import requests

s = {}
server = 'theseus.noc.onelab.eu'
s['email'] = "loic.baron@lip6.fr"
s['password'] = "test12345"
s['hrn'] = 'onelab.upmc.loic_baron'
print("config trying to login to %s" % server)
payload = {'email': s['email'], 'password': s['password']}
r = requests.post("http://"+server+":8111/api/v1/login", headers={str('Content-Type'):'application/json'}, data=json.dumps(payload))
s['cookies'] = r.cookies
s['automate_test'] = False

authority = "urn:publicid:IDN+onelab:upmc+authority+sa"
rootAuthority = "urn:publicid:IDN+onelab+authority+sa"

#on this project we will test creating deleting slices
project = "urn:publicid:IDN+onelab:upmc:testradomir+authority+sa"

