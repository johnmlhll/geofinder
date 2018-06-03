from packages.datatransformation import DataTransformation
import unittest
import coverage
import pandas
import os
import time

cov = coverage.Coverage()  # pragma: no cover
cov.start()  # pragma: no cover


class TestDataTransformation(unittest.TestCase):
    '''
        Test class definition: to test data transformation class for
        correct handling and processing of geo data requests
    '''
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.transform = DataTransformation()
        self.input_latitude = '54.596857'
        self.input_longitude = '-5.950621'
        self.expected_address = '59 Leeson St, Belfast BT12, UK'
        self.input_address = '10 Leeson Street, Dublin 2, Ireland'
        self.input_first_name = 'John'
        self.input_last_name = 'Mulhall'
        self.input_email_address = 'johnmlhll@yahoo.com'
        self.too_many_file = \
            open(os.path.join('data', 'expected_too_manyrecords.csv'))

    def testGeocodeAddress(self):
        '''
            Test method defintion: test method tests the
            actual helper method that calls google's api via
            geopy
        '''
        input_df = pandas.DataFrame(
                            [[self.input_address,
                                self.input_first_name,
                                self.input_last_name,
                                self.input_email_address]],
                            columns=[
                                    'Geo Address',
                                    'First Name',
                                    'Last Name',
                                    'Email Address']
                    )
        expected_single_result = pandas.DataFrame(
                            [[self.input_address,
                                self.input_first_name,
                                self.input_last_name,
                                self.input_email_address,
                                self.input_latitude,
                                self.input_longitude]],
                            columns=[
                                    'Geo Address',
                                    'First Name',
                                    'Last Name',
                                    'Email Address',
                                    'Latitude',
                                    'Longitude']
                    )
        actual_result_df = self.transform.geocode_address(input_df)
        self.assertEqual(len(actual_result_df.columns),
                         len(expected_single_result.columns),
                         msg='Fail - missing latitude/longtitude in result')

    def testProcessFileInputs(self):
        '''
            Test method defintion: test method
            that processes csv file inputs for a valid file input
        '''
        with self.assertRaises(Exception,
                               msg='None file args raised no Exception'):
                self.transform.process_file_inputs(None)
                time.sleep(5)
        with self.assertRaises(Exception,
                               msg='Invalid file args raised no Exception'):
                    self.transform.process_file_inputs('Error')
                    time.sleep(5)

    def testProcessSingleRequest(self):
        '''
            Test method definition: test method that
            processes single address request details
            return geo coordinates  if found
        '''
        with self.assertRaises(Exception,
                               msg='Incorrect datatypes accepted as args'):
            self.transform.process_single_request(1321, 234234, 234234, 234234)
            time.sleep(5)
        with self.assertRaises(Exception,
                               msg='None object accepted as args'):
            self.transform.process_single_request(None)
            time.sleep(5)

    def testGetLocation(self):
        '''
            Test method definition: test method that
            tests the method which returns street address
            from geo coordinates
        '''
        bad_case = self.transform.get_location(
                                            self.input_latitude,
                                            self.input_longitude
                                            )
        time.sleep(1)
        self.assertEqual(self.expected_address, bad_case,
                         msg='Incorrect address returned \
                                            re: lat/long inputs')
        with self.assertRaises(Exception,
                               msg='Incorrect lat/long \
                                            datatype handling error'):
            self.transform.get_location(None, None)
            time.sleep(1)

    def testProcessLocationRequest(self):
        '''
            Test method definition: test method that processes
            geo coordinates and returns an address if found
        '''
        with self.assertRaises(Exception,
                               msg='Incorrect processing of \
                                        lat/long address request'):
                    self.transform.process_location_request(
                                self.input_latitude,
                                self.input_longitude,
                                self.input_first_name,
                                self.too_many_file,
                                self.input_email_address)
        time.sleep(1)
        cov.stop()
        cov.html_report()

    def tearDown(self):
        del self.transform
        self.too_many_file.close()

    @classmethod
    def tearDownClass(cls):
        pass
