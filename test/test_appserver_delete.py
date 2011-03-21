#!/usr/bin/env python


import time
import unittest

import boostertest


class TestAppserverDelete(boostertest.BoosterTestCase):
    """ Test the appserver-delete action """

    def setUp(self):
        """ Set the action and other commonly used fixture data """
        self.params = {}
        self.params['action'] = "appserver-delete"
        self.params['group-name'] = "Default"
        self.params['appserver-name'] = "slats"
        # collect appserver names for later teardown
        self.teardown_appservers = []

    def tearDown(self):
        """ Remove items from server created during tests """
        params = {}
        params['action'] = "appserver-delete"
        params['group-name'] = "Default"
        for appserver in self.teardown_appservers:
            params['appserver-name'] = appserver
            time.sleep(3)
            response, body = self.booster.request(params)
            self.assertTrue(response.status in (404, 200))

    def test_basic_appserver_deletion_results_in_200(self):
        """ A successful appserver deletion should result in 200 """
        # create the appserver
        params = {}
        params['action'] = "appserver-create-http"
        params['appserver-name'] = "mrtickle"
        params['group-name'] = "Default"
        params['modules-name'] = "Modules"
        params['database-name'] = "Documents"
        params['root'] = "/Docs"
        params['port'] = "8801"
        self.teardown_appservers.append(params['appserver-name'])
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 201)
        self.assertEqual(err, "none")
        # delete and assert
        params = self.params
        params['appserver-name'] = "mrtickle"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 200)
        self.assertEqual(err, "none")

    def test_delete_nonexistent_appserver_results_in_404(self):
        """ Attempting to delete a non-existent appserver should return 404 """
        params = self.params
        params['appserver-name'] = "no-such-appserver-exists-here"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 404)
        self.assertTrue(err.find("does not exist") != 1)

    def test_empty_appserver_name_results_in_404(self):
        """ A appserver-delete with empty appserver-name value should result in 404 """
        params = self.params
        params['appserver-name'] = ""
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 404)
        self.assertTrue(err.find("Appserver '' does not exist") != -1) 

    def test_delete_appserver_with_no_appserver_name_results_in_400(self):
        """ A appserver-delete with missing appserver-name should result in 400 """
        params = self.params
        del params['appserver-name'] 
        response, body = self.booster.request(self.params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 400)
        self.assertTrue(err.find("valid set of arguments was not provided") != 1)

    def test_delete_appserver_in_nonexistent_group_results_in_500(self):
        """ Attempting to delete a non-existent appserver should return 404 """
        params = self.params
        params['group-name'] = "no-such-group-exists-here"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 500)
        self.assertTrue(err.find("Error running action 'appserver-delete'. Error: No such group") > -1)



if __name__=="__main__":

    unittest.main()
    
