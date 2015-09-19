from collections import defaultdict
from collections import Counter
from decimal import *
import sys

def NBC(trainSet, testSet, featureList):
	MLE, priorP, priorN = learnNBC(trainSet, featureList)
	predictions = NBCClassify(testSet, featureList, MLE, priorP, priorN)
	ZOL, baseLineError = computeZeroOneLoss(predictions, priorP, priorN)		
	return ZOL, baseLineError

def learnNBC(trainSet, featureList):
	classLabels = trainSet['classLabel']
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
	
	#dict that stores MLE vals would look like: {'feature1':[fPpP,fNpP,fPpN,fNpP], 'feature2':[],...} (feature positive-given-class-psitive etc)
	MLEDict = defaultdict(list)
	
	#applying laplace smoothing for to-be denominators	
	priorPCount +=2
	priorNCount +=2
	for feature in featureList:
		#compute max likelyhood estimates
		featureVals = trainSet[feature]
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
	#print MLEDict, priorP, priorN
	return MLEDict, priorP, priorN

def NBCClassify(testSet, featureList, MLE, priorP, priorN):
	testSetSize = len(testSet[featureList[1]])
	getcontext.prec = 1000
	results = defaultdict(list)
	#MLE vals would look like: {'feature1':[fPpP,fNpP,fPpN,fNpP], 'feature2':[],...}
	for i in range(testSetSize):
		probPositive = priorP
		probNegative = priorN
		for word in featureList:
			featureVal = testSet[word][i]
			if featureVal == 1:
				probPositive *= MLE[word][0]
				probNegative *= MLE[word][2]
			elif featureVal == 0:
				probPositive *= MLE[word][1]
				probNegative *= MLE[word][3]
		#add true class label to results
		results[i].append(testSet['classLabel'][i])
		#add predicted class label to results
		#print "prob of positive for: "+str(i)
		#print str(probPositive)
		#print "prob of negative for: "+str(i)
		#print probNegative
		if probPositive > probNegative:
			results[i].append(1)
		else:
			results[i].append(0)
	#print results
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
		if actLabel != baseLinePrediction:
			baseLineError+=1
	result = zeroOneLoss/float(totalSize)
	baseLineResult = baseLineError/float(totalSize)
	return result,baseLineResult
