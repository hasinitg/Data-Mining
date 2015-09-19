import json
import csv
import selectWords as wordSelector
from collections import defaultdict
from constructFeatures import * 
from kmeans import *
import random
from NBC import *
from inc10FCV import *

def exp0():
	#read CSV
	dataset = "stars_data.csv"
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
	json.dump(bagOfWords, open("bagOfWords.txt",'w'))
	
	#prepare 100 topics from files written by experiment 1:StandardKMeans
	kmWPClusters = json.load(open("wordClustersStdKM_WP_50.txt"))
	kmWNPClusters = json.load(open("wordClustersStdKM_WNP_50.txt"))
	kmAllClusters = defaultdict(list)
	for i,topicLabel in enumerate(kmWPClusters.keys()):
		intLabel = int(float(topicLabel))
		kmAllClusters[intLabel] = kmWPClusters[topicLabel]

	for i,topicLabel in enumerate(kmWNPClusters.keys()):
		intLabel = int(float(topicLabel))
		intLabel += 50
		kmAllClusters[intLabel] = kmWNPClusters[topicLabel]
	json.dump(kmAllClusters, open("allTopics_KM.txt","w"))
	
	#prepare 100 topics from files written by experiment 1:SphericalKMeans
	skmWPClusters = json.load(open("wordClustersSP_KM_WP_50.txt"))
	skmWNPClusters = json.load(open("wordClustersSP_KM_WNP_50.txt"))
	skmAllClusters = defaultdict(list)
	for i,topicLabel in enumerate(skmWPClusters.keys()):
		intLabel = int(float(topicLabel))
		skmAllClusters[intLabel] = skmWPClusters[topicLabel]

	for i,topicLabel in enumerate(skmWNPClusters.keys()):
		intLabel = int(float(topicLabel))
		intLabel += 50
		skmAllClusters[intLabel] = skmWNPClusters[topicLabel]
	json.dump(skmAllClusters, open("allTopics_SKM.txt","w"))

def exp1(clusteringMethod):
	#read CSV
	dataset = "stars_data.csv"
	datasetFObj = open(dataset)
	datasetFReader = csv.DictReader(datasetFObj, delimiter=',')
	rows = list(datasetFReader)
	#construct dict from data
	datasetDict = defaultdict(list)
	for row in rows:
		datasetDict['text'].append(row['text'])
		datasetDict['classLabel'].append(row['stars'])
	#select top words	
	bagOfWords,topTenWords = wordSelector.selectWords(datasetDict['text'])
	#print bagOfWords
	#construct features for KMeans using selected words, to select topics for NBC
	WP,WNP = constructFeatresForKMeans(datasetDict, 1, bagOfWords)
	
	clusterSizes = [10,20,50,100,200]
	resultsStdKMWP = defaultdict(list)
	resultsStdKMWNP = defaultdict(list)
	for size in clusterSizes:
		if clusteringMethod == 1:
			#WP
			centroids, clusterLabels, clusterScore, sumOfDistance = clusterWithRandomRestarts(WP, size)
			resultsStdKMWP['size'].append(size)
			resultsStdKMWP['cluster score'].append(clusterScore)
			clusters = defaultdict(list)
			for i,label in enumerate(clusterLabels):
				clusters[label].append(bagOfWords[i])
			#write word clustering for each size into a file:
			fname = "wordClustersStdKM_WP_"+str(size)+".txt"
			json.dump(clusters, open(fname,'w'))
			#WNP
			centroids, clusterLabels, clusterScore, sumOfDistance = clusterWithRandomRestarts(WNP, size)			
			resultsStdKMWNP['size'].append(size)
			resultsStdKMWNP['cluster score'].append(clusterScore)
			clusters = defaultdict(list)
			for i,label in enumerate(clusterLabels):
				clusters[label].append(bagOfWords[i])	
			#write word clustering for each size into a file:
			fname = "wordClustersStdKM_WNP_"+str(size)+".txt"
			json.dump(clusters, open(fname,'w'))

		elif clusteringMethod == 2:
			centroids, clusterLabels, clusterScore, sumOfDistance = spclusterWithRandomRestarts(WP, size)
			resultsStdKMWP['size'].append(size)
			resultsStdKMWP['cluster score'].append(clusterScore)
			clusters = defaultdict(list)
			for i,label in enumerate(clusterLabels):
				clusters[label].append(bagOfWords[i])
			#write word clustering for each size into a file:
			fname = "wordClustersSP_KM_WP_"+str(size)+".txt"
			json.dump(clusters, open(fname,'w'))
		
			centroids, clusterLabels, clusterScore, sumOfDistance = spclusterWithRandomRestarts(WNP, size)		
			resultsStdKMWNP['size'].append(size)
			resultsStdKMWNP['cluster score'].append(clusterScore)
			clusters = defaultdict(list)
			for i,label in enumerate(clusterLabels):
				clusters[label].append(bagOfWords[i])	
			#write word clustering for each size into a file:
			fname = "wordClustersSP_KM_WNP_"+str(size)+".txt"
			json.dump(clusters, open(fname,'w'))
	
	rfName = "results_WP_"+str(clusteringMethod)+".txt"
	rfName2 = "results_WNP_"+str(clusteringMethod)+".txt"
	json.dump(resultsStdKMWP, open(rfName,'w'))
	json.dump(resultsStdKMWNP, open(rfName2,'w'))

def exp2():
	noOfClusters = 50
	listOfTrainSetSizes = [100,250,500,1000,2000]
	datasetSize = 5000
	noOfFolds = 10	
	#read CSV
	dataset = "stars_data.csv"
	datasetFObj = open(dataset)
	datasetFReader = csv.DictReader(datasetFObj, delimiter=',')
	rows = list(datasetFReader)
	print "dataset size:"+str(len(rows))
	#construct dict from data
	datasetDict = defaultdict(list)
	for row in rows:
		datasetDict['text'].append(row['text'])
		datasetDict['classLabel'].append(row['stars'])
	#read features
	kmClusteredWords = json.load(open("allTopics_KM.txt"))
	skmClusteredWords = json.load(open("allTopics_SKM.txt"))	
	#parition data randomly for incremental k-fold cross validation:
	testSetPartitions, trainSetPartitions = generatePartitions(datasetSize, noOfFolds, listOfTrainSetSizes)
	#run NBC with inc10FCV using Kmeans-clustered words as features
	resultsForTopWords = crossValidate(datasetDict, noOfFolds, testSetPartitions, trainSetPartitions, 2, kmClusteredWords)
	print "Results for KMeans-clustered words:"	
	print resultsForTopWords
	#run NBC with inc10FCV using clustered words as features
	print "Results for S-KMeans-clustered words:"	
	resultsForClusteredWords = crossValidate(datasetDict, noOfFolds, testSetPartitions, trainSetPartitions, 2, skmClusteredWords)
	print resultsForClusteredWords

def exp3():
	noOfClusters = 50
	listOfTrainSetSizes = [100,250,500,1000,2000]
	datasetSize = 5000
	noOfFolds = 10	
	#read CSV
	dataset = "stars_data.csv"
	datasetFObj = open(dataset)
	datasetFReader = csv.DictReader(datasetFObj, delimiter=',')
	rows = list(datasetFReader)
	#print "dataset size:"+str(len(rows))
	#construct dict from data
	datasetDict = defaultdict(list)
	for row in rows:
		datasetDict['text'].append(row['text'])
		datasetDict['classLabel'].append(row['stars'])
	#read features
	kmClusteredWords = json.load(open("allTopics_KM.txt"))
	bagOfWords = json.load(open("bagOfWords.txt"))	
	#parition data randomly for incremental k-fold cross validation:
	testSetPartitions, trainSetPartitions = generatePartitions(datasetSize, noOfFolds, listOfTrainSetSizes)
	#run NBC with inc10FCV using Kmeans-clustered words as features
	resultsForTopWords = crossValidate(datasetDict, noOfFolds, testSetPartitions, trainSetPartitions, 2, kmClusteredWords)
	print "Results for KMeans-clustered words:"	
	print resultsForTopWords
	#run NBC with inc10FCV using top words as features
	print "Results for top words:"	
	resultsForClusteredWords = crossValidate(datasetDict, noOfFolds, testSetPartitions, trainSetPartitions, 1, bagOfWords)
	print resultsForClusteredWords

def exp4():
	noOfClusters = 50
	listOfTrainSetSizes = [100,250,500,1000,2000]
	datasetSize = 5000
	noOfFolds = 10	
	#read CSV
	dataset = "stars_data.csv"
	datasetFObj = open(dataset)
	datasetFReader = csv.DictReader(datasetFObj, delimiter=',')
	rows = list(datasetFReader)
	#print "dataset size:"+str(len(rows))
	#construct dict from data
	datasetDict = defaultdict(list)
	for row in rows:
		datasetDict['text'].append(row['text'])
		datasetDict['classLabel'].append(row['stars'])
	#read features
	kmClusteredWords = json.load(open("allTopics_KM.txt"))
	bagOfWords = json.load(open("bagOfWords.txt"))
	randWords = random.sample(bagOfWords,100)		
	
	#parition data randomly for incremental k-fold cross validation:
	testSetPartitions, trainSetPartitions = generatePartitions(datasetSize, noOfFolds, listOfTrainSetSizes)
	#run NBC with inc10FCV using Kmeans-clustered words as features
	resultsForTopWords = crossValidate(datasetDict, noOfFolds, testSetPartitions, trainSetPartitions, 2, kmClusteredWords)
	print "Results for KMeans-clustered words:"	
	print resultsForTopWords
	#run NBC with inc10FCV using 100 top words as features
	print "Results for top words:"	
	resultsForClusteredWords = crossValidate(datasetDict, noOfFolds, testSetPartitions, trainSetPartitions, 1, randWords)
	print resultsForClusteredWords
	
	#combine features for approach C:
	for j,word in enumerate(randWords):
		kmClusteredWords[j+100]=word	
	
	#run NBC with inc10FCV using Kmeans-clustered words as features
	resultsForCombWords = crossValidate(datasetDict, noOfFolds, testSetPartitions, trainSetPartitions, 2, kmClusteredWords)
	print "Results for combined words:"	
	print resultsForCombWords

if __name__ == "__main__":
	exp1(1)
	exp1(2)
	exp0()	
	exp2()
	#exp3()
	#exp4()












