#!/usr/bin/python

#
# Copyright 2015 Benjamin David Holmes, All rights reserved.
#

import subprocess
import os
import re
import sys
from ssh import SSHClient

IGNORE_FILE_TYPES = [".pyc", ".csv"]
BASE_UPLOAD_FROM_DIR = "../src/server/housepricehistory"
BASE_UPLOAD_TO_DIR = "/webapps/property/housepricehistory"
UWSGI_LOCATION = "/webapps/property/housepricehistory/reload"

def inHiddenFolder (path):
	match = re.match(r"^.*/\..+?/.*$", path);
	return match is not None

def restartDjangoServer ():
	client = SSHClient()
	client.load_system_host_keys()
	client.connect("bdholmes.com", username="aldarn")
	stdin, stdout, stderr = client.exec_command("touch " + UWSGI_LOCATION)

	if len(stdout.readlines()) > 0:
		for line in stdout.readlines():
			print line
	else:
		print "Django server restarted!"

def makeDirs (path):
	baseDir = BASE_UPLOAD_TO_DIR
	dirPaths = []
	for dirPath in path.split("/"):
		actualDirPath = os.path.join(baseDir, dirPath)
		dirPaths.append(actualDirPath)
		baseDir = actualDirPath

	if dirPaths is not None and len(dirPaths) > 1:
		del dirPaths[len(dirPaths)-1] # Remove the file name

		client = SSHClient()
		client.load_system_host_keys()
		client.connect("bdholmes.com", username="aldarn")

		for dirPath in dirPaths:
			stdin, stdout, stderr = client.exec_command("mkdir " + dirPath)

			error = False
			for std in [stdout, stderr]:
				if len(std.readlines()) > 0:
					error = True
					for line in std.readlines():
						print line

			if not error:
				print "Created dir " + dirPath + "..."

def main():
	codeOnly = True if len(sys.argv) > 1 and sys.argv[1] == "-c" else False

	for root, subFolders, fileNames in os.walk(BASE_UPLOAD_FROM_DIR):
		for fileName in fileNames:
			filePath = os.path.join(root, fileName)

			if not inHiddenFolder(filePath):
				fileExtension = os.path.splitext(fileName)[1]
				if fileExtension and fileExtension not in IGNORE_FILE_TYPES and (not codeOnly or fileExtension == ".py"):
					relativePathMatch = re.match(r"^" + BASE_UPLOAD_FROM_DIR + r"/(.+?)$", filePath)
					if relativePathMatch:
						makeDirs(relativePathMatch.group(1))

						toFilePath = os.path.join(BASE_UPLOAD_TO_DIR, relativePathMatch.group(1))

						print "Uploading " + filePath + " to " + toFilePath + "..."

						p = subprocess.Popen(["scp", filePath, "aldarn@bdholmes.com:" + toFilePath])
						sts = os.waitpid(p.pid, 0)

	restartDjangoServer();

if __name__ == '__main__':
	main()
