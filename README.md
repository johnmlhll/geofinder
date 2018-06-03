Technical Overview
------------------------

Last Version:               1.0

Current Version:          2.0

Deploy Date:              3rd June 2018

Production url:           https://geopath.herokuapp.com/

Developer Portfolio:  http://jmulhall.azurewebsites.net/


Project GeoPath is a web application that focuses on geo coding services and other API related
services to come. It is from V2.0 providing the following services:

a. Geo coordinates (latitude, longitude) for single query entries based on address in the form of
  e.g. 10 Griffith Avenue, Dublin 9, Ireland

b. Geo coordinates (latitude, longitude) for .csv file query entries for multiple queries up-to
  500 entries in a '.csv' file format of 'lastname, street address, area, city, country'
  e.g. 'Mulhall, 30 Griffith Avenue, Glasnevin, Dublin 9, Ireland'

c. Reverse geo coordinates look up for single query entries only returning addresses from
  latitude and longitude inputs from the user interface form.

In addition to the service, the V2.0 web application also has an 'about' page where you can learn
about the developer (i.e. me) and the purpose of this application.  Currently, there are plans for
a version 3.0 for the following feature implementations:

1. An address return feature base on short wave ham radio call handle supplied running against
    the FCC api where details are made available for all ham radio operators in the USA

2. A top of page icon to make page navigation easier returning to the menu

Please note that this application was developed using geopy Nominatim() and GoogleV3()
classes organizing API contact. Please note that both classes adhere to the terms and conditions
of the API's and may suspend if too many entries are made or repeated over a short period of time.
As I have not yet implemented an account (paid) API key to buy API requests off Google,
please respect this is a free but limited service based upon the free API contacts allowed by
the 3rd party API vendors.

Product Demonstration
----------------------------

Product Trailer:                  https://youtu.be/Wqlj_MzSHJ4

Product Demonstration:     https://youtu.be/mM1bhMSr4eY
