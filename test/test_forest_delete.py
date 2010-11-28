#!/usr/bin/env python


import unittest

import boostertest


class TestForestDelete(boostertest.BoosterTestCase):
    """ Test the forest-delete action """

    def setUp(self):
        """ Set the action and other commonly used fixture data """
        self.params = {}
        self.params['action'] = "forest-delete"
        self.params['forest-name'] = "pinecone-a"
        # collect forest names for later teardown
        self.teardown_forests = []

    def tearDown(self):
        """ Remove items from server created during tests """
        params = {}
        params['action'] = "forest-delete"
        for forest in self.teardown_forests:
            params['forest-name'] = forest
            response, body = self.booster.request(params)
            self.assertTrue(response.status in (404, 200))

    def test_basic_forest_deletion_results_in_200(self):
        """ A successful forest deletion should result in 200 """
        # create the forest
        params = {}
        params['action'] = "forest-create"
        params['forest-name'] = "firs"
        params['host-name'] = "localhost"
        params['data-directory'] = "private"
        self.teardown_forests.append(params['forest-name'])
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 201)
        self.assertEqual(err, "none")
        # delete and assert
        params = self.params
        params['forest-name'] = "firs"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 200)
        self.assertEqual(err, "none")

    def test_delete_nonexistent_forest_results_in_404(self):
        """ Attempting to delete a non-existent forest should return 404 """
        params = self.params
        params['forest-name'] = "no-such-forest-exists-here"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 404)
        self.assertTrue(err.find("does not exist") != 1)

    def test_delete_forest_with_no_forest_name_results_in_400(self):
        """ A forest-delete with missing forest-name should result in 400 """
        params = self.params
        del params['forest-name'] 
        response, body = self.booster.request(self.params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 400)
        self.assertTrue(err.find("valid set of arguments was not provided") != 1)

    @boostertest.skiptest
    def test_empty_forest_name_results_in_500(self):
        """ A forest-delete with empty forest-name value should result in 500 """
        params = self.params
        params['forest-name'] = ""
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 500)
        self.assertTrue(err.find("Error running action 'forest-delete'") != -1) 
        self.assertTrue(err.find("Error: Invalid lexical value") != -1)


if __name__=="__main__":

    unittest.main()
    
