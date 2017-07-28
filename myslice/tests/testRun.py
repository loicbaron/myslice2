#!/usr/bin/env python3.5
import sys
import unittest
from myslice.tests.rest_authorities import TestAuthority
from myslice.tests.rest_login import TestLogin
from myslice.tests.rest_projects import TestProjects
from myslice.tests.rest_users import TestUsers
from myslice.tests.rest_slices import TestSlices
from myslice.tests.rest_leases import TestLeases
from myslice.tests.tools import send_email
from myslice.tests.config import s, server

if __name__ == '__main__':

    # we expect to have FQDN of the server we want to test,
    # otherwise FQDN will be taken from config file

    #define server you want to test
    if len(sys.argv) == 2:
        servername = sys.argv.pop()
        TestLogin.SERVER = servername
        TestAuthority.SERVER = servername
        TestProjects.SERVER = servername
        TestUsers.SERVER = servername
        TestLeases.SERVER = servername
    else:
        servername = server

    #define tests you want to run
    suites = [unittest.TestLoader().loadTestsFromTestCase(TestLogin),
              unittest.TestLoader().loadTestsFromTestCase(TestAuthority),
              unittest.TestLoader().loadTestsFromTestCase(TestProjects),
              unittest.TestLoader().loadTestsFromTestCase(TestUsers),
              unittest.TestLoader().loadTestsFromTestCase(TestSlices),
              unittest.TestLoader().loadTestsFromTestCase(TestLeases)
              ]
    testSuite = unittest.TestSuite(suites)

    #update test defitnitions in MySQL for the server
    # this is quite nasty - to be updated :/
    if s['automate_test']:
        from myslice.tests.mysqlTestBackend import MysqlTestBackend
        database = MysqlTestBackend(server = servername)
        database.updateTestDefinitions(testSuite)
        database.close()


    #run tests and collect output
    testResult = unittest.TextTestRunner(verbosity=0, buffer=True).run(unittest.TestSuite(suites))

    if s['automate_test']:

        #save results to db
        database = MysqlTestBackend(testResult, servername)
        database.newTestRun()
        database.saveTestResults()

        #send emails about errors
        unnoticedIssues = database.getListOfUnemailedIssues()

        to = ['radomir.klacza@lip6.fr',
		# ]
         #'pauline.gaudet-chardonnet@lip6.fr',
          #             'radomir.klacza@lip6.fr',
                       'loic.baron@lip6.fr',
                       'amira.bradai@lip6.fr']

        for issue in unnoticedIssues:
            subject = issue['server'] + " on " + issue['issue']
            body = "Date: " + str(issue['date']) + "\n" \
                   + "Server: " + issue['server'] + "\n" \
                   + "testCase: " + issue['testCase'] + "\n" \
                   + "test function name: " + issue['testFunction'] + "\n" \
                   + "Issue type: " + issue['issue'] + "\n" \
                   + "Problem description: " + issue['issue_text'] + "\n" \
                   + "\n\n\n You can find more info here: http://url \n" \
                   + "\n\n\n Kind regards\n Your tester"

            for person in to:
                send_email(subject, body, person)
            database.setTestEmailSent(1, issue['testCase'], issue['testFunction'])


        database.close()


