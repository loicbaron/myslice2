#!/usr/bin/env python3.5
import time
time.sleep(10)

print("test should work")
import requests
r = requests.get('http://localhost:8111')
print(r.text)
r = requests.get('http://localhost:8080')
print(r.text)
