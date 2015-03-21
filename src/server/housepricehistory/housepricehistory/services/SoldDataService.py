import time
import logging
import getpass
from collections import defaultdict
from ..models import SoldProperty

logger = logging.getLogger(__name__)

def getAllAveragePriceData():
	# Get all properties ordered by descending date
	soldProperty = SoldProperty.objects.all().order_by('-date')[:1]

	# Create a date averages dictionary that defaults to holding prices and counts for different property types on specific days
	dateAverages = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

	# Populate the date averages
	for property in soldProperty:
		propertyDay = time.strftime("%d/%m/%Y")
		dateAverages[propertyDay][property.type]["total"] += property.price
		dateAverages[propertyDay][property.type]["count"] += 1

	logger.debug("date averages: %s" % dateAverages)

	data = "Date\tFlats\tTerraced\tDetached\tSemi-Detached\n"
	for date, averages in dateAverages.iteritems():
		data += "%s\t%s\t%s\t%s\t%s\n" % (date, _getAverage(averages["F"]), _getAverage(averages["T"]),
			_getAverage(averages["D"]), _getAverage(averages["S"]))

	return data

def _getAverage(averageDict):
	# Should dates with no data be blank instead of 0?
	if len(averageDict) == 0:
		return 0
	return int(float(averageDict["total"]) / float(averageDict["count"]))

def getAveragePriceData(startTimestamp, endTimestamp):
	pass
