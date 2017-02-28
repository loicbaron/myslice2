#!/usr/bin/env python3.5
import json
import requests

s = {}
server = 'zeus.noc.onelab.eu'
s['email'] = "loic.baron@lip6.fr"
s['password'] = "test12345"
s['hrn'] = 'onelab.upmc.loic_baron'
payload = {'email': s['email'], 'password': s['password']}
r = requests.post("http://"+server+":8111/api/v1/login", headers={str('Content-Type'):'application/json'}, data=json.dumps(payload))
s['cookies'] = r.cookies

authority = "urn:publicid:IDN+onelab:upmc+authority+sa"
rootAuthority = "urn:publicid:IDN+onelab+authority+sa"



