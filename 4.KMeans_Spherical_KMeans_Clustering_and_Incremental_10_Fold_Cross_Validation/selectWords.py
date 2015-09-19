from string import punctuation
import sys
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
	#if len(sortedWords) < 2200:
	#	print len(sortedWords)
		#print "ERROR: Number of unique words should be atleast 2200."
		#sys.exit(1)
	#return 201-2200 words and top 10 out of them as two sets
	#print (sortedWords[0:200])
	bagOfWords = sortedWords[200:2200]
	#bagOfWords = sortedWords[10:60]
	topTenWords = sortedWords[200:210]	
	#topTenWords = sortedWords[10:20]		
	return bagOfWords,topTenWords
