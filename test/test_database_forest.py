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
        self.assertEqual(response.status, 201)
        # create a test forest 
        paramsf = {}
        paramsf['action'] = "forest-create"
        paramsf['forest-name'] = "manytrees"
        paramsf['host-name'] = "localhost"
        paramsf['data-directory'] = "private"
        self.teardown_forests.append(paramsf['forest-name'])
        response, body = self.booster.request(paramsf)
        self.assertEqual(response.status, 201)
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


if __name__=="__main__":

    unittest.main()
    
