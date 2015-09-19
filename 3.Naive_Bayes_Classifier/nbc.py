import csv
import NBCOnSets as nbcsets
from collections import defaultdict
import sys
def NBC(trainF, testF, task, printTW):
	#print error and exit if unexpected classification task is specified.
	if (task!=5) and (task!=7):	
		print "Undefined classification task!. Please try again."
		sys.exit(1)
	#read training data file and testing data file and create dict objects
	#to be passed to nbcset	method	
	trainFObj = open(trainF)
	trainFReader = csv.DictReader(trainFObj, delimiter=',')
	#create dict out of csv reader
	trainDict = defaultdict(list)
	for row in trainFReader:
		for col in trainFReader.fieldnames:
			trainDict[col].append(row[col])
	
	testFObj = open(testF)
	testFReader = csv.DictReader(testFObj, delimiter=',')
	testDict = defaultdict(list)
	for row in testFReader:
		for col in testFReader.fieldnames:
			testDict[col].append(row[col])
	nbcsets.NBCOnSets(trainDict, testDict, task, printTW)
 
if __name__ == "__main__":
	#print sys.argv
	if len(sys.argv) < 5:
		print "ERROR! Wrong number of arguments provided. Please try again."
		sys.exit(1)
	NBC(sys.argv[1],sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
	#NBC("stars_data.csv","funny_data.csv", 5, 1)
	#NBC("stars_ss.csv","star_test.csv", 5, 1)
