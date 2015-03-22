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

	return _createDataTSVFromAverages(_dictFetchAll(cursor))

def getAveragePriceData(startDate, endDate):
	"""
	Grabs all the properties inclusively between the given start and end timestamps and returns the average price of each type for
	each day in TSV format.

	TODO: Caching date averages in the database (or e.g. Redis) would improve performance.

	:param startDate: Start date.
	:param endDate: End date.
	:return: TSV data.
	"""
	# Convert dates to timestamps
	start = int(time.mktime(datetime.datetime.strptime(startDate, "%d-%m-%Y").timetuple()))
	end = int(time.mktime(datetime.datetime.strptime(endDate, "%d-%m-%Y").timetuple())) + 86400

	# Run the query to get the averages for each type on each day between the start and end timestamps
	cursor = connection.cursor()
	cursor.execute("SELECT AVG(price) AS average, type, date(to_timestamp(date)) AS date FROM housepricehistory_soldproperty "
				   "WHERE date >= %s AND date < %s GROUP BY date, type ORDER BY date", [start, end])

	return _createDataTSVFromAverages(_dictFetchAll(cursor))

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

############
# Old Code #
############

def __getDailyValues(properties):
	"""
	Gets the total sold price value and count for each type of property for each day.

	:param properties: The property objects.
	:return: Nested dictionary of property week:property type:total/count.
	"""
	# Create a date averages dictionary that defaults to holding prices and counts for different property types for each day
	dateAverages = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

	# Populate the date averages
	for property in properties:
		propertyDay = int((datetime.datetime.fromtimestamp(property.date).date() - datetime.date(1970, 1, 1)).total_seconds())
		dateAverages[propertyDay][property.type]["total"] += property.price
		dateAverages[propertyDay][property.type]["count"] += 1

	return dateAverages

def __createDataTSV(dailyValues):
	"""
	Creates TSV data for the given daily values.

	:param dailyValues: The daily values to create the data from.
	:return: TSV data.
	"""
	data = "date\tFlats\tTerraced\tDetached\tSemi-Detached\n"
	for date in sorted(dailyValues):
		averages = dailyValues[date]
		data += "%s\t%s\t%s\t%s\t%s\n" % (datetime.datetime.fromtimestamp(date).strftime("%d/%m/%Y"), __getAverage(averages["F"]), __getAverage(averages["T"]),
			__getAverage(averages["D"]), __getAverage(averages["S"]))

	return data

def __getAverage(averageDict):
	"""
	Gets the average (mean) for the given dictionary containing the total and count.

	:param averageDict: Average dictionary.
	:return: Mean value or 0 if no values in dict.
	"""
	if len(averageDict) == 0:
		return 0
	return int(float(averageDict["total"]) / float(averageDict["count"]))
