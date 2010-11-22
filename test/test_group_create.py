#!/usr/bin/env python


import unittest

import boostertest


class TestGroupCreate(boostertest.BoosterTestCase):
    """ Test the group-create action """

    def setUp(self):
        """ Set the action and other commonly used fixture data """
        self.params = {}
        self.params['action'] = "group-create"
        # collect group names for later teardown
        self.teardown_groups = []

    def tearDown(self):
        """ Remove items from server created during tests """
        params = {}
        params['action'] = "group-delete"
        for group in self.teardown_groups:
            params['group-name'] = group
            response, body = self.booster.request(params)
            self.assertTrue(response.status in (404, 200))

    def test_basic_group_creation_results_in_201(self):
        """ A successful group creation should result in a 201 """
        params = self.params
        params['group-name'] = "orange-servers"
        self.teardown_groups.append("orange-servers")
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 201)
        self.assertEqual(err, "none")

    def test_create_group_with_existing_name_results_in_409(self):
        """ Attempting to create a pre-existing group should result in 409 """ 
        params = self.params
        params['group-name'] = "orange-servers"
        self.teardown_groups.append("orange-servers")
        # create the group
        response, body = self.booster.request(params)
        self.assertEqual(response.status, 201)
        # second create should result in 409
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 409)
        self.assertTrue(err.find("already exists") != -1)

    def test_no_group_name_results_in_400(self):
        """ A non-existent group-name value should result in 400 """
        response, body = self.booster.request(self.params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 400)
        self.assertTrue(err.find("valid set of arguments was not provided") != 1)

    @boostertest.skiptest
    def test_empty_group_name_results_in_400(self):
        """ An empty group-name value should result in 400 """
        #self.booster.debuglevel = 1
        self.params['group-name'] = ""
        response, body = self.booster.request(self.params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 400)
        #self.assertTrue(err.find("") != 1)

    def test_create_group_with_invalid_name_results_in_500(self):
        """ Invalid group names should be rejected by api and result in 500 """
        badnames = ("%%zxcggg", "$fbbhhjh$")
        for badname in badnames:
            params = self.params
            params['group-name'] = badname
            # create should result in 500
            response, body = self.booster.request(params)
            err = response.get("x-booster-error", "none")
            self.assertEqual(response.status, 500)
            self.assertTrue(err.find("Error running action 'group-create'") != -1)
            self.assertTrue(err.find("Error: Invalid lexical value") != -1)


if __name__=="__main__":

    unittest.main()
    
