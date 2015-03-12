#!/usr/bin/python

import subprocess
import os
import re
from ssh import SSHClient

def inHiddenFolder (path):
	match = re.match(r"^.*/\..+?/.*$", path);
	if match is None:
		return False
	return True

def restartDjangoServer ():
	UWSGI_LOCATION = "/webapps/property/housepricehistory/reload"

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
	dirPaths = [os.path.join(BASE_UPLOAD_TO_DIR, dirPath) for dirPath in path.split("/")]

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

BASE_UPLOAD_FROM_DIR = "../src/server/"
BASE_UPLOAD_TO_DIR = "~/webapps/property/housepricehistory/housepricehistory"

for root, subFolders, fileNames in os.walk(BASE_UPLOAD_FROM_DIR):
	for fileName in fileNames:
		filePath = os.path.join(root, fileName)

		if not inHiddenFolder(filePath):
			if os.path.splitext(fileName)[1]:
				relativePathMatch = re.match(r"^" + BASE_UPLOAD_FROM_DIR + r"/(.+?)$", filePath)
				if relativePathMatch:
					makeDirs(relativePathMatch.group(1))

					toFilePath = os.path.join(BASE_UPLOAD_TO_DIR, relativePathMatch.group(1))

					print "Uploading " + filePath + " to " + toFilePath + "..."

					p = subprocess.Popen(["scp", filePath, "aldarn@bdholmes.com:" + toFilePath])
					sts = os.waitpid(p.pid, 0)

restartDjangoServer();
