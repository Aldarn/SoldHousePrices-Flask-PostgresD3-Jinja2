import time
import logging
import datetime
from collections import defaultdict
from ..models import SoldProperty

logger = logging.getLogger(__name__)

def getAllAveragePriceData():
	"""
	Grabs all the properties and calculates the average price of each type on each day.

	TODO: Really these values should be cached, otherwise this would simply be too intensive for the entire data set.
	:return: TSV data.
	"""

	# Get all properties ordered by descending date
	soldProperty = SoldProperty.objects.all().order_by('-date')[:10000]

	# Create a date averages dictionary that defaults to holding prices and counts for different property types on specific days
	dateAverages = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

	# Populate the date averages
	for property in soldProperty:
		propertyDay = int((datetime.datetime.fromtimestamp(property.date).date() - datetime.date(1970, 1, 1)).total_seconds())
		dateAverages[propertyDay][property.type]["total"] += property.price
		dateAverages[propertyDay][property.type]["count"] += 1

	logger.debug("date averages: %s" % dateAverages)

	data = "date\tFlats\tTerraced\tDetached\tSemi-Detached\n"
	for date in sorted(dateAverages):
		averages = dateAverages[date]
		data += "%s\t%s\t%s\t%s\t%s\n" % (datetime.datetime.fromtimestamp(date).strftime("%d/%m/%Y"), _getAverage(averages["F"]), _getAverage(averages["T"]),
			_getAverage(averages["D"]), _getAverage(averages["S"]))

	return data

def _getAverage(averageDict):
	"""
	Gets the average (mean) for the given dictionary containing the total and count.

	:param averageDict: Average dictionary.
	:return: Mean value or 0 if no values in dict.
	"""
	if len(averageDict) == 0:
		return 0
	return int(float(averageDict["total"]) / float(averageDict["count"]))

def getAveragePriceData(startTimestamp, endTimestamp):
	pass
