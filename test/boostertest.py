""" boostertest - utilities for functional testing of booster

This module includes test utilities that are common to most of the functional 
tests.  The BoosterTestCase class should be subclassed by most test cases.
The BoosterRequest class allow for performing an http request and receiving 
the http response, in a single line.  

Example test case and booster call >

    class TestGroupCreate(boostertest.BoosterTestCase):

        def test_basic_group_create_results_in_201(self):
            params = {}
            params['action'] = "group-create"
            params['group-name'] = "somegroup"
            response, body = self.booster.request(params)
            self.assertEqual(response.status, 200)


See the functional test modules for more examples.
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


import httplib2
import os
import unittest
import urllib
import urlparse



class BoosterRequest(object):
    """ A utility for managing http requests and responses to booster """

    def __init__(self):
        """ Setup server info for MarkLogic / booster test instance 

        Generally, it is expected that callers will set environment variables 
        in their development / test environment.  These env should point to 
        their own test instance of MarkLogic Server and the booster.xqy module.
        """
        self.debuglevel = os.environ.get("BOOSTER_DEBUG", 0)
        self.scheme = os.environ.get("BOOSTER_SCHEME", "http")
        self.hostname = os.environ.get("BOOSTER_HOST", "localhost")
        self.port = os.environ.get("BOOSTER_PORT", "8001")
        self.username = os.environ.get("BOOSTER_USER", "admin")
        self.password = os.environ.get("BOOSTER_PASS", "password")
        self.netloc = "%s:%s" % (self.hostname, self.port)
        self.booster_path = "booster.xqy"
        urlparts = (self.scheme, self.netloc, self.booster_path, '', '', '')
        self.base_uri = urlparse.urlunparse(urlparts)

    def request(self, parameters={}, custom_headers={}, method="GET"):
        """ Send a request to booster.xqy and return the response and body 
        
        accepts:
           parameters - a dictionary of querystring/form parameters
           custom_headers - a dictionary of http request headers 
           method - an http method
        returns:
            response - the status line and headers (response obj from httplib2)
            body - the contents of the body of the http response
        """
        # set default headers, then integrate/override with those passed in
        headers = {}
        headers['User-Agent'] = "booster test"
        if custom_headers:
            for key, value in custom_headers:
                headers[key] = value
        # setup the querystring/form parameters and related request details
        if parameters:
            encoded_parameters = urllib.urlencode(parameters)
            if method == "POST":
                uri = self.base_uri
                body = encoded_parameters
            else:
                uri = "%s?%s" % (self.base_uri, encoded_parameters)
        else:
            uri = self.base_uri
        # make the request
        httplib2.debuglevel = self.debuglevel
        hconn = httplib2.Http()
        hconn.add_credentials(self.username, self.password)
        response, body = hconn.request(uri, method, headers=headers)
        return response, body


class BoosterTestCase(unittest.TestCase):
    """ A customized TestCase for use in the functional tests """

    def __init__(self, *args, **kwds):
        """ Init TestCase and add custom hooks """
        super(BoosterTestCase, self).__init__(*args, **kwds)
        # allow all tests to make simple booster requests
        #   Ex: response = self.booster.request()
        self.booster = BoosterRequest()


def skiptest(test_function):
    """ For use as a decorator, to skip a test function """
    pass




