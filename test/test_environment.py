#!/usr/bin/env python


import unittest

import boostertest


class TestEnvironment(boostertest.BoosterTestCase):
    """ Test the functional testing environment
    
    This is a simple test case for confirming the test environment is in 
    working order.  If it fails, here are things that could be wrong:
        * test host cannot make connection to MarkLogic server
        * MarkLogic Server test instance is not running
        * booster.xqy file has not been placed in MarkLogic app server root
        * environment variables are not set or are incorrect
        * ...
    """

    def test_environment_with_basic_booster_call(self):
        """ A call with no parameters should return a 400 """
        self.booster.debuglevel = 1
        response, body = self.booster.request()
        self.assertEqual(response.status, 400)


if __name__=="__main__":

    unittest.main()


