import sys, os, logging

class settings(object):

    class email(object):
        theme = 'onelab'
        host = 'smtp.gmail.com'
        port = 587
        ssl = True
        user = 'zhouquantest16@gmail.com'
        password = 'zqtest123'
        domain = theme + '.eu'
        dir_path = os.path.expanduser("~/intern/myslice/myslice/email/templates")