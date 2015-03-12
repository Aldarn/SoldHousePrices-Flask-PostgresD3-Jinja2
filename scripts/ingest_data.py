#!/usr/bin/python

DATA_TO_CSV_COLUMN = {
	"uid": 0,
	"price": 1,
	"date": 2,
	"postCode": 3,
	"type": 4, # D = Detached, S = Semi-Detached, T = Terraced, F = Flats/Maisonettes
	"isOld": 5, # Y = a newly built property, N = an established residential building
	"duration": 6, # Relates to the tenure: F = Freehold, L-Leasehold etc.
	"paon": 7, # Primary Addressable Object Name. If there is a sub-building for example the building is divided into flats, see Secondary Addressable Object Name (SAON).
	"saon": 8, # Secondary Addressable Object Name. If there is a sub-building, for example the building is divided into flats, there will be a SAON.
	"street": 9,
	"locality": 10,
	"town": 11,
	"district": 12,
	"county": 13
}

def insertEntries(entries):
	"""
	Inserts a batch of entries.
	:param entries: List of entry insert SQLs.
	"""
	# TODO: Concat the sql's
	# TODO: Run the sql
	# TODO: Commit it
	pass

def getDataEntryInsertSQL(entry):
	"""
	Gets the insert SQL for an entry.
	:param entry: The entry to get the SQL for.
	:return: The insert SQL for the entry.
	"""
	entryData = entry.split(",")
	return """INSERT INTO sold_property ('id', '%s')
		   VALUES ('', '%s')""" \
		   % ("', '".join(DATA_TO_CSV_COLUMN.keys()), "', '".join([entryData[i] for i in DATA_TO_CSV_COLUMN.values()]))

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

def main():
	with open("../full_sold_data.csv", 'r') as fileHandle:
		processedCount = 0
		totalEntries = x
		currentInserts = []
		for entry in fileHandle:
			checkPrintProgress(processedCount, totalEntries)
			currentInserts.append(getDataEntryInsertSQL(entry))

			# TODO: Replace arbitrary insert count with a check for the maximum insert sql length
			if len(currentInserts) == 100:
				insertEntries(currentInserts)
				del currentInserts[:]

if __name__ == '__main__':
	main()
