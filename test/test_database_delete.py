#!/usr/bin/env python


import unittest

import boostertest


class TestDatabaseDelete(boostertest.BoosterTestCase):
    """ Test the database-delete action """

    def setUp(self):
        """ Set the action and other commonly used fixture data """
        self.params = {}
        self.params['action'] = "database-delete"
        self.params['database-name'] = "vipdb"
        # collect database names for later teardown
        self.teardown_databases = []

    def tearDown(self):
        """ Remove items from server created during tests """
        params = {}
        params['action'] = "database-delete"
        for database in self.teardown_databases:
            params['database-name'] = database
            response, body = self.booster.request(params)
            self.assertTrue(response.status in (404, 200))

    def test_basic_database_deletion_results_in_200(self):
        """ A successful database deletion should result in 200 """
        # create the database
        params = {}
        params['action'] = "database-create"
        params['database-name'] = "tomba"
        params['security-db-name'] = "Security"
        params['schema-db-name'] = "Schemas"
        self.teardown_databases.append(params['database-name'])
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 201)
        self.assertEqual(err, "none")
        # delete and assert
        params = self.params
        params['database-name'] = "tomba"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 200)
        self.assertEqual(err, "none")

    def test_delete_nonexistent_database_results_in_404(self):
        """ Attempting to delete a non-existent database should return 404 """
        params = self.params
        params['database-name'] = "no-such-database-exists-here"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 404)
        self.assertTrue(err.find("does not exist") != -1) 

    def test_empty_database_name_results_in_404(self):
        """ A database-delete with empty database-name value should result in 404 """
        params = self.params
        params['database-name'] = ""
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 404)
        self.assertTrue(err.find("Database '' does not exist") != -1) 

    def test_delete_database_with_no_database_name_results_in_400(self):
        """ A database-delete with missing database-name should result in 400 """
        params = self.params
        del params['database-name'] 
        response, body = self.booster.request(self.params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 400)
        self.assertTrue(err.find("valid set of arguments was not provided") != 1)



if __name__=="__main__":

    unittest.main()
    
