
import unittest

import deployment
import rest_activity_authority
import rest_activity_slice
import rest_activity_user
import rest_authorities
import rest_login
import rest_projects
import rest_users
import rethinkdb as r

if __name__ == '__main__':
    suites = [unittest.TestLoader().loadTestsFromTestCase(deployment.TestDeployment),
              unittest.TestLoader().loadTestsFromTestCase(rest_login.TestLogin),
              unittest.TestLoader().loadTestsFromTestCase(rest_authorities.TestAuthority),
              unittest.TestLoader().loadTestsFromTestCase(rest_projects.TestProjects),
              unittest.TestLoader().loadTestsFromTestCase(rest_users.TestUsers),
              ]
    testResult = unittest.TextTestRunner(verbosity=0).run(unittest.TestSuite(suites))

    # print('The errors: ', testResult.errors)
    # print('The Failures: ', testResult.failures)
    # print('The number of runs: ', testResult.testsRun)
    # print('Test were successful: ', testResult.wasSuccessful())

    r.connect("localhost", 28015).repl()

    err = []
    for module, detail in testResult.errors:
        x = {}
        x['module'] = str(module).replace("'", '\'')
        x['details'] = str(detail).replace("'", '\'')
        err.append(x)

    fail = []
    for module, detai   l in testResult.failures:
        x = {}
        x['module'] =  str(module).replace("'", '\'')
        x['details'] = str(detail).replace("'", '\'')
        fail.append(x)

    status = "OK" if testResult.wasSuccessful()  else "Failed"

    # r.table('turtles').insert({
    #     "status": ,
    #     "failures": fail,
    #     "tests": testResult.testsRun,
    #     "errors": err,
    #     "failno": len(fail),
    #     "errno": len(err),
    # }).run()
