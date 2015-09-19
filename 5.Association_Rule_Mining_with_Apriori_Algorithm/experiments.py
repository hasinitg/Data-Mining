from collections import defaultdict
import selectWords as wordSelector
import json
import csv
import apriori as apr

def exp1():	
	#read CSV
	dataset = "stars_data.csv"
	#dataset = "starsPN.csv"
	datasetFObj = open(dataset)
	datasetFReader = csv.DictReader(datasetFObj, delimiter=',')
	rows = list(datasetFReader)
	print "dataset size:"+str(len(rows))
	#construct dict from data
	datasetDict = defaultdict(list)
	for row in rows:
		datasetDict['text'].append(row['text'])
		datasetDict['classLabel'].append(row['stars'])
	#select top words
	bagOfWords,topTenWords = wordSelector.selectWords(datasetDict['text'])
	#construct binary features	
	featureSet = wordSelector.constructBinaryFeatures(datasetDict, bagOfWords)
	#json.dump(bagOfWords, open("bagOfWords.txt",'w'))
	#mine association rules based on confidence
	rules = apr.MineAssociationRules(featureSet, bagOfWords, 0.03, 0.25, 1)
	print "sorted rules: "
	print rules
	#print top 30 rules
	for i,ruleItem in enumerate(rules):
		rule = ruleItem[0]
		conf = ruleItem[1][0]
		support = ruleItem[1][1]
		if i==30:
			break
		#build antecedent and consequence:
		antecedent = rule[0]
		conseq = rule[1]
		la = 0
		lc = 0
		if isinstance(antecedent, int):
			la=1
		else:
			la = len(antecedent)
		if isinstance(conseq, int):
			lc=1
		else:
			lc = len(conseq)
		if la == 1 and lc == 1:
			print "IF "+bagOfWords[antecedent]+" THEN "+bagOfWords[conseq]+", support: "+str(support)+", confidence: "+str(conf)
		elif la == 1 and lc == 2:
			print "IF "+bagOfWords[antecedent]+" THEN "+bagOfWords[conseq[0]]+" AND "+bagOfWords[conseq[1]]+", support: "+str(support)+", confidence: "+str(conf)
		elif la==2 and lc==1:
			print "IF "+bagOfWords[antecedent[0]]+" AND "+bagOfWords[antecedent[1]]+" THEN "+bagOfWords[conseq]+", support: "+str(support)+", confidence: "+str(conf)
	#mine association rules based on chi-squared
	#print top 30 words

def exp2():
	#read CSV
	dataset = "stars_data.csv"
	#dataset = "starsPN.csv"
	datasetFObj = open(dataset)
	datasetFReader = csv.DictReader(datasetFObj, delimiter=',')
	rows = list(datasetFReader)
	print "dataset size:"+str(len(rows))
	#construct dict from data
	datasetDict = defaultdict(list)
	for row in rows:
		datasetDict['text'].append(row['text'])
		datasetDict['classLabel'].append(row['stars'])
	#select top words	
	bagOfWords,topTenWords = wordSelector.selectWords(datasetDict['text'])
	#construct binary features	
	featureSet = wordSelector.constructBinaryFeatures(datasetDict, bagOfWords)
	#json.dump(bagOfWords, open("bagOfWords.txt",'w'))
	#mine association rules based on confidence
	rules = apr.MineAssociationRules(featureSet, bagOfWords, 0.03, 0.05, 2)
	print "sorted rules: "
	#print rules
	#print top 30 rules
	for i,ruleItem in enumerate(rules):
		rule = ruleItem[0]
		chisq = ruleItem[1][0]
		pVal = ruleItem[1][1]
		support = ruleItem[1][2]
		if i==30:
			break
		#build antecedent and consequence:
		antecedent = rule[0]
		conseq = rule[1]
		la = 0
		lc = 0
		if isinstance(antecedent, int):
			la=1
		else:
			la = len(antecedent)
		if isinstance(conseq, int):
			lc=1
		else:
			lc = len(conseq)
		if la == 1 and lc == 1:
			print "IF "+bagOfWords[antecedent]+" THEN "+bagOfWords[conseq]+", support: "+str(support)+", interestingness: "+str(chisq)+", p-val: "+str(pVal)
		elif la == 1 and lc == 2:
			print "IF "+bagOfWords[antecedent]+" THEN "+bagOfWords[conseq[0]]+" AND "+bagOfWords[conseq[1]]+", support: "+str(support)+", interestingness: "+str(chisq)+", p-val: "+str(pVal)
		elif la==2 and lc==1:
			print "IF "+bagOfWords[antecedent[0]]+" AND "+bagOfWords[antecedent[1]]+" THEN "+bagOfWords[conseq]+", support: "+str(support)+", interestingness: "+str(chisq)+", p-val: "+str(pVal)

if __name__ == "__main__":
	exp2()
