#!/usr/bin/env python


import unittest

import boostertest


class TestGroupCreate(boostertest.BoosterTestCase):
    """ Test the group-create action
    """

    def setUp(self):
        """ Set the action and other commonly used fixture data """
        self.params = {}
        self.params['action'] = "group-create"

    def tearDown(self):
        """ """
        pass

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


if __name__=="__main__":

    unittest.main()
    
