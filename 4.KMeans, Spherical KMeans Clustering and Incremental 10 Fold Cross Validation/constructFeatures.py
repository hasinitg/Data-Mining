import numpy as np
from string import punctuation
from collections import Counter
from collections import defaultdict

#feature type indicates standard k-means or shperical k-means
def constructFeatresForKMeans(dataset, featureType, featureList):
	dsSize = len(dataset['text'])
	#print dsSize
	featureSize = len(featureList)
	#print featureSize
	#WPMatrix = np.empty(shape=(2000,2500))
	WPMatrix = np.zeros(shape=(featureSize,dsSize/2))
	#WNPMatrix = np.empty(shape=(2000,2500))
	WNPMatrix = np.zeros(shape=(featureSize,dsSize/2))
	reviews = dataset["text"]
	wpColIndex = 0
	wnpColIndex = 0
	for j,review in enumerate(reviews):
		#print "review:"+str(j)
		#pre-process data: remove punctuations, convert to lower case, split
		setOfWords = review.translate(None, punctuation).lower().split()
		wordCounts = Counter(setOfWords)
		#print setOfWords
		if dataset['classLabel'][j] == '5':
			for i,word in enumerate(featureList):
				if word in wordCounts:
					#print "wp"+str(wpColIndex)
					WPMatrix[i][wpColIndex] = wordCounts[word]
				else:
					#print "wp"+str(wpColIndex)
					WPMatrix[i][wpColIndex] = 0
			wpColIndex+=1
		else:
			for i,word in enumerate(featureList):
				if word in wordCounts:
					#print "wnp:"+str(wnpColIndex)
					WNPMatrix[i][wnpColIndex] = wordCounts[word]
				else:
					#print "wnp:"+str(wnpColIndex)
					WNPMatrix[i][wnpColIndex] = 0
			wnpColIndex+=1
				
	#fix for all zeros features if features are constructed for spherical k-means
	#if featureType == 2:	
	#	for k in range(featureSize)	
	#		zeroCounts = Counter(WPMatrix[k])
	#		if zeroCounts[0] == 
	#print WPMatrix
	#print WNPMatrix
	return WPMatrix, WNPMatrix

#feature type indicates whether top words or clustered words
def constructFeaturesForNBC(dataset, featureType, featureList):
	featureSet = defaultdict(list)
	reviews = dataset['text']
	if featureType == 1:
		#print "Costructing features on top words"
		#create feature set with top words
		for i,review in enumerate(reviews):
			setOfWords = set(review.translate(None, punctuation).lower().split())
			for word in featureList:
				if word in setOfWords:
					featureSet[word].append(1)
				else:
					featureSet[word].append(0)
			classLabelVal = dataset['classLabel'][i]
			if int(classLabelVal) == 5:
				featureSet["classLabel"].append(1)
			elif int(classLabelVal) == 1:
				featureSet["classLabel"].append(0)
		#print featureSet
		return featureSet
	elif featureType == 2:
		#print "Constructing features on clustered words."
		#create feature set with clustered words
		topics = featureList.keys()
		for i,review in enumerate(reviews):
			#print review			
			setOfWords = set(review.translate(None, punctuation).lower().split())
			for topic in topics:
				isTopicIncluded = False
				for word in featureList[topic]:
					if word in setOfWords:
						isTopicIncluded = True
						break
				if isTopicIncluded:
					featureSet[topic].append(1)
				else:
					featureSet[topic].append(0)
			classLabelVal = dataset['classLabel'][i]
			if int(classLabelVal) == 5:
				featureSet["classLabel"].append(1)
			elif int(classLabelVal) == 1:
				featureSet["classLabel"].append(0)
		#print featureSet		
		return featureSet
	
