from collections import defaultdict
import random
from NBC import *
import math
from constructFeatures import *
import numpy as numpy
#this splits dataset to test sets and then leaves out each one of them and use the rest to 
#generate 10 random training sets for each of the sizes given in listOfTrainSetSizes
def generatePartitions(datasetSize,noOfFolds,listOfTrainSetSizes):
	testSetSize = datasetSize/noOfFolds	
	#parition dataset into test sets	
	testSetPartitions = defaultdict(list)
	randomList = random.sample(range(datasetSize),datasetSize)
	for i in range(noOfFolds):
		for j in range(testSetSize):
			testSetPartitions[i].append(randomList[testSetSize*i+j])
	#print "Test Set Partitions:"
	#print testSetPartitions
	
	#create train set indices
	trainSetPartitions = defaultdict(defaultdict)
	for trainSetSize in listOfTrainSetSizes:
		partitionList = defaultdict(list)		
		for i in range(noOfFolds):
			randomList = random.sample(range(datasetSize),datasetSize)
			count = 0
			for j,randomIndex in enumerate(randomList):
				if count == trainSetSize:
					break
				if randomIndex in testSetPartitions[i]:
					continue
				partitionList[i].append(randomIndex)
				count+=1	
		trainSetPartitions[trainSetSize] = partitionList		
	#print "Train Set Partitions:"	
	#print trainSetPartitions		
	return testSetPartitions, trainSetPartitions

def crossValidate(dataset, noOfFolds, testSetPartitions, trainSetPartitions, featureType, featureList):
	
	#build test data sets based on provided indices
	testSetData = defaultdict(defaultdict)
	for k in testSetPartitions.keys():
		#store texts and class labels for each test set
		testData = defaultdict(list)
		testSetIndices = testSetPartitions[k]
		for i,index in enumerate(testSetIndices):
			testData['text'].append(dataset['text'][index])
			testData['classLabel'].append(dataset['classLabel'][index])
		#construct features for current test data set
		testSetFeatures = constructFeaturesForNBC(testData, featureType, featureList) 
		testSetData[k] = testSetFeatures
	#print testSetData
	
 	#datastructure to hold final results
	finalResults = defaultdict(defaultdict)
	#for each train set size
	for i in trainSetPartitions.keys():
		ZOL = []
		BLE = []
		#for each fold in k fold
		for j in range(noOfFolds):
			currentTrainSet = defaultdict(list)
			currentTrainSetIndices = trainSetPartitions[i][j]
			for k,index in enumerate(currentTrainSetIndices):
				currentTrainSet['text'].append(dataset['text'][index])	
				currentTrainSet['classLabel'].append(dataset['classLabel'][index])
			currentTrainSetFeatures = constructFeaturesForNBC(currentTrainSet, featureType, featureList)
			if featureType == 1:
				l,bl = NBC(currentTrainSetFeatures, testSetData[j], featureList)
			if featureType == 2:
				l,bl = NBC(currentTrainSetFeatures, testSetData[j], featureList.keys())
			ZOL.append(l)
			BLE.append(bl)
		#calculate mean ZOL and standard error w.r.t NBC prediction and baseline prediction for each train set size
		ZOLArr = numpy.array(ZOL)
		ZOLMean = numpy.mean(ZOLArr)
		ZOLStd = numpy.std(ZOLArr)
		standardErr = ZOLStd/math.sqrt(noOfFolds)

		BArr = numpy.array(BLE)
		BEMean = numpy.mean(BArr)
		BEStd = numpy.std(BArr)
		bstdErr = BEStd/math.sqrt(noOfFolds)		
		
		currentResults = {'avg':[ZOLMean],'stderr':[standardErr],'blavg':[BEMean],'blstderr':[bstdErr]}
		finalResults[i] = currentResults
	#print finalResults
	return finalResults

if __name__ == "__main__":
	generatePartitions(50,10,[5,10,20,30,40])
