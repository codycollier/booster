#!/usr/bin/env python


import time
import unittest

import boostertest


class TestAppserverCreateWebdav(boostertest.BoosterTestCase):
    """ Test the appserver-create-webdav action """

    def setUp(self):
        """ Set the action and other commonly used fixture data """
        self.params = {}
        self.params['action'] = "appserver-create-webdav"
        self.params['appserver-name'] = "some-web-app"
        self.params['group-name'] = "Default"
        self.params['database-name'] = "Documents"
        self.params['root'] = "/Docs"
        self.params['port'] = "8801"
        # collect app server names for later teardown
        self.teardown_appservers = []

    def tearDown(self):
        """ Remove items from server created during tests """
        params = {}
        params['action'] = "appserver-delete"
        params['group-name'] = "Default"
        for appserver in self.teardown_appservers:
            params['appserver-name'] = appserver
            response, body = self.booster.request(params)
            self.assertTrue(response.status in (404, 200))
            time.sleep(3)

    def test_basic_webdav_appserver_creation_results_in_201(self):
        """ A successful webdav appserver creation should result in a 201 """
        params = self.params
        params['appserver-name'] = "webdav-loops"
        self.teardown_appservers.append("webdav-loops")
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 201)
        self.assertEqual(err, "none")
        time.sleep(3)

    def test_create_webdav_appserver_with_existing_name_results_in_409(self):
        """ Attempting to create a pre-existing webdav appserver should result in 409 """ 
        params = self.params
        params['appserver-name'] = "grape-nuts"
        self.teardown_appservers.append("grape-nuts")
        # create the appserver
        response, body = self.booster.request(params)
        self.assertEqual(response.status, 201)
        time.sleep(3)
        # second create should result in 409
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 409)
        self.assertTrue(err.find("already exists") != -1)

    def test_create_webdav_appserver_in_nonexistent_group_results_in_500(self):
        """ An appserver-create-webdav should fail with 500 if group does not exist """
        params = self.params
        params['appserver-name'] = "webdav-crunch"
        params['group-name'] = "there-is-no-such-group"
        self.teardown_appservers.append("webdav-crunch")
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 500)
        self.assertTrue(err.find("Error running action 'appserver-create-webdav'. Error: No such group") > -1)

    def test_create_webdav_appserver_with_invalid_name_results_in_500(self):
        """ An appserver-create-webdav with invalid appserver-name should be rejected by api and result in 500 """
        badnames = ("%%zxcggg", "$fbbhhjh$")
        for badname in badnames:
            params = self.params
            params['appserver-name'] = badname
            # create should result in 500
            response, body = self.booster.request(params)
            err = response.get("x-booster-error", "none")
            self.assertEqual(response.status, 500)
            self.assertTrue(err.find("Error running action 'appserver-create-webdav'") != -1)
            self.assertTrue(err.find("Error: Invalid lexical value") != -1)

    def test_create_webdav_appserver_with_missing_required_parameter_results_in_400(self):
        """ A missing but required parameters should result in 400 """
        required_parameters = ("appserver-name", "group-name", "database-name", 
                                "root", "port")
        for rp in required_parameters:
            params = self.params.copy()
            del params[rp]
            response, body = self.booster.request(params)
            err = response.get("x-booster-error", "")
            self.assertEqual(response.status, 400)
            self.assertTrue(err.find("valid set of arguments was not provided") != 1)

    def test_create_webdav_appserver_with_empty_required_parameter_results_in_500(self):
        """ An empty but required parameters should result in 500 """
        required_parameters = ("appserver-name", "group-name", "database-name", 
                                "root", "port")
        for rp in required_parameters:
            params = self.params.copy()
            params[rp] = ""
            # create should result in 500
            response, body = self.booster.request(params)
            err = response.get("x-booster-error", "none")
            self.assertEqual(response.status, 500)
            self.assertTrue(err.find("Error running action 'appserver-create-webdav'") != -1)
            self.assertTrue(err.find("Error: ") != -1)


if __name__=="__main__":

    unittest.main()
    
