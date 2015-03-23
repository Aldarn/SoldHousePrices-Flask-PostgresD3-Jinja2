#!/usr/bin/python2.7

from django.utils import unittest
from django.test import TestCase
from ..housepricehistory.services.SoldDataService import getAveragePriceData, \
	_createDataTSVFromAverages, _getTSVDataLine

class TestSoldDataService(TestCase):
	def testGetAveragePriceData(self):
		startDate = "01-01-2015"
		endDate = "01-02-2015"
		postCode = None
		# -------------------------------------------------------
		data = getAveragePriceData(startDate, endDate, postCode)
		# -------------------------------------------------------
		self.assertTrue("date\tFlats\tTerraced\tDetached\tSemi-Detached" in data)

	def testGetAveragePriceDataNoResults(self):
		startDate = "01-01-2030"
		endDate = "01-02-2030"
		postCode = None
		# -------------------------------------------------------
		data = getAveragePriceData(startDate, endDate, postCode)
		# -------------------------------------------------------
		self.assertFalse("date\tFlats\tTerraced\tDetached\tSemi-Detached" in data)

	def testGetAveragePriceDataInvalidStartDate(self):
		startDate = "fake fake fake"
		endDate = "01-01-2015"
		postCode = None
		# -------------------------------------------------------
		data = getAveragePriceData(startDate, endDate, postCode)
		# -------------------------------------------------------
		self.assertFalse("date\tFlats\tTerraced\tDetached\tSemi-Detached" in data)

	def testGetAveragePriceDataEndDateBeforeStartDate(self):
		startDate = "02-02-2015"
		endDate = "01-01-2015"
		postCode = None
		# -------------------------------------------------------
		data = getAveragePriceData(startDate, endDate, postCode)
		# -------------------------------------------------------
		self.assertFalse("date\tFlats\tTerraced\tDetached\tSemi-Detached" in data)

	def testCreateDataTSVFromAverages(self):
		averages = [
			{"date": "2015-02-01", "type": "D", "average": 40000},
			{"date": "2015-02-01", "type": "S", "average": 30000},
			{"date": "2015-02-01", "type": "F", "average": 10000},
			{"date": "2015-02-01", "type": "T", "average": 20000},
			{"date": "2015-02-02", "type": "D", "average": 100000},
			{"date": "2015-02-02", "type": "F", "average": 500},
			{"date": "2015-02-03", "type": "S", "average": 999},
			{"date": "2015-02-03", "type": "T", "average": 888},
			{"date": "2015-02-03", "type": "F", "average": 777}
		]
		# -------------------------------------------------------
		data = _createDataTSVFromAverages(averages)
		# -------------------------------------------------------
		self.assertEqual("date\tFlats\tTerraced\tDetached\tSemi-Detached"
			"\n2015-02-01\t10000\t20000\t40000\t30000"
			"\n2015-02-02\t500\t0\t100000\t0"
			"\n2015-02-03\t777\t888\t0\t999", data)

	def testGetTSVDataLine(self):
		date = "2015-02-01"
		typeAverages = {"F": 10000, "T": 20000, "D": 40000, "S": 30000}
		# -------------------------------------------------------
		tsvDataLine = _getTSVDataLine(date, typeAverages)
		# -------------------------------------------------------
		self.assertEqual("\n2015-02-01\t10000\t20000\t40000\t30000", tsvDataLine)

def main():
	unittest.main()

if __name__ == '__main__':
	main()