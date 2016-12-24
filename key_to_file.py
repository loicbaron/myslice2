#!/usr/bin/env python3.5
import os

directory = "/var/myslice"
if not os.path.exists(directory):
    os.makedirs(directory)

pkey = os.environ['MYSLICE_PKEY']
with open("/var/myslice/myslice.pkey", "w") as f:
    f.write(pkey)

cert = os.environ['MYSLICE_CERT']
with open("/var/myslice/myslice.cert", "w") as f:
    f.write(cert)

cert = os.environ['MYSLICE_PUB']
with open("/var/myslice/myslice.pub", "w") as f:
    f.write(cert)
