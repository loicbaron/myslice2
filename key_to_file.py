#!/usr/bin/env python3.5
import os

pkey = os.environ['MYSLICE_PKEY']
with open("/root/myslice.pkey", "w") as f:
    f.write(pkey)

cert = os.environ['MYSLICE_CERT']
with open("/root/myslice.cert", "w") as f:
    f.write(cert)
