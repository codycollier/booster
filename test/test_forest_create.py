#!/usr/bin/env python


import unittest

import boostertest


class TestForestCreate(boostertest.BoosterTestCase):
    """ Test the forest-create action """

    def setUp(self):
        """ Set the action and other commonly used fixture data """
        self.params = {}
        self.params['action'] = "forest-create"
        self.params['forest-name'] = "docs-forest-a"
        self.params['host-name'] = "somehost"
        self.params['data-directory'] = "private"
        # collect app server names for later teardown
        self.teardown_forests = []

    def tearDown(self):
        """ Remove items from server created during tests """
        params = {}
        params['action'] = "forest-delete"
        for forest in self.teardown_forests:
            params['forest-name'] = forest 
            response, body = self.booster.request(params)
            self.assertTrue(response.status in (404, 200))

    def test_basic_forest_creation_results_in_201(self):
        """ A successful forest creation should result in a 201 """
        params = self.params
        params['forest-name'] = "treetops"
        self.teardown_forests.append("treetops")
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 201)
        self.assertEqual(err, "none")

    def test_create_forest_with_existing_name_results_in_409(self):
        """ Attempting to create a pre-existing forest should result in 409 """ 
        params = self.params
        params['forest-name'] = "forest-no-trees"
        self.teardown_forests.append("forest-no-trees")
        # create the forest
        response, body = self.booster.request(params)
        self.assertEqual(response.status, 201)
        # second create should result in 409
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 409)
        self.assertTrue(err.find("already exists") != -1)

    def test_create_forest_with_no_forest_name_results_in_400(self):
        """ A non-existent forest-name value should result in 400 """
        params = self.params
        del params['forest-name']
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 400)
        self.assertTrue(err.find("valid set of arguments was not provided") != 1)

    def test_create_forest_with_empty_forest_name_results_in_500(self):
        """ An forest-create with empty forest-name value should result in 500 """
        params = self.params
        params['forest-name'] = ""
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 500)
        self.assertTrue(err.find("Error running action 'forest-create'") != -1)
        self.assertTrue(err.find("Error: Invalid lexical value") != -1)

    def test_create_forest_with_invalid_name_results_in_500(self):
        """ An forest-create with invalid forest-name should be rejected by api and result in 500 """
        badnames = ("%%zxcggg", "$fbbhhjh$")
        for badname in badnames:
            params = self.params
            params['forest-name'] = badname
            # create should result in 500
            response, body = self.booster.request(params)
            err = response.get("x-booster-error", "none")
            self.assertEqual(response.status, 500)
            self.assertTrue(err.find("Error running action 'forest-create'") != -1)
            self.assertTrue(err.find("Error: Invalid lexical value") != -1)

    #def test_create_forest_with_public_data_directory(self):
    #def test_create_forest_with_no_host_name_results_in_400(self):
    #def test_create_forest_with_empty_host_name_results_in_500(self):
    #def test_create_forest_with_invalid_host_name_results_in_500(self):
    #def test_create_forest_with_no_data_directory_results_in_400(self):
    #def test_create_forest_with_empty_data_directory_results_in_500(self):
    #def test_create_forest_with_invalid_data_directory_results_in_500(self):


if __name__=="__main__":

    unittest.main()
    
