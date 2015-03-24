#
# Copyright 2015 Benjamin David Holmes, All rights reserved.
#

import logging
import time
import datetime
from collections import defaultdict
from django.db import connection

logger = logging.getLogger(__name__)

def getAllAveragePriceData():
	"""
	Grabs all the properties and returns the average price of each type for each day in TSV format.

	TODO: Caching date averages in the database (or e.g. Redis) would improve performance.

	:return: TSV data.
	"""
	# Run the query to get the averages for each type on each day between the start and end timestamps
	cursor = connection.cursor()
	cursor.execute("SELECT AVG(price) AS average, type, date(to_timestamp(date)) AS date FROM housepricehistory_soldproperty "
				   "GROUP BY date, type ORDER BY date")

	averages = _dictFetchAll(cursor)
	if len(averages) == 0:
		return "No results."

	return _createDataTSVFromAverages(averages)

def getAveragePriceData(startDate, endDate, postCode):
	"""
	Grabs all the properties inclusively between the given start and end timestamps and returns the average price of each type for
	each day in TSV format.

	TODO: Caching date averages in the database (or e.g. Redis) would improve performance.

	:param startDate: Start date.
	:param endDate: End date.
	:return: TSV data.
	"""
	# Convert dates to timestamps
	try:
		start = int(time.mktime(datetime.datetime.strptime(startDate, "%d-%m-%Y").timetuple()))
		end = int(time.mktime(datetime.datetime.strptime(endDate, "%d-%m-%Y").timetuple())) + 86400
	except ValueError, ve:
		logger.debug("Error parsing start and end dates: %s" % ve)
		return "Invalid start or end date."

	if start >= end:
		return "Start date must be before end date."

	# Run the query to get the averages for each type on each day between the start and end timestamps
	cursor = connection.cursor()

	if postCode is not None:
		cursor.execute("SELECT AVG(price) AS average, type, date(to_timestamp(date)) AS date FROM housepricehistory_soldproperty "
			"WHERE date >= %s AND date < %s AND postcode LIKE %s GROUP BY date, type ORDER BY date", [start, end, '%s%%' % postCode])
	else:
		cursor.execute("SELECT AVG(price) AS average, type, date(to_timestamp(date)) AS date FROM housepricehistory_soldproperty "
			"WHERE date >= %s AND date < %s GROUP BY date, type ORDER BY date", [start, end])

	averages = _dictFetchAll(cursor)
	if len(averages) == 0:
		return "No results."

	return _createDataTSVFromAverages(averages)

def _createDataTSVFromAverages(averages):
	"""
	Creates TSV data from the property type daily averages.

	:param averages: Property type daily averages.
	:return: TSV data.
	"""
	data = "date\tFlats\tTerraced\tDetached\tSemi-Detached"
	currentDate = averages[0]["date"]
	typeAverages = defaultdict(int)

	# Loop each average and group them into data lines by date
	for average in averages:
		averageDate = average["date"]
		if currentDate != averageDate:
			data += _getTSVDataLine(currentDate, typeAverages)
			currentDate = averageDate
			typeAverages.clear()
		typeAverages[average["type"]] = average["average"]

	# Don't forget the last date
	data += _getTSVDataLine(currentDate, typeAverages)

	return data

def _getTSVDataLine(date, typeAverages):
	"""
	Creates one line of the TSV.

	:param date: The date of the entry.
	:param typeAverages: The averages for each property type on this date.
	:return: String TSV line.
	"""
	return "\n%s\t%s\t%s\t%s\t%s" % (date, typeAverages["F"], typeAverages["T"], typeAverages["D"], typeAverages["S"])

def _dictFetchAll(cursor):
	"""
	Creates a dictionary of column:value from the results of a raw query.

	:param cursor: Database cursor.
	:return: Dictionary column:value.
	"""
	desc = cursor.description
	return [
		dict(zip([col[0] for col in desc], row))
		for row in cursor.fetchall()
	]
