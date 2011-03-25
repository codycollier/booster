#!/usr/bin/env python


import time
import unittest

import boostertest


class TestDatabaseAddField(boostertest.BoosterTestCase):
    """ Test the database-field-add action """

    def setUp(self):
        """ Set the action and other commonly used fixture data """
        self.params = {}
        self.params['action'] = "database-add-field"
        self.params['database-name'] = "Documents"
        self.params['field-name'] = "myNewField"
        self.params['include-root'] = "True"
        # collect app server names for later teardown
        self.teardown_fields= []

    def tearDown(self):
        """ Remove items from server created during tests """
        params = {}
        params['action'] = "database-delete-field"
        params['database-name'] = "Documents"
        for field in self.teardown_fields:
            params['field-name'] = field 
            response, body = self.booster.request(params)
            self.assertTrue(response.status in (404, 200))
            time.sleep(3)

    def test_basic_database_add_field_results_in_201(self):
        """ A successful database-add-field should result in a 201 """
        params = self.params
        params['field-name'] = "BasicElements"
        self.teardown_fields.append("BasicElements")
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 201)
        self.assertEqual(err, "none")
        time.sleep(3)

    def test_database_add_field_with_existing_name_results_in_409(self):
        """ Attempting to create a pre-existing field should result in 409 """ 
        params = self.params
        params['field-name'] = "DocDetails"
        self.teardown_fields.append("DocDetails")
        # create the appserver
        response, body = self.booster.request(params)
        self.assertEqual(response.status, 201)
        time.sleep(3)
        # second create should result in 409
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 409)
        self.assertTrue(err.find("already exists") != -1)

    def test_database_add_field_in_nonexistent_db_results_in_500(self):
        """ An database-add-field should fail with 500 if group does not exist """
        params = self.params
        params['field-name'] = "myField1"
        params['database-name'] = "there-is-no-such-db"
        self.teardown_fields.append("myField1")
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 500)
        self.assertTrue(err.find("Error running action 'database-add-field'. Error: No such group") > -1)

    def test_database_add_field_with_invalid_name_results_in_500(self):
        """ An database-add-field with invalid field-name should be rejected by api and result in 500 """
        badnames = ("%%zxcggg7654", "$fb123bhhjh$")
        for badname in badnames:
            params = self.params
            params['field-name'] = badname
            # create should result in 500
            response, body = self.booster.request(params)
            err = response.get("x-booster-error", "none")
            self.assertEqual(response.status, 500)
            self.assertTrue(err.find("Error running action 'database-add-field'") != -1)
            self.assertTrue(err.find("Error: Invalid lexical value") != -1)

    def test_database_add_field_with_missing_required_parameter_results_in_400(self):
        """ A missing but required parameter should result in 400 """
        required_parameters = ("database-name", "field-name", "include-root")
        for rp in required_parameters:
            params = self.params.copy()
            del params[rp]
            response, body = self.booster.request(params)
            err = response.get("x-booster-error", "")
            self.assertEqual(response.status, 400)
            self.assertTrue(err.find("valid set of arguments was not provided") != 1)

    def test_database_add_field_with_empty_required_parameter_results_in_500(self):
        """ An empty but required parameter should result in 500 """
        required_parameters = ("database-name", "field-name", "include-root")
        for rp in required_parameters:
            params = self.params.copy()
            params[rp] = ""
            # create should result in 500
            response, body = self.booster.request(params)
            err = response.get("x-booster-error", "none")
            self.assertEqual(response.status, 500)
            self.assertTrue(err.find("Error running action 'database-add-field'") != -1)
            self.assertTrue(err.find("Error: ") != -1)


if __name__=="__main__":

    unittest.main()
    
