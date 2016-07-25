from setuptools import setup

setup(name='myslice',
      version='2.0.0',
      description='MySlice version 2',
      url='http://myslice.info',
      author='Ciro Scognamiglio',
      author_email='ciro.scognamiglio@lip6.fr',
      license='MIT',
      packages=['myslice'],
      install_requires=[
          'tornado',
          'tornado_cors',
          'SockJS-tornado',
          'rethinkdb',
          'requests',
          'pycryptodome',
          'pytz',
          'python-dateutil',
          'premailer',
          'python-oauth2',
          'pyzmq'

          ],
      #scripts=['myslice/bin/myslice-sync', 'myslice/bin/myslice-web'],
      #data_files=[('/etc', ['config/planetlab.cfg-dist']),
      #            ('/etc/init.d', ['init/myslice'])],
      zip_safe=False)
