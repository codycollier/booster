#!/usr/bin/env python


import unittest

import boostertest


class TestDatabaseSet(boostertest.BoosterTestCase):
    """ Test the database-set* action """

    def setUp(self):
        """ Create common database and params """
        # create test database
        params = {}
        params['action'] = "database-create"
        params['database-name'] = "zerodb"
        params['security-db-name'] = "Security"
        params['schema-db-name'] = "Schemas"
        response, body = self.booster.request(params)
        self.assertTrue(response.status in (201,409))
        # collect db names for later teardown
        self.teardown_databases = []
        self.teardown_databases.append(params['database-name'])
        # common params
        self.params = {}
        self.params['action'] = "database-set"
        self.params['database-name'] = params['database-name']

    def tearDown(self):
        """ Remove items from server created during tests """
        params = {}
        params['action'] = "database-delete"
        for database in self.teardown_databases:
            params['database-name'] = database
            response, body = self.booster.request(params)
            self.assertTrue(response.status in (404, 200))

    def test_basic_database_set_settings_result_in_200(self):
        """ Ensure happy path versions of database-set settings return 201"""
        params = self.params
        settings = (
            ("attribute-value-positions", "true"),              #xs:boolean
            ("collection-lexicon", "true"),                     #xs:boolean
            ("directory-creation", "automatic"),                #xs:string
            ("element-value-positions", "true"),                #xs:boolean
            ("element-word-positions", "true"),                 #xs:boolean
            ("enabled", "true"),                                #xs:boolean
            ("expunge-locks", "automatic"),                     #xs:string
            ("fast-case-sensitive-searches", "true"),           #xs:boolean
            ("fast-diacritic-sensitive-searches", "true"),      #xs:boolean
            ("fast-element-character-searches", "true"),        #xs:boolean
            ("fast-element-phrase-searches", "true"),           #xs:boolean
            ("fast-element-trailing-wildcard-searches", "true"),#xs:boolean
            ("fast-element-word-searches", "true"),             #xs:boolean
            ("fast-phrase-searches", "true"),                   #xs:boolean
            ("fast-reverse-searches", "true"),                  #xs:boolean
            ("format-compatibility", "automatic"),              #xs:string
            ("in-memory-limit", "10000"),                       #xs:unsignedInt
            ("in-memory-list-size", "256"),                     #xs:unsignedInt
            ("in-memory-range-index-size", "10"),               #xs:unsignedInt
            ("in-memory-reverse-index-size", "5"),              #xs:unsignedInt
            ("in-memory-tree-size", "256"),                     #xs:unsignedInt
            ("index-detection", "automatic"),                   #xs:string
            ("inherit-collections", "true"),                    #xs:boolean
            ("inherit-permissions", "true"),                    #xs:boolean
            ("inherit-quality", "true"),                        #xs:boolean
            ("journal-size", "256"),                            #xs:unsignedInt
            ("journaling", "strict"),                           #xs:string
            ("language", "es"),                                 #xs:string
            ("locking", "strict"),                              #xs:string
            ("maintain-directory-last-modified", "false"),      #xs:boolean
            ("maintain-last-modified", "false"),                #xs:boolean
            ("merge-enable", "true"),                           #xs:boolean
            ("merge-max-size", "512"),                          #xs:unsignedInt
            ("merge-min-ratio", "3"),                           #xs:unsignedInt
            ("merge-min-size", "100"),                          #xs:unsignedInt
            ("merge-priority", "normal"),                       #xs:string
            ("merge-timestamp", "0"),                           #xs:unsignedLong
            ("name", "zerodb"),                                 #xs:string
            ("one-character-searches", "true"),                 #xs:boolean
            ("positions-list-max-size", "128"),                 #xs:unsignedInt
            ("preallocate-journals", "true"),                   #xs:boolean
            ("preload-mapped-data", "true"),                    #xs:boolean
            ("range-index-optimize", "memory-size"),            #xs:string
            ("reindexer-enable", "true"),                       #xs:boolean
            ("reindexer-throttle", "3"),                        #xs:unsignedInt
            ("reindexer-timestamp", "0"),                       #xs:unsignedInt
            ("stemmed-searches", "decompounding"),              #xs:string
            ("three-character-searches", "true"),               #xs:boolean
            ("three-character-word-positions", "true"),         #xs:boolean
            ("trailing-wildcard-searches", "true"),             #xs:boolean
            ("trailing-wildcard-word-positions", "true"),       #xs:boolean
            ("two-character-searches", "true"),                 #xs:boolean
            ("uri-lexicon", "true"),                            #xs:boolean
            ("word-positions", "true"),                         #xs:boolean
            ("word-searches", "true"),                          #xs:boolean
            )
        for pair in settings:
            params['setting'], params['value'] = pair
            response, body = self.booster.request(params)
            err = response.get("x-booster-error", "none")
            self.assertEqual(response.status, 200)
            self.assertEqual(err, "none")

    def test_database_set_on_nonexistent_database_results_in_404(self):
        """ Attempting set on a non-existent database should result in 404 """
        params = self.params
        params['database-name'] = "db-does-not-exist"
        params['setting'] = "attribute-value-positions"
        params['value'] = "true"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 404)
        self.assertTrue(err.find("Database 'db-does-not-exist' does not exist") > -1)

    def test_database_set_on_nonexistent_setting_results_in_404(self):
        """ Attempting set on a non-existent setting should result in 404 """
        params = self.params
        params['setting'] = "batmans-cape"
        params['value'] = "black"
        response, body = self.booster.request(params)
        err = response.get("x-booster-error", "none")
        self.assertEqual(response.status, 404)
        self.assertTrue(err.find("Database setting 'batmans-cape' does not exist") > -1)

    def test_database_set_with_missing_required_parameter_results_in_400(self):
        """ A missing but required parameter should result in 400 """
        params = self.params
        params['setting'] = "attribute-value-positions"
        params['value'] = "true"
        for rp in ("setting", "value"):
            params2 = params.copy()
            del params2[rp]
            response, body = self.booster.request(params2)
            err = response.get("x-booster-error", "none")
            self.assertEqual(response.status, 400)
            self.assertTrue(err.find("valid set of arguments was not provided") != 1)

    def test_database_set_with_empty_required_parameter_results_in_500(self):
        """ An empty but required parameter should result in 500 """
        params = self.params
        params['setting'] = "attribute-value-positions"
        params['value'] = "true"
        for rp in ("value",):
            params2 = params.copy()
            params2[rp] = ""
            response, body = self.booster.request(params2)
            err = response.get("x-booster-error", "none")
            self.assertEqual(response.status, 500)
            self.assertTrue(err.find("Error running action 'database-set'") != -1)
            self.assertTrue(err.find("Error: ") != -1)


if __name__=="__main__":

    unittest.main()
    
