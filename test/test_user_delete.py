#!/usr/bin/env python


import unittest

import boostertest


class TestUserDelete(boostertest.BoosterTestCase):
    """ Test the user-delete action
    """

    def setUp(self):
        """ Set the action and other commonly used fixture data """
        self.params = {}
        self.params['action'] = "user-delete"
        self.params['user-name'] = "justauser"
        # sample user
        self.user1 = {}
        self.user1['user-name'] = "samuel35"
        self.user1['description'] = "user description"
        self.user1['password'] = "samspass"
        self.user1['role-names'] = "app-user"
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

    def test_basic_user_deletion_results_in_200(self):
        """ A successful user deletion should result in 200 """
        # create the user
        params = self.params
        params.update(self.user1)   # merge in user1 data
        params['action'] = "user-create"
        username = params['user-name']
        self.teardown_users.append(username)
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 201)
        self.assertEqual(err, "none")
        # delete and assert
        params = {}
        params['action'] = "user-delete"
        params['user-name'] = username
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 200)
        self.assertEqual(err, "none")

    def test_delete_nonexistent_user_results_in_404(self):
        """ Attempting to delete a non-existent user should return 404 """
        params = self.params
        params['user-name'] = "no-such-user-is-here-on-server-go-away"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 404)
        self.assertTrue(err.find("does not exist") != 1)

    def test_delete_user_with_no_user_name_results_in_400(self):
        """ A user-delete with missing user-name should result in 400 """
        params = self.params
        del params['user-name']
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "")
        self.assertEqual(response.status, 400)
        self.assertTrue(err.find("valid set of arguments was not provided") != 1)

    @boostertest.skiptest
    def test_empty_user_name_results_in_500(self):
        """ A user-delete with empty user-name value should result in 500 """
        params = self.params
        params['user-name'] = ""
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 500)
        self.assertTrue(err.find("Error running action 'user-delete'") != -1) 
        self.assertTrue(err.find("Error: Invalid lexical value") != -1)


if __name__=="__main__":

    unittest.main()
    
