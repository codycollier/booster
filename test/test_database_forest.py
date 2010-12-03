#!/usr/bin/env python


import unittest

import boostertest


class TestDatabaseForest(boostertest.BoosterTestCase):
    """ Test the database and forest association actions """

    def setUp(self):
        """ Set the action and other commonly used fixture data """
        # collect app server names for later teardown
        self.teardown_databases = []
        self.teardown_forests = []
        # create a test database
        paramsd = {}
        paramsd['action'] = "database-create"
        paramsd['database-name'] = "test-dub"
        paramsd['security-db-name'] = "Security"
        paramsd['schema-db-name'] = "Schemas"
        self.teardown_databases.append(paramsd['database-name'])
        response, body = self.booster.request(paramsd)
        self.assertTrue(response.status in (201, 409))
        # create a test forest 
        paramsf = {}
        paramsf['action'] = "forest-create"
        paramsf['forest-name'] = "manytrees"
        paramsf['host-name'] = "localhost"
        paramsf['data-directory'] = ""
        self.teardown_forests.append(paramsf['forest-name'])
        response, body = self.booster.request(paramsf)
        self.assertTrue(response.status in (201, 409))
        # set common vars
        self.params = {}
        self.params['database-name'] = paramsd['database-name']
        self.params['forest-name'] = paramsf['forest-name']

    def tearDown(self):
        """ Remove items from server created during tests """
        # delete test databases 
        params = {}
        params['action'] = "database-delete"
        for database in self.teardown_databases:
            params['database-name'] = database 
            response, body = self.booster.request(params)
            self.assertTrue(response.status in (404, 200))
        # delete test forests
        params = {}
        params['action'] = "forest-delete"
        params['delete-data'] = "true"
        for database in self.teardown_forests:
            params['forest-name'] = database 
            response, body = self.booster.request(params)
            self.assertTrue(response.status in (404, 200))

    def test_basic_database_forest_attach_results_in_200(self):
        """ A successful database forest attach should result in a 200 """
        params = self.params
        params['action'] = "database-attach-forest"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 200)
        self.assertEqual(err, "none")

    def test_basic_database_forest_detach_results_in_200(self):
        """ A successful database forest detach should result in a 200 """
        # attach
        params = self.params
        params['action'] = "database-attach-forest"
        response, body = self.booster.request(params)
        self.assertEqual(response.status, 200)
        # detach and assert
        params['action'] = "database-detach-forest"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 200)
        self.assertEqual(err, "none")

    def test_attach_with_nonexistent_database_results_in_404(self):
        """ A forest attach to a non-existent db should result in a 404 """
        params = self.params
        params['action'] = "database-attach-forest"
        params['database-name'] = "fork"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 404)
        self.assertEqual(err, "Database 'fork' does not exist")

    def test_attach_with_nonexistent_forest_results_in_404(self):
        """ An attach with a non-existent forest should result in a 404 """
        params = self.params
        params['action'] = "database-attach-forest"
        params['forest-name'] = "spoons"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 404)
        self.assertEqual(err, "Forest 'spoons' does not exist")

    def test_detach_with_nonexistent_database_results_in_404(self):
        """ A forest detach to a non-existent db should result in a 404 """
        params = self.params
        params['action'] = "database-detach-forest"
        params['database-name'] = "knives"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 404)
        self.assertEqual(err, "Database 'knives' does not exist")

    def test_detach_with_nonexistent_forest_results_in_404(self):
        """ A detach with a non-existent forest should result in a 404 """
        params = self.params
        params['action'] = "database-detach-forest"
        params['forest-name'] = "sporks"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 404)
        self.assertEqual(err, "Forest 'sporks' does not exist")

    def test_attach_on_attached_forest_results_in_409(self):
        """ Attempting attach on an attached forest should result in a 409 """
        # attach
        params = self.params
        params['action'] = "database-attach-forest"
        response, body = self.booster.request(params)
        self.assertEqual(response.status, 200)
        # attempt another attach and assert
        params['action'] = "database-attach-forest"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 409)
        self.assertEqual(err, "Forest is already attached to a database")

    def test_detach_on_detached_forest_results_in_409(self):
        """ Attempting detach on a detached forest should result in a 409 """
        params = self.params
        params['action'] = "database-detach-forest"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 409)
        self.assertEqual(err, "Forest is not attached to given database")

    def test_attach_with_missing_database_name_results_in_400(self):
        """ A attach with a missing database-name should result in 400 """
        params = self.params
        params['action'] = "database-attach-forest"
        del params['database-name']
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 400)
        self.assertTrue(err.find("valid set of arguments was not provided") != 1)

    def test_detach_with_missing_forest_name_results_in_400(self):
        """ A detach with a missing forest-name should result in 400 """
        params = self.params
        params['action'] = "database-detach-forest"
        del params['forest-name']
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 400)
        self.assertTrue(err.find("valid set of arguments was not provided") != 1)

    def test_detach_with_missing_database_name_results_in_400(self):
        """ A detach with a missing database-name should result in 400 """
        params = self.params
        params['action'] = "database-detach-forest"
        del params['database-name']
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 400)
        self.assertTrue(err.find("valid set of arguments was not provided") != 1)

    def test_detach_with_missing_forest_name_results_in_400(self):
        """ A detach with a missing forest-name should result in 400 """
        params = self.params
        params['action'] = "database-detach-forest"
        del params['forest-name']
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 400)
        self.assertTrue(err.find("valid set of arguments was not provided") != 1)


if __name__=="__main__":

    unittest.main()
    
