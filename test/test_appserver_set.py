#!/usr/bin/env python


import time
import unittest

import boostertest


class TestAppserverSet(boostertest.BoosterTestCase):
    """ Test the appserver-set* action """

    def setUp(self):
        """ Create appserver and params """
        # create test appserver
        params = {}
        params['action'] = "appserver-create-http"
        params['appserver-name'] = "test-app-123"
        params['group-name'] = "Default"
        params['modules-name'] = "Modules"
        params['database-name'] = "Documents"
        params['root'] = "/Docs"
        params['port'] = "8801"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 201)
        self.assertEqual(err, "none")
        time.sleep(3)
        # collect appserver names for later teardown
        self.teardown_appservers = []
        self.teardown_appservers.append(params['appserver-name'])
        # common params
        self.params = {}
        self.params['action'] = "appserver-set"
        self.params['appserver-name'] = params['appserver-name']

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

    def test_basic_appserver_set_settings_result_in_200(self):
        """ Ensure happy path versions of appserver-set settings return 201"""
        params = self.params
        # skipped for now
        #("database", "123456789"),                  # xs:unsignedLong xdmp:database("Documents")
        #("default-user", "123456789"),              # xs:unsignedLong sec:uid-for-name("annabelle")
        #("last-login", "123456789"),                # xs:unsignedLong? 0, (), or xdmp:database("last-login")
        #("modules-database", "123456789"),          # item()  0, "file-system", or xdmp:database("Documents")
        #("privilege", "123456789"),                 # xs:unsignedLong sec:get-privilege("http://marklogic.com/my.uri","execute")
        #("ssl-certificate-template", "123456789"),  # xs:unsignedLong pki:template-get-id(pki:get-template-by-name("mycert"))
        #("ssl-client-certificate-authorities", "#"),# xs:unsignedLong* 
        settings = (
                ("address", "0.0.0.0"),                     # xs:string
                ("authentication", "digestbasic"),          # xs:string
                ("backlog", "64"),                          # xs:unsignedInt
                ("collation", "http://marklogic.com/collation/codepoint"),      # xs:string
                # this setting only exists for webdav app servers
                # ("compute-content-length", "true"),         # xs:boolean
                ("concurrent-request-limit", "128"),        # xs:unsignedInt
                ("debug-allow", "false"),                   # xs:boolean
                ("default-time-limit", "120"),              # xs:unsignedInt
                ("default-xquery-version", "1.0-ml"),       # xs:string
                ("display-last-login", "false"),            # xs:boolean
                ("enabled", "true"),                        # xs:boolean
                ("error-handler", "errorhandler.xqy"),      # xs:string
                ("keep-alive-timeout", "0"),                # xs:unsignedInt
                ("log-errors", "true"),                     # xs:boolean
                ("max-time-limit", "120"),                  # xs:unsignedInt
                # note this name needs to stay the same
                ("name", "test-app-123"),                   # xs:string
                ("output-encoding", "UTF-8"),               # xs:string
                ("output-sgml-character-entities", "none"), # xs:string
                ("port", "8400"),                           # xs:unsignedInt
                ("pre-commit-trigger-depth", "5000"),       # xs:unsignedInt
                ("pre-commit-trigger-limit", "5100"),       # xs:unsignedInt
                ("profile-allow", "false"),                 # xs:boolean
                ("request-timeout", "120"),                 # xs:unsignedInt
                ("root", "Samples/"),                       # xs:string
                ("session-timeout", "1800"),                # xs:unsignedInt
                ("ssl-allow-sslv3", "true"),                # xs:boolean
                ("ssl-allow-tls", "true"),                  # xs:boolean
                ("ssl-ciphers", "All"),                     # xs:string
                ("ssl-hostname", "TestHost"),               # xs:string
                ("ssl-require-client-certificate", "false"),# xs:boolean
                ("static-expires", "3601"),                 # xs:unsignedInt
                ("threads", "128"),                         # xs:unsignedInt
                ("url-rewriter", "rewriter.xqy"),           # xs:string
                )

        for pair in settings:
            params['setting'], params['value'] = pair
            response, body = self.booster.request(params)
            err = response.get("x-booster-error", "none")
            self.assertEqual(response.status, 200)
            self.assertEqual(err, "none")
            # sleep and allow service to restart
            time.sleep(2)

    def test_appserver_set_on_nonexistent_appserver_results_in_404(self):
        """ Attempting set on a non-existent appserver should result in 404 """
        params = self.params
        params['appserver-name'] = "appserver-does-not-exist"
        params['setting'] = "keep-alive-timeout"
        params['value'] = "1"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 404)
        self.assertTrue(err.find("Appserver 'appserver-does-not-exist' does not exist") > -1)

    def test_appserver_set_on_nonexistent_setting_results_in_404(self):
        """ Attempting set on a non-existent setting should result in 404 """
        params = self.params
        params['setting'] = "fake-setting"
        params['value'] = "1"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 404)
        self.assertTrue(err.find("Appserver setting 'fake-setting' does not exist") > -1)

    def test_appserver_set_with_missing_required_parameter_results_in_400(self):
        """ A missing but required parameter should result in 400 """
        params = self.params
        params['setting'] = "keep-alive-timeout"
        params['value'] = "1"
        for rp in ("setting", "value"):
            params2 = params.copy()
            del params2[rp]
            response, body = self.booster.request(params2)
            err = response.get("x-booster-error", "none")
            self.assertEqual(response.status, 400)
            self.assertTrue(err.find("valid set of arguments was not provided") != 1)

    def test_appserver_set_with_empty_required_parameter_results_in_500(self):
        """ An empty but required parameter should result in 500 """
        params = self.params
        params['setting'] = "keep-alive-timeout"
        params['value'] = "1"
        for rp in ("value",):
            params2 = params.copy()
            params2[rp] = ""
            response, body = self.booster.request(params2)
            err = response.get("x-booster-error", "none")
            self.assertEqual(response.status, 500)
            self.assertTrue(err.find("Error running action 'appserver-set'") != -1)
            self.assertTrue(err.find("Error: ") != -1)


if __name__=="__main__":

    unittest.main()
    
