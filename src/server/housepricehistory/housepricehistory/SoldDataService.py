import time
from models import SoldProperty

def getAllAveragePriceData():
	soldProperty = SoldProperty.objects.all().order_by('date')
	dateAverages = {}
	for property in soldProperty:
		propertyDay = time.strftime("%d/%m/%Y")
		if propertyDay in dateAverages:
			if property.type in dateAverages[propertyDay]:
				dateAverages[propertyDay][property.type]["total"] += property.price
				dateAverages[propertyDay][property.type]["count"] += 1
			else:
				dateAverages[propertyDay][property.type]["total"] = property.price
				dateAverages[propertyDay][property.type]["count"] = 1

	data = "Date\tFlats\tTerraced\tDetached\tSemi-Detached\n"
	for date, averages in dateAverages.iteritems():
		data += "%s\t%s\t%s\t%s\t%s\n" % (date, getAverage(averages["F"]), getAverage(averages["T"]),
			getAverage(averages["D"]), getAverage(averages["S"]))

	return data

def getAverage(averageDict):
	return int(float(averageDict["total"]) / float(averageDict["count"]))

def getAveragePriceData(startTimestamp, endTimestamp):
	pass