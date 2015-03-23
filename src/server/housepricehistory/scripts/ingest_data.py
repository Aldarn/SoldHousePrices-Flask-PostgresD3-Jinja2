#!/usr/bin/python

import psycopg2
import time
import datetime
import csv
from itertools import chain

DATA_TO_CSV_COLUMN = {
	"uid": 0,
	"price": 1,
	"date": 2,
	"postcode": 3,
	"type": 4, # D = Detached, S = Semi-Detached, T = Terraced, F = Flats/Maisonettes
	"isold": 5, # Y = a newly built property, N = an established residential building
	"duration": 6, # Relates to the tenure: F = Freehold, L-Leasehold etc.
	"paon": 7, # Primary Addressable Object Name. If there is a sub-building for example the building is divided into flats, see Secondary Addressable Object Name (SAON).
	"saon": 8, # Secondary Addressable Object Name. If there is a sub-building, for example the building is divided into flats, there will be a SAON.
	"street": 9,
	"locality": 10,
	"town": 11,
	"district": 12,
	"county": 13
}

def insertEntries(db, cursor, entries):
	"""
	Inserts a batch of entries.
	:param entries: List of entry insert SQLs.
	"""
	# Get the columns to use in the correct order
	columns = ", ".join(sorted(DATA_TO_CSV_COLUMN, key = lambda k: DATA_TO_CSV_COLUMN[k]))

	# Create the prepared statement
	insertSql = "INSERT INTO housepricehistory_soldproperty (%s) VALUES %s;" % (columns,
		("(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s), " * len(entries))[:-2])

	# Execute with all entry data unpacked
	cursor.execute(insertSql, tuple(chain(*entries)))
	db.commit()

def getFormattedEntry(entry):
	"""
	Converts the entry into a list of values and formats each where necessary.
	:param entry: The entry in the data file to format.
	:return: Formatted list of entry values.
	"""
	# Remove braces from the uid
	entry[DATA_TO_CSV_COLUMN["uid"]] = entry[DATA_TO_CSV_COLUMN["uid"]].replace('{', '').replace('}', '')

	# Convert the date into a timestamp
	entry[DATA_TO_CSV_COLUMN["date"]] = int(time.mktime(datetime.datetime.strptime(entry[DATA_TO_CSV_COLUMN["date"]],
		"%Y-%m-%d %H:%M").timetuple()))

	# Remove record status if it exists
	if len(entry) > len(DATA_TO_CSV_COLUMN):
		del entry[-1]

	return entry

def checkPrintProgress(currentCount, total):
	"""
	Prints a progress report for each percentage completed.
	:param currentCount: The current number of entries added.
	:param total: The total number of entries to add.
	"""
	if currentCount == 0:
		return

	previousPercentageComplete = int(((float(currentCount - 1) / float(total)) * 100.0))
	percentageComplete = int(((float(currentCount) / float(total)) * 100.0))
	if previousPercentageComplete < percentageComplete:
		message = str(percentageComplete) + '% COMPLETE'
		print '\n' + '***** ' * 10
		print message.rjust(30 + len(message) / 2)
		print '***** ' * 10 + '\n'

def main(dataFile = "../data/feb_2015_sold_data.csv"):
	db = psycopg2.connect("dbname=housepricehistory user=postgres password=fakefake host=localhost")
	cursor = db.cursor()

	with open(dataFile, 'r') as fileHandle:
		processedCount = 0
		totalEntries = 83245
		currentEntries = []

		# CSV module will split each line of data correctly and remove field quotes
		for entry in csv.reader(fileHandle):
			checkPrintProgress(processedCount, totalEntries)
			processedCount += 1

			currentEntries.append(getFormattedEntry(entry))

			# TODO: Replace arbitrary insert count with a check for the maximum insert sql length
			if len(currentEntries) == 1:
				insertEntries(db, cursor, currentEntries)
				del currentEntries[:]

	cursor.close()
	db.close()

if __name__ == '__main__':
	main()
