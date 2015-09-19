import operator
import json
import itertools as iter
from collections import defaultdict
def generateIntrRuleSets(L, intrTr, intrMType):
	#L = json.load(open("FreqItemSets.txt"))
	R = defaultdict()
	freqSetSizes = L.keys()
	freqSetSizes.sort()
	#print freqSetSizes
	l = len(freqSetSizes)
	for k in range(1, (freqSetSizes[l-1])+1):
		#print k
		freqSetList = L[k]
		for freqItemSet in freqSetList.keys():
			if isinstance(freqItemSet, int):
				continue
			else:
				#print "rules for item set:"				
				#print freqItemSet
				rules = generateRulesForFreqItemSet(freqItemSet, L, intrTr)
				#print rules
				R.update(rules)
	#sortedR = sorted(R.items(), key=operator.itemgetter(1), reverse=True)
	sortedR = sorted(R.items(), key=lambda i:i[1][0], reverse=True)
	return sortedR

def generateRulesForFreqItemSet(freqItemSet, L, intrTr):
	rules = defaultdict()
	itemSetSize = len(freqItemSet)
	nonValidAntecedents = list()
	for conseqSize in range(1,itemSetSize):
		#r,nonValidAntecedents = generateRulesForConseqSizeK(conseqSize, freqItemSet, intrTr, nonValidAntecedents, L)
		r = generateRulesForConseqSizeK(conseqSize, freqItemSet, intrTr, L)
		#print "in valid antecedent for conseq size: "+str(conseqSize)
		#print nonValidAntecedents
		rules.update(r)
	return rules

def generateRulesForConseqSizeK(conseqSize, freqItemSet, intrTr, L):
	combinationsForConseq = iter.combinations(freqItemSet, conseqSize)
	conseqList = list(combinationsForConseq)	
	#print "combinations of size: "+str(conseqSize)
	#print conseqList 
	#nonValidAntecedentsForNextConseqSize = list()
	rules = defaultdict()
	for conseq in conseqList:
		antecedent = set(freqItemSet) - set(conseq)
		antecedent = tuple(antecedent)
		antecedent = tuple(sorted(antecedent))
		#print antecedent
		antSize = len(antecedent)
		if antSize == 1:
			antecedent = antecedent[0]
		if conseqSize == 1:
			conseq = conseq[0]
		#if antecedent in nonValidAntecedents:
		#	nonValidAntecedentsForNextConseqSize.append(iter.combinations(antecedent, antSize-1))
		#else:
		#calculate confidence
		matchingItemSetList = L[len(freqItemSet)]
		supportFreqItemSet = matchingItemSetList[freqItemSet]
		#print antecedent
		matchingAntecedentSetList = L[antSize]
		#print matchingAntecedentSetList
		if antecedent in matchingAntecedentSetList.keys():
			supportAntecedent = matchingAntecedentSetList[antecedent]
			confidence = supportFreqItemSet/float(supportAntecedent)
			if confidence >= intrTr:
				#rules[(antecedent, conseq)] = confidence
				rules[(antecedent, conseq)] = [confidence, supportFreqItemSet]
	return rules #,nonValidAntecedentsForNextConseqSize

def testcase1():
	L = {1: {0: 0.4, 1: 0.55, 2: 0.45, 3: 0.4, 4: 0.45, 5: 0.5, 6: 0.5}, 2: {(0, 1): 0.35, (1, 2): 0.25, (2, 5): 0.1, (1, 3): 0.3, (4, 6): 0.25, (1, 5): 0.2, (4, 5): 0.2, (1, 4): 0.2, (2, 4): 0.25, (0, 6): 0.25, (2, 6): 0.35, (0, 5): 0.15, (3, 6): 0.2, (0, 4): 0.15, (2, 3): 0.25, (1, 6): 0.35, (0, 3): 0.3, (3, 4): 0.2, (0, 2): 0.25, (3, 5): 0.2}, 3: {(3, 4, 6): 0.15, (2, 3, 5): 0.05, (1, 2, 4): 0.15, (0, 1, 2): 0.2, (0, 1, 3): 0.3, (0, 1, 4): 0.15, (0, 1, 5): 0.15, (0, 1, 6): 0.2, (0, 2, 3): 0.2, (2, 3, 6): 0.2, (2, 4, 5): 0.05, (0, 2, 4): 0.15, (2, 4, 6): 0.2, (0, 2, 6): 0.25, (1, 2, 3): 0.2, (0, 3, 6): 0.2, (0, 3, 4): 0.15, (1, 4, 6): 0.2, (1, 2, 6): 0.25, (1, 3, 6): 0.2, (0, 3, 5): 0.1, (1, 3, 5): 0.1, (1, 3, 4): 0.15, (3, 4, 5): 0.05, (2, 3, 4): 0.15, (0, 4, 6): 0.15}}
	#print L
	R = generateIntrRuleSets(L, 0.25, 1)
	sortedR = sorted(R.items(),key=operator.itemgetter(1), reverse=True) 
	print R
	print "sorted R:"
	print sortedR
	print str(len(R.keys()))
		
if __name__ == "__main__":
	L = {1:{6: 0.1362, 41: 0.114, 2000:0.5}, 2:{(6, 41): 0.0422, (41, 2000): 0.0938, (6, 2000): 0.0806}, 3:{(6, 41, 2000): 0.036}}
	R = generateRulesForConseqSizeK(1, (6,41,2000), 0.25, L)
	print R
