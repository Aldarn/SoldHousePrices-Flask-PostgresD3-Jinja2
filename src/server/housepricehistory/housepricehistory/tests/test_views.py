#!/usr/bin/python2.7

#
# Copyright 2015 Benjamin David Holmes, All rights reserved.
#

from django.utils import unittest
from django.test import TestCase
from ..views import averagePrices

class TestViews(TestCase):
	fixtures = ['test_data.json']

	def testAveragePrices(self):
		request = MockRequest({}, 'GET')
		# -------------------------------------------------------
		response = averagePrices(request)
		# -------------------------------------------------------
		self.assertTrue("date\tFlats\tTerraced\tDetached\tSemi-Detached" in response.content)

	def testAveragePricesWithFilters(self):
		request = MockRequest({"start": "01-01-2014", "end": "01-02-2015", "postCode": "SW12"}, 'GET')
		# -------------------------------------------------------
		response = averagePrices(request)
		# -------------------------------------------------------
		self.assertTrue("date\tFlats\tTerraced\tDetached\tSemi-Detached" in response.content)

class MockRequest(object):
	def __init__(self, GET, method):
		self.GET = GET
		self.method = method

def main():
	unittest.main()

if __name__ == '__main__':
	main()