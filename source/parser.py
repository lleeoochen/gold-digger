from bs4 import BeautifulSoup
import os
import csv
import time
import datetime

#returns list of files in the directory
def getAllFiles(dir):
	files = []
	listing = os.listdir(dir)
	for fileName in listing:
		files.append(fileName)
	return files

#format and get output folder name
def getOutputFolder(folder, files):
	#get quarter
	filename = getCleanData(folder, files[0])[0][0]
	quarter = filename[:filename.find('_')]

	#assign output folders
	outputFolder = "./Data/" + quarter + "/"
	if (os.environ.get('cronFlag') == "True"):
		outputFolder = "./DataCrontab/" + quarter + "/"

	#create unexisted folders
	if not os.path.exists(os.path.dirname(outputFolder)):
		os.makedirs(os.path.dirname(outputFolder))

	return outputFolder

#list for cleaned data
def getCleanData(folder, file):
	cleanedData = []

	#create bs object
	soup = BeautifulSoup(open(folder + file), "html.parser")

	#find all table bodies and store them in list
	rows = soup.find_all('tr', {'class':'CourseInfoRow'})

	#iterate over list and create our raw results
	data = []
	for row in rows:
		colData = []

		cols = row.find_all('td')
		for col in cols:
			for string in col.stripped_strings:
				colData.append(string)
		data.append(colData)

	#getting significant information
	for course in data:
		cleanedDataTemp = []
		#append filename for information about Quarter and Year
		cleanedDataTemp.append(str(file))
		cleanedDataTemp.append(course[0])
		cleanedDataTemp.append(course[course.index('College:') + 1])
		cleanedDataTemp.append(course[course.index('Units:') + 1])
		cleanedDataTemp.append(course[course.index('Grading:') + 1])
		#grab last 5 indices containing important information
		for index in range(len(course) - 4, len(course)):
			cleanedDataTemp.append(course[index])
		#add the cleaned course data to cleanedData
		if cleanedDataTemp[len(cleanedDataTemp) - 2] == 'T B A':
			cleanedDataTemp[len(cleanedDataTemp) - 2] = 'N/A'
		if cleanedDataTemp[len(cleanedDataTemp) - 3] == 'T B A':
			cleanedDataTemp[len(cleanedDataTemp) - 3] = 'N/A'
			cleanedDataTemp[len(cleanedDataTemp) - 4] = 'N/A'
		elif ('am' not in cleanedDataTemp[len(cleanedDataTemp) - 3] and 'pm' not in cleanedDataTemp[len(cleanedDataTemp) - 3]):
			cleanedDataTemp = []

		cleanedData.append(cleanedDataTemp)
	print('parsed: ' + file)
	return cleanedData


#get start time
start = time.time()

#directory containing html files to parse ***EDIT THIS PATH IF USED ON A DIFFERENT MACHINE***
inputFolder = './Output/'
filesToParse = getAllFiles(inputFolder)

#format output directory
outputFolder = getOutputFolder(inputFolder, filesToParse)

#output to CSV file:
now = datetime.datetime.now()
with open(outputFolder + "data_" + str(now.month) + "_" + str(now.day) + "_" + str(now.hour) + ".csv", "w+", newline="") as f:
	writer = csv.writer(f)
	for file in filesToParse:
		writer.writerows(getCleanData(inputFolder, file))

end = time.time()
#print elapsed time
print('Time to parse: ' + str(end - start))

#print out CSV file (testing purposes)
#os.system('column -s, -t < ./Data/data.csv | less -#2 -N -S')

#Print out raw results:
"""
for course in data:
	i = 0
	for x in course:
		print(str(i) + ": ")
		print(x)
		i+=1
	print('\n')
"""