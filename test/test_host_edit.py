#!/usr/bin/env python


import time
import unittest

import boostertest


class TestHostEdit(boostertest.BoosterTestCase):
    """ Test the host actions """

    def setUp(self):
        """ Set the action and other commonly used fixture data """
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

    def test_basic_host_set_group_results_in_200(self):
        """ A successful host group change should result in 200 """
        # create a group 
        params = {}
        params['action'] = "group-create"
        params['group-name'] = "boxes54"
        self.teardown_groups.append("boxes54")
        response, body = self.booster.request(params)
        self.assertEqual(response.status, 201)
        # move a host to the new group
        params['action'] = "host-set-group"
        params['host-name'] = "localhost"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 200)
        self.assertEqual(err, "none")
        # sleep while the service restarts
        time.sleep(3)
        # move the host back to the default group
        params['action'] = "host-set-group"
        params['host-name'] = "localhost"
        params['group-name'] = "Default"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 200)
        self.assertEqual(err, "none")
        # sleep while the service restarts
        time.sleep(3)

    def test_host_set_group_on_nonexistent_group_results_in_404(self):
        """ Attempting move to a non-existent group should result in 404 """
        params = {}
        params['action'] = "host-set-group"
        params['host-name'] = "localhost"
        params['group-name'] = "bogus"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 404)
        self.assertTrue(err.find("Group 'bogus' does not exist") > -1)

    def test_host_set_group_on_nonexistent_host_results_in_404(self):
        """ Attempting move a non-existent host should result in 404 """
        params = {}
        params['action'] = "host-set-group"
        params['host-name'] = "bogus-host"
        params['group-name'] = "Default"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 404)
        self.assertTrue(err.find("Host 'bogus-host' does not exist") > -1)

    def test_host_set_group_with_missing_required_parameter_results_in_400(self):
        """ A missing but required parameter should result in 400 """
        params = {}
        params['action'] = "host-set-group"
        params['host-name'] = "localhost"
        params['group-name'] = "Default"
        for rp in ("host-name", "group-name"):
            params2 = params.copy()
            del params2[rp]
            response, body = self.booster.request(params2)
            err = response.get("x-booster-error", "")
            self.assertEqual(response.status, 400)
            self.assertTrue(err.find("valid set of arguments was not provided") != 1)


if __name__=="__main__":

    unittest.main()
    
