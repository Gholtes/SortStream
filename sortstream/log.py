import csv
import os
from datetime import datetime


def YYYYMMDDHMS():
    return datetime.now().strftime("%Y%m%d_%H-%M-%S")

def saveLogs(array, filename = "logs", appPath = ".", saveLoc = "logs", verbose = False):
	home = os.listdir(appPath)
	if not saveLoc in home:
		os.mkdir(os.path.join(appPath, saveLoc))

	filename += "_" + YYYYMMDDHMS() + ".csv"

	with open(os.path.join(appPath, saveLoc, filename), "w", newline="") as csvfile:
		writer = csv.writer(csvfile)
		for row in array:
			writer.writerow(row)
		if verbose:
			print("logfile {0} saved at {1}".format(filename, os.path.join(appPath, saveLoc, filename)))
