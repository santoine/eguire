""" Episode guide reminder """

import urllib
import csv
import re
import episode

ALL_SHOWS_URL = "http://www.epguides.com/common/allshows.txt"
CSV_FILENAME = "allShows.csv"
MY_SHOWS_FILENAME = "myShows"
EMPTY_END_DATE = "___ ____"
# indexes for the CSV files
title, directory, tvrage, start_date, end_date, number_of_episodes, run_time, network, country = range(0,9)
titles = "title", "directory", "tvrage", "start_date", "end_date", "number_of_episodes", "run_time", "network", "country"

""" Imports list of shows from epguides.com to a CSV file"""
def downloadShowsToCSV(filename= CSV_FILENAME, url=ALL_SHOWS_URL):
	filehandler = urllib.urlopen(url)
	filereader = csv.reader(filehandler, delimiter=',',quotechar='"')
	with open(filename, 'wb') as csvfile:
		showwriter =csv.writer(csvfile)	
		#indexes are set to remove the first row (title) and the last row (empty element)
		# for row in list(filereader)[1:-1]:
		for row in tuple(filereader)[1:-1]:
			showwriter.writerow(row)
	return filename

""" Imports the list of shows from the csv file"""
def loadShows(filename=CSV_FILENAME):
	f = None
	try:
		f =  open(filename, 'rb')
	except IOError:
		f = open(downloadShowsToCSV(filename), 'rb')
	filereader = csv.reader(f, delimiter=',',quotechar='"')
	# index are used to remove the titles (first line) and an empty line (last line)
	return tuple(filereader)[1:-1]
			
""" Finds a show in the shows list """
def find(regexTitle, shows=loadShows()):
	prog = re.compile(regexTitle)
	showsFound = [show for show in shows if prog.match(show[title])]	
	if len(showsFound) == 1:
		return showsFound[0]
	elif len(showsFound) > 1:
		return showsFound
	else:
		return None 

""" Prints the definition of the show. 
    The following argument allows to display elements of the show description as title, tvrage,..."""
def printShow(show, *showElements):	
	if showElements :
		for showElement in showElements:
			print titles[showElement] + " : " + show[showElement]
	else:
		for i, s in enumerate(show):
			print titles[i] + " : " + s

""" Selects the shows still running"""
def runningShows(shows=loadShows()):
	return [show for show in shows if show[end_date] == EMPTY_END_DATE]

# downloadShowsToCSV()
# printShow(find(".*X-Files"))
shows = loadShows()
printShow(shows)
# for show in runningShows() : 
# 	# printShow(show)
# 	printShow(show, title, tvrage)


# print episode.find(find(".*X-Files"))