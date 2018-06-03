import pandas  # pragma: no cover
import numpy  # pragma: no cover
import os  # pragma: no cover
import sys  # pragma: no cover
import re  # pragma: no cover
import coverage  # pragma: no cover
from flask import Flask, render_template, send_file, request, make_response
from geopy.geocoders import Nominatim  # pragma: no cover
from geopy.geocoders import GoogleV3  # pragma: no cover
from urllib.request import Request  # pragma: no cover

# declare class objs/vars
geo_locator = Nominatim()  # pragma: no cover
address_locator = GoogleV3()  # pragma: no cover


class DataTransformation(object):
    '''
        Class Definition: DataTransformation() - to process the
        application's data objects for geocoding
    '''
    def geocode_address(self, df_geodata):
        '''
            Method definition: geo code submitted
            addresses and return long/lat to entry
        '''
        try:
            # vars/objs
            latitude = None
            longitude = None
            df_geodata['Coordinates'] = \
                df_geodata['Geo Address'].apply(geo_locator.geocode)
            df_geodata['Latitude'] = \
                df_geodata['Coordinates']\
                .apply(lambda x: x.latitude if x is not None else None)
            df_geodata['Longitude'] = df_geodata['Coordinates']\
                .apply(lambda x: x.longitude if x is not None else None)
            df_geodata = df_geodata.drop('Coordinates', 1)
            return df_geodata
        except Exception as e:
            err = 'System Notice: Geo coding (geocode_address) \
            process failed. \n API failure returned str null \
            object instead of dataframe geo result'
            return err

    def process_file_inputs(self, file):
        '''
            Method definition: to process the input file's
            data into a dataframe obj
        '''
        try:
            if file is not None:
                df_addresses = pandas.read_csv(file, error_bad_lines=False)
                if len(df_addresses) > 0 and len(df_addresses) < 501:
                    df_addresses['Geo Address'] = df_addresses.iloc[:, 1]\
                                                    .astype(str) + ',' + \
                                                    df_addresses.iloc[:, 2]\
                                                    .astype(str) + ',' + \
                                                    df_addresses.iloc[:, 3]\
                                                    .astype(str) + ',' + \
                                                    df_addresses.iloc[:, 4]\
                                                    .astype(str)
                    df_result = df_addresses[['Last Name',
                                             'Geo Address']].copy()
                    df_result = self.geocode_address(df_result)
                    df_result.to_csv('geoinfo_results.csv', index=None)
                    # limit html display to 500 records
                    df_result = df_result.iloc[:500, :]
                    return render_template('home.html',
                                           text=df_result.to_html(),
                                           btn='files-result.html')
                else:
                    print('System Notice: Illegal Record Count Submitted \
                        - Total: %s' % str(len(df_addresses)))
                    return render_template('home.html',
                                           text='System Notice: File row/record \
                                           count must be from 1 to 500 only. \
                                           Please revise and try again...')
            else:
                raise Exception('File submitted for processing \
                                           was invalid or not found')
        except Exception as e:
            print('System Notice: Something went wrong \
                (process_file_inputs) . \nDetails are: \n%s' % e)
            return render_template('home.html', text='System Notice: \
                Something went wrong with the upload. \
                \nPlease check data entered and try again...')

    def process_single_request(self, physical_address,
                               first_name, last_name, email):
        '''
            Method definition: to process the
            single input form for geo geordinates
        '''
        if first_name == '':
            first_name = 'Not Entered'
        try:
            df_result = pandas.DataFrame([[physical_address, first_name,
                                         last_name, email]],
                                         columns=['Geo Address',
                                                  'First Name', 'Last Name',
                                                  'Email Address'])
            df_result = self.geocode_address(df_result)
            df_result.to_csv('geoinfo_results.csv', index=False)
            return render_template('home.html',
                                   text=df_result.to_html(index=False),
                                   btn='single-result.html')
        except Exception as e:
            print('System Notice: Something went wrong \
                    (process_single_request). \nDetails are: \n%s' % e)
            return render_template('home.html', text='System Notice: \
                    Something went wrong with single entry query. \
                    \nPlease check data entered and try again...')

    # focusing on the Long/Lat returning address service
    def get_location(self, lat, long):
        '''
            Method definition: to use validated geo coodinates
            to get the location address via geopy returned
        '''
        global street_address
        try:
            lat = float(lat)
            long = float(long)
            location = \
                address_locator.reverse('%s, %s' % (str(lat), str(long)))
            if location is not None:
                street_address = str(location[0])
            else:
                street_address = 'None Found | Bad API Call'
            return street_address
        except ValueError as e:
            err = 'System error: Internal error processing lat/long \
                            coordinates as follows \n%s' % ve
            print(err)
            return street_address

    def process_location_request(self, lat, long,
                                 first_name,
                                 last_name, email):
        '''
            Method definition: process long/lat request for address of
            geo location and return it back to the user if found
        '''
        try:
            geo_address = self.get_location(lat, long)
            print(geo_address)
            df_geolocation = pandas.DataFrame([[geo_address,
                                              lat, long, email]],
                                              columns=['Geo Address',
                                                       'Latitude',
                                                       'Longitude',
                                                       'Requestor Email'])
            if df_geolocation is not None:
                df_geolocation.to_csv('geoinfo_results.csv', index=False)
                return render_template('location.html',
                                       text=df_geolocation.
                                       to_html(index=False),
                                       btn='location-result.html')
            else:
                return render_template('location.html',
                                       text='System Notice: Sorry, \
                                       Bad Coordinates')
        except Exception as e:
            print('System Notice: Something went wrong \
                    (process_location_request). \nDetails are: \n%s' % e)
            return render_template('location.html', text='System Notice: \
                    Something went wrong with single entry query. \
                    \nDetail is as follows: \n%s...\
                    \nPlease check data entered and try again...' % e)
