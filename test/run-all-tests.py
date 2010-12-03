#!/usr/bin/env python
""" run-all-tests.py - run all of the functional tests for booster

This is a simple shell script for running all of the booster functional tests 
in a roughly random order.  The order of the test modules will be randomized 
and the order of the tests in each module will be randomized.  The output will
show one test (and result) per line.
"""

""" 
Copyright 2010 Cody Collier

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import unittest 
import random


if __name__=="__main__":
  
    all_modules = ("test_boundaries.py",
        "test_appserver_create_http.py", "test_appserver_create_webdav.py",
        "test_appserver_create_xdbc.py", "test_appserver_delete.py",
        "test_database_create.py", "test_database_delete.py",
        "test_database_forest.py", "test_database_set.py",
        "test_forest_create.py", "test_forest_delete.py",
        "test_group_create.py", "test_group_delete.py",
        "test_group_set.py", "test_host_edit.py",
        "test_user_create.py", "test_user_delete.py",)

    # create a master_suite of test module suites
    master_suite = unittest.TestSuite()
    for test_module_name in all_modules:
        # import module
        test_module = __import__(test_module_name)
        # create a suite from the module
        suite = unittest.TestLoader().loadTestsFromModule(test_module)
        master_suite.addTests(suite)

    # randomize the order of the test modules
    random.shuffle(master_suite._tests)
    # randomize the order of the tests inside each module
    for suite in master_suite._tests:
        random.shuffle(suite._tests)

    # run the randomized tests
    unittest.TextTestRunner(verbosity=2).run(master_suite)
