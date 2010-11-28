#!/usr/bin/env python


import unittest

import boostertest


class TestDatabaseCreate(boostertest.BoosterTestCase):
    """ Test the database-create action """

    def setUp(self):
        """ Set the action and other commonly used fixture data """
        self.params = {}
        self.params['action'] = "database-create"
        self.params['database-name'] = "test-dub"
        self.params['security-db-name'] = "Security"
        self.params['schema-db-name'] = "Schemas"
        # collect app server names for later teardown
        self.teardown_databases = []

    def tearDown(self):
        """ Remove items from server created during tests """
        params = {}
        params['action'] = "database-delete"
        for database in self.teardown_databases:
            params['database-name'] = database 
            response, body = self.booster.request(params)
            self.assertTrue(response.status in (404, 200))

    def test_basic_database_creation_results_in_201(self):
        """ A successful database creation should result in a 201 """
        params = self.params
        params['database-name'] = "important-data-here"
        self.teardown_databases.append("important-data-here")
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 201)
        self.assertEqual(err, "none")

    def test_create_database_with_existing_name_results_in_409(self):
        """ Attempting to create a pre-existing database should result in 409 """ 
        params = self.params
        params['database-name'] = "radbase"
        self.teardown_databases.append("radbase")
        # create the database
        response, body = self.booster.request(params)
        self.assertEqual(response.status, 201)
        # second create should result in 409
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 409)
        self.assertTrue(err.find("already exists") != -1)

    def test_create_database_with_no_database_name_results_in_400(self):
        """ A non-existent database-name value should result in 400 """
        params = self.params
        del params['database-name']
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 400)
        self.assertTrue(err.find("valid set of arguments was not provided") != 1)

    def test_create_database_with_empty_database_name_results_in_500(self):
        """ An database-create with empty database-name value should result in 500 """
        params = self.params
        params['database-name'] = ""
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 500)
        self.assertTrue(err.find("Error running action 'database-create'") != -1)
        self.assertTrue(err.find("Error: Invalid configuration") != -1)

    def test_create_database_with_invalid_name_results_in_500(self):
        """ An database-create with invalid database-name should be rejected by api and result in 500 """
        badnames = ("%%zxcggg", "$fbbhhjh$")
        for badname in badnames:
            params = self.params
            params['database-name'] = badname
            # create should result in 500
            response, body = self.booster.request(params)
            err = response.get("x-booster-error", "none")
            self.assertEqual(response.status, 500)
            self.assertTrue(err.find("Error running action 'database-create'") != -1)
            self.assertTrue(err.find("Error: Invalid configuration") != -1)

    #def test_create_database_with_no_security_db_name_results_in_400(self):
    #def test_create_database_with_empty_security_db_name_results_in_500(self):
    #def test_create_database_with_invalid_security_db_name_results_in_500(self):
    #def test_create_database_with_no_schema_db_name_results_in_400(self):
    #def test_create_database_with_empty_schema_db_name_results_in_500(self):
    #def test_create_database_with_invalid_schema_db_name_results_in_500(self):

if __name__=="__main__":

    unittest.main()
    
