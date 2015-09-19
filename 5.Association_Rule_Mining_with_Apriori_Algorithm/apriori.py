from collections import Counter
from collections import defaultdict
import itertools as iter
import json
from rules import generateIntrRuleSets
from rulesChiSq import generateRuleSets
def MineAssociationRules(dataset, featureList, suppTr, intrTr, intrMType):
	L,p,q = generateFrqItemSets(dataset, featureList, suppTr)
	print "number of candidate sets: "+str(p)
	print "itemsets found to be frequent: "+ str(q)
	print "itemsets found to be infrequent: "+str(p-q)
	print "###########All freq item sets:################"
	print L
	if intrMType ==1:
		R = generateIntrRuleSets(L, intrTr, intrMType)
		print "number of rules: "
		print str(len(R))
	elif intrMType ==2:
		R = generateRuleSets(L, intrTr, intrMType)
		print "number of valid rules: "
		print str(len(R))
	return R

def generateFrqItemSets(dataset, featureList, suppTr):
	dsSize = len(dataset[featureList[1]])
	#print "dataset size: "+str(dsSize)
	#returned freq item sets will be of the format: {1: {(1):[3], (2):[5], (3):[1], (5):[3]} , 2: {(1, 3): [6], (2, 3): [6], (5, 3): [6]}}, itemsetsize:{(itemset):[freq], ...}}
	L = defaultdict(defaultdict)
	p = len(featureList) # no. of candidate sets considered (i.e: support counted) by the algorithm

	frqItemSetList, frqItemSetDict = findFreqItemSetsOfSizeK(dataset, dsSize, featureList, featureList, 1, suppTr)
	print "numb of freq item sets of size:1="+str(len(frqItemSetList))
	q = len(frqItemSetList) # no. of itemsets found to be frequent
	L[1] = frqItemSetDict
	candItemSetList = list()
	
	for k in range(2,4):
		if len(frqItemSetList)==0:
			#print "no candidates for k="+str(k)
			return
	
		candItemSetList = generateCandidateItemSets(frqItemSetList, frqItemSetDict, k)
		p = p + len(candItemSetList)
		frqItemSetList = defaultdict(list)
		frqItemSetList,frqItemSetDict = findFreqItemSetsOfSizeK(dataset, dsSize, featureList, candItemSetList, k, suppTr)
		print "numb of freq item sets of size:"+str(k)+" = "+str(len(frqItemSetList))
		q = q + len(frqItemSetList)		
		L[k] = frqItemSetDict
	
	return L,p,q

def findFreqItemSetsOfSizeK(dataset, datasetSize, featureList, candidateSetList, itemSetSize, suppTr):	
	#freq item set list for a given item set size is of the form: {(1, 3): [6], (2, 3): [6], (5, 3): [6], (itemset):[freq]}
	freqItemSetDict = defaultdict(list)
	freqItemSetList = list()
	if itemSetSize == 1:
		#we use the indices of features in original feature list as items
		for i,f in enumerate(candidateSetList):
			featureList = dataset[f]
			binaryCounter = Counter(featureList)
			oneCount = binaryCounter[1]
			support = oneCount/float(datasetSize)		
			if support >= suppTr:
				freqItemSetList.append(i)
				freqItemSetDict[i] = support
		#print "freq item sets for set size=1:"
		#print freqItemSetList, freqItemSetDict	
		return freqItemSetList, freqItemSetDict
	else:
		#we use the indices of features in original feature list as items
		for i,f in enumerate(candidateSetList):
			#print f
			count = 0
			for t in range(datasetSize):
				#print t
				featuresPositive = True
				for j in range(itemSetSize):
					featureIndex = f[j]
					#print featureIndex
					featureName = featureList[featureIndex]
					#print featureName
					featureBinaryVal = dataset[featureName][t]
					#print featureBinaryVal
					if not featureBinaryVal:
						featuresPositive = False						
						break
				if featuresPositive:
					count = count + 1
			#print count
			support = count/float(datasetSize)
			#print support						
			if support >= suppTr:
				freqItemSetList.append(f)
				freqItemSetDict[f] = support
		#print "freq item sets for set size="+str(itemSetSize)
		#print freqItemSetList, freqItemSetDict
		return freqItemSetList, freqItemSetDict
		

def generateCandidateItemSets(freqItemSetList, frqItemSetDict, k):
	#print "frequent item sets to generate cadidate sets of size: "+str(k)
	#print freqItemSetList
	freqItemSets = freqItemSetList
	#print "freq item sets:"
	#print freqItemSets
	freqItemSetSize = len(freqItemSets)	
	candItemSets = list()
	if k==2:
		#generate candidate sets in lexiographical order of the indexes of features in the original feature list
		for i,item1 in enumerate(freqItemSets):
			for item2 in freqItemSets[i+1:freqItemSetSize]:
				candItemSet = (item1, item2)
				candItemSets.append(candItemSet)
		#print "candidate item sets for item set size=2:"
		#print candItemSets
		return candItemSets
	else:
		#print "item set size:"+str(k)
		for i,item1 in enumerate(freqItemSets):
			#print "item 1:"
			#print item1
			for item2 in freqItemSets[i+1:freqItemSetSize]:
				#print "item 2:"
				#print item2
				firstSubStringsMatched = True
				for j in range(k-2):
					if item1[j] == item2[j]:
						continue
					else:
						firstSubStringsMatched = False
						break
				if firstSubStringsMatched:
					if item1[k-2]<item2[k-2]:
						#print "creating new item:"
						newItem = list()
						for z in range(k-1):
							newItem.append(item1[z])
						newItem.append(item2[k-2])
						#print tuple(newItem)
						candItemSets.append(tuple(newItem))
						#break
		#prune the candidate item sets
		candSetsAfterPrune = list()
		for cand in candItemSets:
			comb = iter.combinations(cand, k-1)
			subsetList = list(comb)
			#print "combinations: "
			#print subsetList
			allSubSetsRFreq = True
			for ss in subsetList:
				if ss not in frqItemSetDict.keys():
					allSubSetsRFreq = False
					break
			if allSubSetsRFreq:
				candSetsAfterPrune.append(cand)		
		#print "candidate item sets for item set size=3 and above:"
		#print candSetsAfterPrune
		return candSetsAfterPrune

########################################Test Cases####################################################################
def TestCaseForfindFreqItemSetsOfSizeK():
	dataset = {'isNegative': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 'food': [0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0], 'as': [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1], 'isPositive': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'so': [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1], 'have': [1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0], 'its': [0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0]}
	featureList = ["as", "food", "so", "its", "have", "isPositive", "isNegative"]
	candidateSetList = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4), (2, 5), (2, 6), (3, 4), (3, 5), (3, 6), (4, 5), (4, 6), (5, 6)]
	findFreqItemSetsOfSizeK(dataset, 20, featureList, candidateSetList, 2, 0.03)
	
if __name__ == "__main__":
	freqItemSetList = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4), (2, 5), (2, 6), (3, 4), (3, 5), (3, 6), (4, 5), (4, 6)]
	generateCandidateItemSets(freqItemSetList, 3)
