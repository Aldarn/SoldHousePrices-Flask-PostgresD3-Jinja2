About
-----

A simple web application designed to ingesting monthly price paid data from the UK government land registry and transform it into a filterable graph of average prices for each property type over time. The data can be found at http://data.gov.uk/dataset/land-registry-monthly-price-paid-data.

Installation
------------

The following third party software will need installing:
	* Python 2.7
	* Postgres
	* Django (developed with 1.6)
	* psycopg2
	* jinja2
	* django_jinja

You will also need a way to run / deploy Django. The following stack was used during development:
	* DigitalOcean (Ubuntu 14.04 x64)
	* Nginx
	* uWSGI
	* virtualenv

Running the Application
-----------------------

* Launch Django
* Navigate to the django host index page
* Enjoy

Tests
-----

To run all the tests, ensure django is setup and running, navigate to the base app directory and run the following:

./manage.py test

Copyright 2015 Benjamin David Holmes, All rights reserved.