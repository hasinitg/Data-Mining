import csv
from string import punctuation
from collections import defaultdict
from collections import Counter
import sys
import random
from decimal import *
import numpy
def NBCOnSets(trainS, testS, task, printTopWords):
	#extract the data in the 'text' column of each row in trainS set
	#select the top 2000 unique words	
	selectedWords,topTenWords = selectWords(trainS["text"])
	#print top 10 words if requested	
	if printTopWords == 1:
		for i,word in enumerate(topTenWords):
			print "WORD"+str(i+1)+" "+word
		#print topTenWords
	#construct features for train set
	trainFeatures = constructFeatures(trainS, selectedWords, task)
	#print trainFeatures
	#learn NBC on trainset features
	MLE, priorP, priorN = learnNBC(trainFeatures,selectedWords,task)
	#print "output from NBCLearn:"	
	#print MLE
	#print priorP
	#print priorN
	#construct features for test set
	testFeatures = constructFeatures(testS, selectedWords, task)
	#print testFeatures
	#NBC classify on test set
	predictedResults = NBCClassify(testFeatures, selectedWords, MLE, priorP, priorN, task)
	#print predictedResults
	#evaluate zero one loss
	ZOL,baseError = computeZeroOneLoss(predictedResults,priorP,priorN)
	#print zero one loss	
	print "ZEOR-ONE-LOSS "+str(ZOL)
	#print "Base-Error "+str(baseError)
	#return zero one loss
	return ZOL,baseError

	
def selectWords(listOfTexts):
	wordCounts = {}
	for text in listOfTexts:
		#pre-process data: remove punctuations, convert to lower case, split
		setOfAllWords = text.translate(None, punctuation).lower().split()
		for word in setOfAllWords:
			#create the counts of unique words
			if word in wordCounts:
				wordCounts[word] +=1
			else:
				wordCounts[word] =1
	#sort the words by count
	sortedWords = sorted(wordCounts, key=wordCounts.get, reverse=True)
	#print an error if there are no 2200 unique words
	if len(sortedWords) < 2200:
	#	print len(sortedWords)
		print "ERROR: Number of unique words should be atleast 2200."
		sys.exit(1)
	#return 201-2200 words and top 10 out of them as two sets
	#print (sortedWords[0:200])
	bagOfWords = sortedWords[200:2200]
	#bagOfWords = sortedWords[10:60]
	topTenWords = sortedWords[200:210]	
	#topTenWords = sortedWords[10:20]		
	return bagOfWords,topTenWords


def constructFeatures(dataset, bagOfWords, task):
	features = defaultdict(list)
	reviews = dataset["text"]
	funnyVals = dataset["funny"]
	starsVals = dataset["stars"]
	
	for i,review in enumerate(reviews):
		setOfWords = set(review.translate(None, punctuation).lower().split())
		#print setOfWords
		for word in bagOfWords:
			if word in setOfWords:
				features[word].append(1)
			else:
				features[word].append(0)
		if task == 5:
			classLabelVal = funnyVals[i]
			#print classLabelVal
			if int(classLabelVal) > 0:
				#print "isFunny"
				features["isFunny"].append(1)
			elif int(classLabelVal) == 0:
				#print "isFunnyNot"
				features["isFunny"].append(0)
		elif task == 7:
			classLabelVal = starsVals[i]
			if int(classLabelVal) == 5:
				features["isPositive"].append(1)
			elif int(classLabelVal) == 1:
				features["isPositive"].append(0)
	return features


def learnNBC(featureSet, bagOfWords, task):
	#calculate prior
	classLabelIndex = ""
	if task == 5:
		classLabelIndex = "isFunny"
	elif task == 7:
		classLabelIndex = "isPositive"
	classLabels = featureSet[classLabelIndex]
	classCounter = Counter(classLabels)	
	priorPCount = classCounter[1]
	#print "PriorPCount:"
	#print priorPCount
	priorNCount = classCounter[0]
	#print "PriorNCount:"
	#print priorNCount
	priorP = priorPCount/float(len(classLabels))
	priorN = 1-priorP
	#print "PriorP:"
	#print priorP
	#print "PriorN:"
	#print priorN
	#check for a fully biased input:
	if (priorPCount == 0) or (priorNCount == 0):
		print "This is a fully biased sample with same class label value. Exiting the program..."
		sys.exit(1)
	
	#dict that stores MLE vals would look like: {'feature1':[fPpP,fNpP,fPpN,fNpP], 'feature2':[],...}
	MLEDict = defaultdict(list)
	
	#applying laplace smoothing for to-be denominators	
	priorPCount +=2
	priorNCount +=2
	for feature in bagOfWords:
		#compute max likelyhood estimates
		featureVals = featureSet[feature]
		fPcPCount = 0
		fNcPCount = 0
		fPcNCount = 0
		fNcNCount = 0
		for i,c in enumerate(classLabels):
			featureVal = featureVals[i]
			if c == 1:
				if featureVal == 1:
					fPcPCount +=1
				elif featureVal == 0:
					fNcPCount +=1
			elif c == 0:
				if featureVal == 1:
					fPcNCount +=1
				elif featureVal == 0:
					fNcNCount +=1
		#print "feature counts before laplace:"
		#print fPcPCount
		#print fNcPCount
		#print fPcNCount
		#print fNcNCount
		
		#add laplace smoothing to all to-be nominators:
		fPcPCount +=1
		fNcPCount +=1
		fPcNCount +=1
		fNcNCount +=1
			
		fPpPMLE = (fPcPCount)/float(priorPCount)
		MLEDict[feature].append(fPpPMLE)
		#print "fPpPMLE:"
		#print fPpPMLE
		fNpPMLE = fNcPCount/float(priorPCount)
		MLEDict[feature].append(fNpPMLE)
		#print "fNpPMLE:"
		#print fNpPMLE
		fPpNMLE = fPcNCount/float(priorNCount)
		MLEDict[feature].append(fPpNMLE)
		#print "fPpNMLE:"
		#print fPpNMLE
		fNpNMLE = fNcNCount/float(priorNCount)
		MLEDict[feature].append(fNpNMLE)
		#print "fNpNMLE:"
		#print fNpNMLE
	#return MLE estimates and prior estimates
	return MLEDict, priorP, priorN

def NBCClassify(testFeatures, bagOfWords, MLE, priorP, priorN, task):
	testSetSize = len(testFeatures[bagOfWords[1]])
	getcontext.prec = 1000
	results = defaultdict(list)
	#MLE vals would look like: {'feature1':[fPpP,fNpP,fPpN,fNpP], 'feature2':[],...}
	for i in range(testSetSize):
		probPositive = priorP
		probNegative = priorN
		for word in bagOfWords:
			featureVal = testFeatures[word][i]
			if featureVal == 1:
				probPositive *= MLE[word][0]
				probNegative *= MLE[word][2]
			elif featureVal == 0:
				probPositive *= MLE[word][1]
				probNegative *= MLE[word][3]
		#add true class label to results
		classLabelIndex = ""
		if task == 5:
			classLabelIndex = "isFunny"
		elif task == 7:
			classLabelIndex = "isPositive"
		results[i].append(testFeatures[classLabelIndex][i])
		#add predicted class label to results
		#print "prob of positive for: "+str(i)
		#print str(probPositive)
		#print "prob of negative for: "+str(i)
		#print probNegative
		if probPositive > probNegative:
			results[i].append(1)
		else:
			results[i].append(0)
	return results

def computeZeroOneLoss(predictedResults,priorP,priorN):
	totalSize = len(predictedResults.keys())
	zeroOneLoss = 0
	baseLineError = 0
	baseLinePrediction = 0
	if priorP > priorN:
		baseLinePrediction = 1
	for j in range(totalSize):
		labels = predictedResults[j]
		actLabel = labels[0]
		predLabel = labels[1]
		if actLabel != predLabel:
			zeroOneLoss+=1
		if predLabel != baseLinePrediction:
			baseLineError+=1
	result = zeroOneLoss/float(totalSize)
	baseLineResult = baseLineError/float(totalSize)
	return result,baseLineResult
				

if __name__ == "__main__":
	starFile = "stars_data.csv"
	funnyFile = "funny_data.csv"
	summary = defaultdict(list)
	for task in [5,7]:
		if task == 5:
			trainF = funnyFile
		elif task == 7:
			trainF = starFile
		trainFObj = open(trainF)
		trainFReader = csv.DictReader(trainFObj, delimiter=',')
		#create dict out of csv reader
		trainDict = defaultdict(list)
		colNames = trainFReader.fieldnames 
		for k,row in enumerate(trainFReader):
			for col in trainFReader.fieldnames:
				trainDict[col].append(row[col])
		#trSize = len(trainFReader[colNames[1]])
		trSize = k+1
		for size in [10,50,90]:
			ZOLVals = []
			baselineError = []
			trainSize = int(trSize*(size/float(100)))
			for i in range(10):
				trainSampleIndices = random.sample(range(trSize),trainSize)
				trainSample = defaultdict(list)
				testSample = defaultdict(list)
				for col in colNames:
					attr = trainDict[col]
					for j in range(len(attr)):
						if j in trainSampleIndices:
							trainSample[col].append(attr[j])
						else:
							testSample[col].append(attr[j])
				ZOL,baseError = NBCOnSets(trainSample, testSample, task, 0)
				ZOLVals.append(ZOL)
				baselineError.append(baseError)
			#print ZOLVals
			ZOLArr = numpy.array(ZOLVals)
			ZOLMean = numpy.mean(ZOLArr)
			ZOLStd = numpy.std(ZOLArr)
			if task == 5:
				summary["type"].append("FCE")
			if task == 7:
				summary["type"].append("SCE")
			summary["size"].append(trainSize)
			summary["mean"].append(ZOLMean)
			summary["stdv"].append(ZOLStd)
			#print baselineError
			BArr = numpy.array(baselineError)
			BEMean = numpy.mean(BArr)
			BEStd = numpy.std(BArr)
			if task == 5:
				summary["type"].append("FBE")
			if task == 7:
				summary["type"].append("SBE")
			summary["size"].append(trainSize)
			summary["mean"].append(BEMean)
			summary["stdv"].append(BEStd)
	print summary
