#!/usr/bin/env python


import time
import unittest

import boostertest


class TestDatabaseDeleteField(boostertest.BoosterTestCase):
    """ Test the database-delete-field action """

    def setUp(self):
        """ Set the action and other commonly used fixture data """
        self.params = {}
        self.params['action'] = "database-delete-field"
        self.params['database-name'] = "Documents"
        self.params['field-name'] = "myNewField"
        # collect appserver names for later teardown
        self.teardown_fields = []

    def tearDown(self):
        """ Remove items from server created during tests """
        params = {}
        params['action'] = "database-delete-field"
        params['database-name'] = "Documents"
        for field  in self.teardown_fields:
            params['field-name'] = field 
            time.sleep(3)
            response, body = self.booster.request(params)
            self.assertTrue(response.status in (404, 200))

    def test_basic_field_deletion_results_in_200(self):
        """ A successful appserver deletion should result in 200 """
        # create the field 
        params = {}
        params['action'] = "database-add-field"
        params['database-name'] = "Documents"
        params['field-name'] = "field19"
        self.teardown_fields.append(params['field-name'])
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 201)
        self.assertEqual(err, "none")
        # delete and assert
        params = self.params
        params['field-name'] = "field19"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 200)
        self.assertEqual(err, "none")

    def test_delete_nonexistent_field_results_in_404(self):
        """ Attempting to delete a non-existent field should return 404 """
        params = self.params
        params['field-name'] = "no-such-field-exists-here"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 404)
        self.assertTrue(err.find("does not exist") != 1)

    def test_empty_field_name_results_in_404(self):
        """ A database-delete-field with empty field-name value should result in 404 """
        params = self.params
        params['field-name'] = ""
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 404)
        self.assertTrue(err.find("Field '' does not exist") != -1) 

    def test_delete_database_field_with_no_field_name_results_in_400(self):
        """ A database-delete-field with missing field-name should result in 400 """
        params = self.params
        del params['field-name'] 
        response, body = self.booster.request(self.params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 400)
        self.assertTrue(err.find("valid set of arguments was not provided") != 1)

    def test_delete_database_field_in_nonexistent_database_results_in_500(self):
        """ Attempting to delete a non-existent appserver should return 404 """
        params = self.params
        params['db-name'] = "no-such-db-exists-here"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 500)
        self.assertTrue(err.find("Error running action 'database-delete-field'. Error: No such database") > -1)



if __name__=="__main__":

    unittest.main()
    
