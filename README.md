MySlice Web Frontend
=======================

MySlice Web Frontend python module, for more information: `https://myslice.info`

Requirement
=======================
Install MySliceLib Module: `http://gitlab.noc.onelab.eu/onelab/myslicelib`

Install
=======================

~~~
    git clone git@gitlab.noc.onelab.eu:onelab/myslice.git
    pip3 install -r requirements.txt
    python3.5 setup.py develop
~~~


Configure
=======================

~~~
    vi ~/myslice/myslice/__init__.py
~~~


- Setup Endpoints: Registry and AMs
~~~
    myslicelibsetup.endpoints = [
            Endpoint(url="https://sfa3.planet-lab.eu:12346",type="AM", timeout=30, name="PLE"),
            Endpoint(url="https://localhost:6080",type="Reg", timeout=10, name="OneLab Registry"),
    ]
~~~

- Setup Admin account
~~~
    path = "/var/myslice/"
    pkey = path + "myslice.pkey"
    hrn = "onelab.myslice"
    email = "support@myslice.info"
    cert = path + "myslice.cert"
~~~

- Setup the RethinkDB connection
~~~
    class db(object):
        host = "localhost"
        port = 28015
        name = "myslice"
~~~
- Setup the email server connection
~~~
    class email(object):
        dirpath = '/myslice/myslice/web/templates/email'
        theme = 'onelab'
        domain = 'onelan.eu'
        host = 'smtp.gmail.com'
        port = 587
        ssl = True
        user = 'name@gmail.com'
        password = 'pass'
~~~
- Setup the Web server URL and Port
~~~
    class web(object):
        url = 'http://dev.myslice.info'
        port = '8111'
~~~

Run MySlice
=======================

~~~
    ~/myslice/myslice/bin/myslice-web
    ~/myslice/myslice/bin/myslice-server
    ~/myslice/myslice/bin/myslice-monitor
~~~