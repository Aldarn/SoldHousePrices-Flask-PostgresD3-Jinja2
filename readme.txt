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

To run all the tests, execute nosetests from a command line interface when the
current directory is the same as the one this file is in.
