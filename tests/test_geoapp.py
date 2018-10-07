import os  # pragma: no cover
import re  # pragma: no cover
import unittest  # pragma: no cover
import tempfile  # pragma: no cover
import pandas  # pragma: no cover
import flask  # pragma: no cover
import coverage  # pragma: no cover
from packages.datatransformation import DataTransformation  # pragma: no cover


class TestGeoApp(unittest.TestCase):
    '''
        Test Class Definition: Tests the GeoApp package class and all
        user defined methods for functional robustness
    '''
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.app = flask.Flask(__name__)

    # targets geoapp.py
    def testHomeStatus(self):
        '''
            Test method definition: tests the home page routing path
        '''
        with self.app.test_request_context('/?name=ScaryMary'):
            assert flask.request.path == '/'
            assert flask.request.args['name'] == 'ScaryMary'

    def testResultsRoute(self):
        '''
            Test method definition: tests the results table view
        '''
        with self.app.test_client() as c:
            results = c.get('/?result=results-table')
            assert flask.request.args['result'] == 'results-table'

    def testLocationRoute(self):
        '''
            Test method defintion: tests the url extension with
            the location view
        '''
        with self.app.test_client() as i:
            results = i.get('/?result=location')
            assert flask.request.args['result'] == 'location'

    def testAboutRoute(self):
        '''
            Test method definition: tests the url extension with
            the about view
        '''
        with self.app.test_client() as a:
            results = a.get('/?result=about')
            assert flask.request.args['result'] == 'about'
        cov.stop()
        cov.html_report()

    def tearDown(self):
        del self.app

    @classmethod
    def tearDownClass(cls):
        pass
