#!/usr/bin/env python3.5

import pymysql
from datetime import datetime
from time import time
import sys

class MysqlTestBackend:

    def __init__(self, testResult = None, server = None, testid = None):
        self.db = pymysql.connect(host="localhost",    # your host, usually localhost
                     user="",         # your username
                     passwd="",  # your password
                     db="tester_myslice")        # name of the data base
        self.cursor = self.db.cursor()
        self.timestamp = datetime.now()
        self.timestamp = datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
        print(self.timestamp)
        self.testResult = testResult
        self.server = server
        self.testid = testid


    def close(self):
        self.db.close()

    def newTestRun(self):

        sql = "INSERT INTO testrun VALUES (NULL, %s)"
        self.cursor.execute(sql, (self.timestamp,))
        self.db.commit()
        self.testid = self.cursor.lastrowid


    def saveTestResults(self):

        if self.testResult and self.testid and self.server:

            # this need to be executed before saving issues (it sets all status to ok)
            self._updateLastTestExecution()

            # this is to save all issues
            self._saveIssues('errors', self._returnListOf(self.testResult.errors))
            self._saveIssues('failures', self._returnListOf(self.testResult.failures))

            #this is to clean up DB after inserting issues
            self._cleanDb()
        else:
            print("testResult and testid and server are required", self.testResult, self.testid, self.server)

    def setTestEmailSent(self, email_status, testClassName, testFunction):
        sql = "UPDATE tests set email_sent = %s WHERE testClassName = %s and testFunction = %s and server = %s"
        self.cursor.execute(sql, (email_status, testClassName, testFunction, self.server))
        self.db.commit()


    def getListOfUnemailedIssues(self):
        # The two SQL one can combine into one...
        allissues = []

        sql = "SELECT id, testClassName, testFunction, server, lastRun FROM tests WHERE status = 'FAILED' and (email_sent IS NULL OR email_sent = 0)"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()

        for record in data:
            sql = "SELECT timestamp, failed, err, failed_text, err_text FROM tests_results WHERE test_id = %s ORDER BY timestamp DESC LIMIT 1;"
            self.cursor.execute(sql, record[0])
            result = self.cursor.fetchall()[0]
            issue = "ERROR" if result[2] is not None else "FAILED"
            issue_text = result[3] if issue == 'FAILED' else result[4]
            allissues.append({'testCase' : record[1],
                              'testFunction': record[2],
                              'issue': issue,
                              'issue_text': issue_text,
                              'server': record[3],
                              'date': record[4],
                              })
        return allissues


    def _cleanDb(self, executedTestCase = None):

        if executedTestCase:
            # This need to be implemented
            pass
        else:
            try:
                # if status is NULL it means that we dont have issue any more
                print("cleaning tests after inserting issues")
                sql = "UPDATE tests set email_sent = NULL where server = %s and status is NULL"
                self.cursor.execute(sql, (self.server,))
                self.db.commit()

            except:
                print('failed while cleaning db after inserting tests')
                self.db.rollback()



    def _updateLastTestExecution(self, executedTestCase = None):

        if executedTestCase:
            # This need to be implemented
            pass
        else:
            try:
                print("updating all tests")
                sql = "UPDATE tests set lastRun = %s where server = %s"
                self.cursor.execute(sql, (self.timestamp, self.server))
                self.db.commit()
                sql = "UPDATE tests set status = NULL where server = %s"
                self.cursor.execute(sql, (self.server,))
                self.db.commit()
            except:
                print('failed while updating the lastRun of test')
                self.db.rollback()


    def _setTestStatus(self, testClassName, testFunction, status):
        sql = "UPDATE tests set status = %s WHERE testClassName = %s and testFunction = %s and server = %s"
        self.cursor.execute(sql, (status, testClassName, testFunction, self.server))
        self.db.commit()

    def _returnListOf(self, issues):
        fail = []
        for module, detail in issues:
            x = {}
            x['module'] = str(module).replace("'", '\'')
            x['details'] = str(detail).replace("'", '\'')
            fail.append(x)
        return fail


    def _getStatus(self):
        status = "OK" if self.testResult.wasSuccessful()  else "FAILED"
        return status



    def _saveIssues(self, kind, records):

        if kind == 'errors':
            sql_insert = "INSERT INTO tests_results VALUES (%s, %s, %s, NULL, 1, NULL, %s )"
        elif kind == 'failures':
            sql_insert = "INSERT INTO tests_results VALUES (%s, %s, %s, 1, NULL, %s, NULL )"
        else:
            print("Impossible just happened... check the code")

        for record in records:
            id = None
            functionName= record['module'].split(' ')[0]
            className = record['module'].split(' ')[1].split('.')[3].replace(')','')

            self._setTestStatus(className, functionName, "FAILED")

            try:
                sql_get_id = "SELECT id FROM tests WHERE testClassName = '%s' AND testFunction = '%s' AND server = '%s'"
                self.cursor.execute(sql_get_id % (className, functionName, self.server))
                id = int(self.cursor.fetchall()[0][0])

            except:
                print("Error: no id was found for the test", id, sys.exc_info())

            try:
                self.cursor.execute(sql_insert, (id, self.testid, self.timestamp, record['details']))
                self.db.commit()
            except:
                print("error in inserting values", sys.exc_info())
                self.db.rollback()

if __name__=='__main__':
    pass
