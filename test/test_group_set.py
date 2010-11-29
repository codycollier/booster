#!/usr/bin/env python


import unittest

import boostertest


class TestGroupSet(boostertest.BoosterTestCase):
    """ Test the group-set* action """

    def setUp(self):
        """ Create a test group to be used in most tests """
        self.params = {}
        self.params['action'] = "group-create"
        self.params['group-name'] = "group007"
        response, body = self.booster.request(self.params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 201)
        self.assertEqual(err, "none")
        # collect group names for later teardown
        self.teardown_groups = []
        self.teardown_groups.append(self.params['group-name'])

    def tearDown(self):
        """ Remove items from server created during tests """
        params = {}
        params['action'] = "group-delete"
        for group in self.teardown_groups:
            params['group-name'] = group
            response, body = self.booster.request(params)
            self.assertTrue(response.status in (404, 200))

    def test_basic_group_set_settings_result_in_200(self):
        """ Ensure happy path versions of group-set settings return 201"""
        params = self.params
        params['action'] = "group-set"
        settings = (("list-cache-size", "500"), 
                    ("compressed-tree-cache-size", "300"))
        for pair in settings:
            params['setting'], params['value'] = pair
            response, body = self.booster.request(params)
            err = response.get("x-booster-error", "none")
            self.assertEqual(err, "none")




if __name__=="__main__":

    unittest.main()
    
