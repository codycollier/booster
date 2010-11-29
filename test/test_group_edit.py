#!/usr/bin/env python


import unittest

import boostertest


class TestGroupEdit(boostertest.BoosterTestCase):
    """ Test the actions related to editing of an existing group """

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

    def test_basic_group_set_list_cache_size_results_in_200(self):
        """ A basic set of a group list cache size should return a 200 """
        params = self.params
        params['action'] = "group-set-list-cache-size"
        params['value'] = "100"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(err, "none")





if __name__=="__main__":

    unittest.main()
    
