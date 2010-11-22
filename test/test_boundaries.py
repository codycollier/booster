#!/usr/bin/env python


import unittest

import boostertest


class TestBoundaries(boostertest.BoosterTestCase):
    """ Test boundary conditions 

    Almost all successful requests to booster require a valid action parameter 
    to be included.  These tests aim to confirm that booster fails gracefully 
    when the action parameter is invalid or missing.  It also covers other 
    boundary conditions which don't fit well in one of the other modules.
    """

    def setUp(self):
        """ """
        pass

    def tearDown(self):
        """ """
        pass

    def test_no_parameters_results_in_400(self):
        """ A call with no querystring or form parameters should result in 400 """
        response, body = self.booster.request()
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 400)
        self.assertTrue(err.find("action must be supplied") != -1)

    def test_invalid_action_results_in_400(self):
        """ Invalid action values should result in a 400 """
        params = {}
        params['action'] = 'nosuchaction'
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 400)
        self.assertTrue(err.find("not a valid action") != -1)

    def test_empty_action_results_in_400(self):
        """ An empty value for action should result in 400 """
        params = {}
        params['action'] = ''
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 400)
        self.assertTrue(err.find("not a valid action") != -1)


if __name__=="__main__":

    unittest.main()


