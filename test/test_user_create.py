#!/usr/bin/env python


import unittest

import boostertest


class TestUserCreate(boostertest.BoosterTestCase):
    """ Test the user-create action
    """

    def setUp(self):
        """ Set the action and other commonly used fixture data """
        self.params = {}
        self.params['action'] = "user-create"
        # sample users
        self.user1 = {}
        self.user1['user-name'] = "testuser1"
        self.user1['description'] = "test description 1"
        self.user1['password'] = "testpass1"
        self.user1['role-names'] = "admin"
        self.user1['permissions'] = ""
        self.user1['collections'] = ""
        # keep track of created users for later teardown
        self.teardown_users = []

    def tearDown(self):
        """ Remove any created test users """
        params = {}
        params['action'] = "user-delete"
        for user in self.teardown_users:
            params['user-name'] = user
            response, body = self.booster.request(params)
            self.assertTrue(response.status in (200,404))

    def test_basic_create_user_results_in_201(self):
        """ A successful user creation should result in 201 """
        params = self.params
        params.update(self.user1)   # merge in user1 data
        self.teardown_users.append(params['user-name'])
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 201)
        self.assertEqual(err, "none")

    def test_create_user_with_multiple_roles_succeeds(self):
        """ A user creation with multiple roles should succeed """
        params = self.params
        params.update(self.user1)   # merge in user1 data
        params['role-names'] = "app-user,alert-user"
        self.teardown_users.append(params['user-name'])
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 201)
        self.assertEqual(err, "none")

    def test_create_user_with_multiple_permission_succeeds(self):
        """ A user creation with multiple permission pairs should succeed """
        params = self.params
        params.update(self.user1)   # merge in user1 data
        params['permissions'] = "app-user,read;app-user,update"
        self.teardown_users.append(params['user-name'])
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 201)
        self.assertEqual(err, "none")

    def test_create_user_with_multiple_collections_succeeds(self):
        """ A user creation with multiple collections should succeed """
        params = self.params
        params.update(self.user1)   # merge in user1 data
        params['collections'] = "http://marklogic.com/xdmp/alert, http://marklogic.com/xdmp/triggers"
        self.teardown_users.append(params['user-name'])
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 201)
        self.assertEqual(err, "none")

    def test_create_user_with_no_user_name_results_in_400(self):
        """ A user-create with missing user-name should result in 400 """
        response, body = self.booster.request(self.params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 400)
        self.assertTrue(err.find("valid set of arguments was not provided") != 1)

    def test_create_user_with_empty_user_name_results_in_500(self):
        """ A user-create with empty user-name value should result in 500 """
        params = self.params
        params.update(self.user1)   # merge in user1 data
        params['user-name'] = ""
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 500)
        self.assertTrue(err.find("Error running action 'user-create'") != -1) 
        self.assertTrue(err.find("Error: Invalid lexical value") != -1) 

    def test_create_user_with_invalid_name_results_in_500(self):
        """ A user-create with invalid user-name should be rejected by api and result in 500 """
        params = self.params
        params.update(self.user1)   # merge in user1 data
        badnames = ("hows##", "fli$%")
        for badname in badnames:
            params = self.params
            params['user-name'] = badname
            # create should result in 500
            response, body = self.booster.request(params)
            err = response.get("x-booster-error", "none")
            self.assertEqual(response.status, 500)
            self.assertTrue(err.find("Error running action 'user-create'") != -1)
            self.assertTrue(err.find("Error: Invalid lexical value") != -1)

    #def test_create_user_with_no_password_results_in_400(self):
    #def test_create_user_with_empty_password_results_in_500(self):
    #def test_create_user_with_invalid_password_results_in_500(self):
    #def test_create_user_with_no_description_results_in_400(self):
    #def test_create_user_with_empty_description_results_in_201(self):
    #def test_create_user_with_invalid_description_results_in_500(self):
    #def test_create_user_with_no_role_names_results_in_400(self):
    #def test_create_user_with_empty_role_names_results_in_201(self):
    #def test_create_user_with_invalid_role_names_results_in_500(self):
    #def test_create_user_with_no_permissions_results_in_400(self):
    #def test_create_user_with_empty_permissions_results_in_201(self):
    #def test_create_user_with_invalid_permissions_results_in_500(self):
    #def test_create_user_with_no_collections_results_in_400(self):
    #def test_create_user_with_empty_collections_results_in_201(self):
    #def test_create_user_with_invalid_collections_results_in_500(self):



if __name__=="__main__":

    unittest.main()
    
