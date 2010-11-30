#!/usr/bin/env python


import unittest

import boostertest


class TestGroupDelete(boostertest.BoosterTestCase):
    """ Test the group-delete action """

    def setUp(self):
        """ Set the action and other commonly used fixture data """
        self.params = {}
        self.params['action'] = "group-delete"
        self.params['group-name'] = "any-old-group"
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

    def test_basic_group_deletion_results_in_200(self):
        """ A successful group deletion should result in 200 """
        # create the group
        params = self.params
        params['group-name'] = "rosebushes"
        params['action'] = "group-create"
        self.teardown_groups.append(params['group-name'])
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 201)
        self.assertEqual(err, "none")
        # delete and assert
        params['action'] = "group-delete"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 200)
        self.assertEqual(err, "none")

    def test_delete_nonexistent_group_results_in_404(self):
        """ Attempting to delete a non-existent group should return 404 """
        params = self.params
        params['group-name'] = "no-such-group-here"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 404)
        self.assertTrue(err.find("does not exist") != 1)

    def test_empty_group_name_results_in_404(self):
        """ A group-delete with empty group-name value should result in 404 """
        params = self.params
        params['group-name'] = ""
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 404)
        self.assertTrue(err.find("Group '' does not exist") != -1)

    def test_delete_group_with_no_group_name_results_in_400(self):
        """ A group-delete with missing group-name should result in 400 """
        params = self.params
        del params['group-name']
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 400)
        self.assertTrue(err.find("valid set of arguments was not provided") != 1)


if __name__=="__main__":

    unittest.main()
    
