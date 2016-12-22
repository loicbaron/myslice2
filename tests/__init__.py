#!/usr/bin/env python3.5
import json
import requests

s = {}

s['email'] = "loic.baron@lip6.fr"
s['password'] = "cocoboy11"
payload = {'email': s['email'], 'password': s['password']}
r = requests.post("http://localhost:8111/api/v1/login", headers={str('Content-Type'):'application/json'}, data=json.dumps(payload))
s['cookies'] = r.cookies
