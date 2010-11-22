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
        # keep track of created users
        self.created_users = []

    def tearDown(self):
        """ Remove any create test users """
        for user in self.created_users:
            params = {}
            params['action'] = "user-delete"
            params['user-name'] = user
            response, body = self.booster.request(params)
            self.assertTrue(response.status in (200,404))

    def test_basic_user_creation_results_in_201(self):
        """ A successful user creation should result in 201 """
        self.params.update(self.user1)
        self.created_users.append(self.params['user-name'])
        response, body = self.booster.request(self.params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 201)

    def test_user_creation_with_multiple_roles_succeeds(self):
        """ A user creation with multiple roles should succeed """
        self.params.update(self.user1)
        self.params['role-names'] = "app-user,alert-user"
        self.created_users.append(self.params['user-name'])
        response, body = self.booster.request(self.params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 201)

    def test_user_creation_with_multiple_permission_succeeds(self):
        """ A user creation with multiple permission pairs should succeed """
        self.params.update(self.user1)
        self.params['permissions'] = "app-user,read;app-user,update"
        self.created_users.append(self.params['user-name'])
        response, body = self.booster.request(self.params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 201)

    def test_user_creation_with_multiple_collections_succeeds(self):
        """ A user creation with multiple collections should succeed """
        self.params.update(self.user1)
        self.params['collections'] = "http://marklogic.com/xdmp/alert, http://marklogic.com/xdmp/triggers"
        self.created_users.append(self.params['user-name'])
        response, body = self.booster.request(self.params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 201)

    def test_no_user_name_results_in_400(self):
        """ A non-existent user-name value should result in 400 """
        response, body = self.booster.request(self.params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 400)
        self.assertTrue(err.find("valid set of arguments was not provided") != 1)

    @boostertest.skiptest
    def test_empty_user_name_results_in_400(self):
        """ An empty user-name value should result in 400 """
        #self.booster.debuglevel = 1
        self.params['user-name'] = ""
        response, body = self.booster.request(self.params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 400)
        #self.assertTrue(err.find("") != 1)



if __name__=="__main__":

    unittest.main()
    
