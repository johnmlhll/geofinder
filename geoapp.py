from flask import Flask, render_template, request, send_file
from werkzeug import secure_filename  # pragma: no cover
import pandas  # pragma: no cover
import datetime  # pragma: no cover
import os  # pragma: no cover
import logging  # pragma: no cover
from logging.handlers import RotatingFileHandler  # pragma: no cover
from packages.datatransformation import DataTransformation  # pragma: no cover
import unittest  # pragma: no cover
import coverage
from tests.test_geoapp import TestGeoApp  # pragma: no cover
from tests.test_datatransformation import TestDataTransformation
from tests.test_pep8 import TestPep8  # pragma: no cover

# declaration of class objects
transform = DataTransformation()  # pragma: no cover
app = Flask(__name__)  # pragma: no cover


class GeoApp(object):
    """
        Program Defintion V3.0: to upload a csv address file and
        compare to geocoordate returns from the geocoder library
        in Python (API to Google) Program is developed using
        Object Oriented Programming methodologies.
        URL for this application is https://geopath.herokuapp.com/
    """
    # vars
    global filename  # pragma: no cover
    filename = 'geoinfo_results.csv'  # pragma: no cover

    # routing functions
    @app.route('/')
    def geoapp():
        return render_template("home.html")

    @app.route('/result-table', methods=['POST'])
    def result_table():
        if request.method == "POST":
            # file read into memory
            file = request.files['file']
            if file is not None:
                return transform.process_file_inputs(file)
            else:
                return render_template("home.html",
                                       text="System Notice: Zero Results, \
                                       please try again...")

    @app.route('/files-result/')
    def result_file():
        return send_file(filename,
                         attachment_filename='geoinfo_file_%s.csv'
                         % datetime.datetime.now(),
                         as_attachment=True)

    @app.route('/single-result/', methods=['POST'])
    def single_result():
        if request.method == "POST":
            location = request.form["physical_address"]
            given_name = request.form["first_name"]
            family_name = request.form["last_name"]
            email_address = request.form["email"]
            if location != '':
                return transform.process_single_request(location,
                                                        given_name,
                                                        family_name,
                                                        email_address)
            else:
                return render_template("home.html", text="System Notice: \
                Zero Result from Single Search, please try again...")

    @app.route('/single-result/')
    def result_single():
        return send_file(filename,
                         attachment_filename='geoinfo_single_%s.csv'
                         % datetime.datetime.now(),
                         as_attachment=True)

    @app.route('/location/', methods=['GET', 'POST'])
    def location():
        if request.method == 'POST':
            latitude = request.form["lat"]
            longitude = request.form["long"]
            first_name = request.form["f_name"]
            last_name = request.form["l_name"]
            email = request.form["email_add"]
            if longitude != '' and latitude != '':
                return transform.process_location_request(latitude,
                                                          longitude,
                                                          first_name,
                                                          last_name,
                                                          email)
        elif request.method == 'GET':
            return render_template('location.html')
        else:
            return render_template("location.html",
                                   text="Something went wrong \
                                   processing your geo coordinates")

    @app.route('/location-result/')
    def location_result():
        return send_file(filename,
                         attachment_filename='geoinfo_address_%s.csv'
                         % datetime.datetime.now(),
                         as_attachment=True)

    @app.route('/about/')
    def about():
        return render_template("about.html")

if __name__ == "__main__":
    formatter = logging.Formatter("[%(asctime)s] {%(pathname)s: \
                                  %(lineno)d} %(levelname)s - %(message)s")
    handler = RotatingFileHandler(os.path.join('data', 'logs', 'log_info.log'),
                                  maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)  # pragma: no cover
    handler.setFormatter(formatter)  # pragma: no cover
    app.logger.addHandler(handler)  # pragma: no cover
    log = logging.getLogger('werkzeug')  # pragma: no cover
    log.setLevel(logging.DEBUG)  # pragma: no cover
    log.addHandler(handler)  # pragma: no cover
    app.run(debug=True)  # pragma: no cover
    # automated test run
    unittest.main()  # pragma: no cover
