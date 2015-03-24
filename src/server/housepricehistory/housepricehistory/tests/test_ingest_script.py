#!/usr/bin/python2.7

#
# Copyright 2015 Benjamin David Holmes, All rights reserved.
#

import sys
import unittest
import psycopg2
from ..scripts.ingest_data import insertEntries, getFormattedEntry, checkPrintProgress, main as ingestDataMain, DATA_TO_CSV_COLUMN

class TestIngestScript(unittest.TestCase):
	def setUp(self):
		self.db = psycopg2.connect("dbname=housepricehistory_test user=postgres password=fakefake host=localhost")
		self.cursor = self.db.cursor()
		self.cursor.execute("TRUNCATE TABLE housepricehistory_soldproperty;") # Empty the table to begin with

	def tearDown(self):
		self.db.rollback() # Rollback any previously broken changes
		self.cursor.close()
		self.db.close()

	def testInsertEntries(self):
		entries = [
			["uid", 10, 1421712000, "SW12 8ER", "T", False, "L", "paon", "saon", "street", "locality", "town", "district", "county"],
			["uid2", 10, 1421711000, "E3 2QA", "S", False, "L", "paon", "saon", "street", "locality", "town", "district", "county"]
		]
		# -------------------------------------------------------
		insertEntries(self.db, self.cursor, entries)
		# -------------------------------------------------------
		self.assertEqual(len(entries), self._getNumberOfEntriesInDB())

	def testGetFormattedEntry(self):
		entry = ['{A69560CA-94CD-4C29-9B64-116E424EC140}', 117000, '2015-01-12 00:00', 'YO14 9LL', 'F', 'N', 'L', 4, '',
			'NEWTON COURT', '', 'FILEY', 'SCARBOROUGH', 'NORTH YORKSHIRE', 'A']
		# -------------------------------------------------------
		formattedEntry = getFormattedEntry(entry)
		# -------------------------------------------------------
		self.assertEqual(len(formattedEntry), len(DATA_TO_CSV_COLUMN))
		self.assertEqual(formattedEntry[0], 'A69560CA-94CD-4C29-9B64-116E424EC140')
		self.assertEqual(formattedEntry[2], 1421020800)

	def testCheckPrintProgress(self):
		stdout = sys.stdout
		sys.stdout = TestStdout()
		# -------------------------------------------------------
		checkPrintProgress(5, 10)
		# -------------------------------------------------------
		sys.stdout = stdout
		self.assertTrue("50% COMPLETE" in TestStdout.written)

	def testMain(self):
		# -------------------------------------------------------
		ingestDataMain("/webapps/property/housepricehistory/data/test_data.csv", self.db, self.cursor)
		# -------------------------------------------------------
		self.assertEqual(3, self._getNumberOfEntriesInDB())

	def _getNumberOfEntriesInDB(self):
		self.cursor.execute("SELECT * FROM housepricehistory_soldproperty;")
		return len(self.cursor.fetchall())

class TestStdout(object):
	"""
	Used to swallow stdout whilst testing.
	"""
	written = ""
	def write(self, s):
		TestStdout.written += s

def main():
	unittest.main()

if __name__ == '__main__':
	main()
