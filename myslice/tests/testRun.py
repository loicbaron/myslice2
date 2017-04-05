#!/usr/bin/env python3.5
import unittest

from myslice.tests.rest_authorities import TestAuthority
from myslice.tests.rest_login import TestLogin
from myslice.tests.rest_projects import TestProjects
from myslice.tests.rest_users import TestUsers
from myslice.tests.rest_slices import TestSlices
from myslice.tests.rest_leases import TestLeases
from myslice.tests.tools import send_email

import rethinkdb as r
from myslice.tests.config import s
from datetime import datetime

from myslice.tests.config import server

def runTest():

    suites = [unittest.TestLoader().loadTestsFromTestCase(TestLogin),
              unittest.TestLoader().loadTestsFromTestCase(TestAuthority),
              unittest.TestLoader().loadTestsFromTestCase(TestProjects),
              unittest.TestLoader().loadTestsFromTestCase(TestUsers),
              unittest.TestLoader().loadTestsFromTestCase(TestSlices),
              unittest.TestLoader().loadTestsFromTestCase(TestLeases)
              ]

    testResults = unittest.TextTestRunner(verbosity=0).run(unittest.TestSuite(suites))

    return testResults




    # saving data for automate tests
    # if s['automate_test']:
    #     r.connect("localhost", 28015).repl()
    #     r.table('turtles').insert({
    #         "status": status,
    #         "failures": fail,
    #         "tests": testResult.testsRun,
    #         "errors": err,
    #         "failno": len(fail),
    #         "errno": len(err),
    #         "timestamp": datetime.now(r.make_timezone('00:00')),
    #     }).run()
    #
    # # sending email if test failed
    # if s['automate_test'] and not testResult.wasSuccessful() and testResult.wasSuccessful() == 'aaa':
    #     for f in fail:
    #         subject = "ERR: " + f['module']
    #
    #         body = "Testing server: "\
    #                + server \
    #                + " \n " \
    #                + f['details'] + \
    #                "\n more info: http://132.227.122.107:8080/#dataexplorer"
    #
    #         to = ['pauline.gaudet-chardonnet@lip6.fr',
    #               'radomir.klacza@lip6.fr',
    #               'loic.baron@lip6.fr',
    #               'amira.bradai@lip6.fr']
    #
    #
    #         for t in to:
    #             send_email(subject, body,  t)
    #         # send_email(subject, body,  'radomir.klacza@lip6.fr')


if __name__ == '__main__':
    #run tests
    testResult = runTest()

    if s['automate_test']:
        from myslice.tests.mysqlTestBackend import MysqlTestBackend
        #save results to db
        database = MysqlTestBackend(testResult, server)
        database.newTestRun()
        database.saveTestResults()

        #send emails about errors
        unnoticedIssues = database.getListOfUnemailedIssues()

        to = ['radomir.klacza@lip6.fr', ]
        # 'pauline.gaudet-chardonnet@lip6.fr',
        #               'radomir.klacza@lip6.fr',
        #               'loic.baron@lip6.fr',
        #               'amira.bradai@lip6.fr']

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




        # from multiprocessing import Process
    # for i in range(1):
    #     print("startingg")
    #     p = Process(target=runTest)
    #     p.start()
