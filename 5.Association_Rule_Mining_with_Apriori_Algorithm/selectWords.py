from string import punctuation
import sys
from collections import defaultdict
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
	
	#return 201-2200 words and top 10 out of them as two sets
	#print (sortedWords[0:200])
	bagOfWords = sortedWords[100:2100]
	#bagOfWords = sortedWords[25:30]
	topTenWords = sortedWords[100:210]	
	#topTenWords = sortedWords[25:35]		
	return bagOfWords,topTenWords

#construct binary features to select itemsets
def constructBinaryFeatures(dataset, featureList):
	featureSet = defaultdict(list)
	reviews = dataset['text']
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
			featureSet["isPositive"].append(1)
			featureSet["isNegative"].append(0)
		elif int(classLabelVal) == 1:
			featureSet["isPositive"].append(0)
			featureSet["isNegative"].append(1)
	featureList.append("isPositive")
	featureList.append("isNegative")
	#print featureSet
	return featureSet
