import unittest
import coverage
import pep8
import os
import re


class TestPep8(unittest.TestCase):
    '''
        Test class definition: test pep8 coverage on the geoapp project
     '''
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def testPep8Coverage(self):
        # arrange objects
        check = None
        styleAudit = pep8.StyleGuide(quiet=False,
                                     exclude=['*/vm/*',
                                              '*/data/*'])
        file_list = os.listdir('.')
        for filename in file_list:
            if re.match('__pycache__', str(filename)):
                continue
            elif re.search('.py', str(filename)):
                check = styleAudit.check_files(filename)
            else:
                continue
        # assert 8 errors anything above that is valid
        self.assertEqual(check.total_errors, 8,
                         "Found valid Pep8 code errors - See Above")

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass
