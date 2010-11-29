#!/usr/bin/env python


import unittest

import boostertest


class TestGroupSet(boostertest.BoosterTestCase):
    """ Test the group-set* action """

    def setUp(self):
        """ Create a test group to be used in most tests """
        self.params = {}
        self.params['action'] = "group-create"
        self.params['group-name'] = "group007"
        response, body = self.booster.request(self.params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 201)
        self.assertEqual(err, "none")
        # collect group names for later teardown
        self.teardown_groups = []
        self.teardown_groups.append(self.params['group-name'])

    def tearDown(self):
        """ Remove items from server created during tests """
        params = {}
        params['action'] = "group-delete"
        for group in self.teardown_groups:
            params['group-name'] = group
            response, body = self.booster.request(params)
            self.assertTrue(response.status in (404, 200))

    def test_basic_group_set_settings_result_in_200(self):
        """ Ensure happy path versions of group-set settings return 201"""
        params = self.params
        params['action'] = "group-set"
        # skipped
        #("audit-role-restriction", ""),            # skipped - needs two val args
        #("audit-uri-restriction", ""),             # skipped - needs two val args
        #("audit-user-restriction", ""),            # skipped - needs two val args
        settings = (
                ("audit-enabled", "true"),                  # xs:boolean
                ("audit-outcome-restriction", "failure"),   # xs:string
                ("compressed-tree-cache-partitions", "2"),  # xs:unsignedInt
                ("compressed-tree-cache-size", "128"),      # xs:unsignedInt
                ("compressed-tree-read-size", "256"),       # xs:unsignedInt
                ("expanded-tree-cache-partitions", "2"),    # xs:unsignedInt
                ("expanded-tree-cache-size", "256"),        # xs:unsignedInt
                ("failover-enable", "false"),               # xs:boolean
                ("file-log-level", "finest"),               # xs:string
                ("host-initial-timeout", "120"),            # xs:unsignedInt
                ("host-timeout", "120"),                    # xs:unsignedInt
                ("http-timeout", "120"),                    # xs:unsignedInt
                ("http-user-agent", "appserver client"),    # xs:string
                ("keep-audit-files", "7"),                  # xs:unsignedInt
                ("keep-log-files", "14"),                   # xs:unsignedInt
                ("list-cache-partitions", "1"),             # xs:unsignedInt
                ("list-cache-size", "256"),                 # xs:unsignedInt
                # note group is being set to same name to avoid later errors
                ("name", "group007"),                       # xs:string
                ("retry-timeout", "30"),                    # xs:unsignedInt
                ("rotate-audit-files", "daily"),            # xs:string
                ("rotate-log-files", "daily"),              # xs:string
                ("smtp-relay", "smtphost"),                 # xs:string
                ("smtp-timeout", "30"),                     # xs:unsignedInt
                ("system-log-level", "debug"),              # xs:string
                ("trace-events-activated", "false"),        # xs:boolean
                ("xdqp-ssl-allow-sslv3", "false"),          # xs:boolean
                ("xdqp-ssl-allow-tls", "false"),            # xs:boolean
                ("xdqp-ssl-ciphers", "All"),                # xs:string
                ("xdqp-ssl-enabled", "true"),               # xs:boolean
                ("xdqp-timeout", "15"),                     # xs:unsignedInt
                )
        for pair in settings:
            params['setting'], params['value'] = pair
            response, body = self.booster.request(params)
            err = response.get("x-booster-error", "none")
            self.assertEqual(err, "none")

    def test_group_set_on_nonexistent_group_results_in_404(self):
        """ Attempting set on a non-existent group should result in 404 """
        params = self.params
        params['action'] = "group-set"
        params['group-name'] = "group-does-not-exist"
        params['setting'] = "list-cache-partitions"
        params['value'] = "1"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertTrue(err.find("Group 'group-does-not-exist' does not exist") > -1)

    def test_group_set_on_nonexistent_setting_results_in_404(self):
        """ Attempting set on a non-existent setting should result in 404 """
        params = self.params
        params['action'] = "group-set"
        params['setting'] = "fake-setting"
        params['value'] = "1"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertTrue(err.find("Group setting 'fake-setting' does not exist") > -1)




if __name__=="__main__":

    unittest.main()
    
