from sklearn.cluster import KMeans
import random
import numpy as np
from collections import defaultdict
from scipy import spatial
from numpy import linalg as la

def standardKMeansCluster(data, k):
	km = KMeans(n_clusters=k,init='random')
	km.fit(data)
	return km.cluster_centers_, km.labels_ , km.inertia_

def clusterWithRandomRestarts(data, k, maxIterations = 100, noOfRandomRestarts = 10):
	results = defaultdict(list)	
	for i in range(noOfRandomRestarts):
		centroids, clusterLabels, clusterScore, sumOfDistance = clusterByStandardKMeans(data, k, maxIterations, noOfRandomRestarts)
		results['centroids'].append(centroids)
		results['clusterLabels'].append(clusterLabels)
		results['clusterScore'].append(clusterScore)
		results['sumOfDistance'].append(sumOfDistance)
	minDI = np.array(results['sumOfDistance']).argmin()
	return results['centroids'][minDI], results['clusterLabels'][minDI], results['clusterScore'][minDI], results['sumOfDistance'][minDI]	

def spclusterWithRandomRestarts(data, k, maxIterations = 100, noOfRandomRestarts = 10):
	results = defaultdict(list)		
	for i in range(noOfRandomRestarts):
		centroids, clusterLabels, clusterScore, sumOfDistance = sphericalKMeans(data, k, maxIterations, noOfRandomRestarts)
		results['centroids'].append(centroids)
		results['clusterLabels'].append(clusterLabels)
		results['clusterScore'].append(clusterScore)
		results['sumOfDistance'].append(sumOfDistance)
	maxDI = np.array(results['clusterScore']).argmax()
	return results['centroids'][maxDI], results['clusterLabels'][maxDI], results['clusterScore'][maxDI], results['sumOfDistance'][maxDI]	
		
def clusterByStandardKMeans(data, k, maxIterations = 100, noOfRandomRestarts = 10):
	#obtain random centroid indices
	centroidIndices = random.sample(range(data.shape[0]),k)
	#print "centroid indices:"
	#print centroidIndices
	#extract the initial centroids using above random indices
	centroids = data[centroidIndices,]
	#print "initial centroids: "
	#print centroids
	#assign data points to nearest centroids
	clusterLabels = np.zeros(shape=(data.shape[0]))
	clusterScore = 0
	iterCount = 0
	converged = False
	sumOfDistance = 0
	while (not converged) and (iterCount < maxIterations):
		currentClusterScore = 0
		currentSumOfDistance = 0
		currentClusterLabels = np.zeros(shape=(data.shape[0]))
		clusters = defaultdict(list)		
		for i,x in enumerate(data):
			distances = []
			for j,c in enumerate(centroids):
				#print "x:"
				#print x
				#print "c:"
				#print c
				distance = euclideanDistance(x,c)
				distances.append(distance)
			d = np.array(distances)
			currentClusterLabels[i] = (d.argmin())
			clusters[d.argmin()].append(i)
			#print "clusters:"
			#print clusters
			sqD = (d.min())**2
			currentClusterScore+=sqD
			currentSumOfDistance+=d.min()
		
		#initialize datastructure to keep new centroids
		currentCentroids = np.zeros(shape=centroids.shape)
				
		for c,k in enumerate(clusters.keys()):
			currentCentroids[c] = np.mean(np.array(data[clusters[k],]),axis=0)
		#print "centroids:"
		#print centroids		
		#print "new centroids: "
		#print currentCentroids

		#if cluster centroids have not changed then break
		if np.array_equal(centroids, currentCentroids):
			#print "KMeans has converged:"
			#print "old score:"+str(clusterScore)
			#print "new score:"+str(currentClusterScore)
			converged = True			
			clusterScore = currentClusterScore
			sumOfDistance = currentSumOfDistance
			clusterLabels = currentClusterLabels
			centroids = currentCentroids
			iterCount +=1
		else:
			#print "old score: " + str(clusterScore)
			#print "new score: " + str(currentClusterScore)			
			clusterScore = currentClusterScore
			sumOfDistance = currentSumOfDistance
			clusterLabels = currentClusterLabels
			centroids = currentCentroids
			iterCount +=1
	#print "iterations: "+str(iterCount)
	return centroids, clusterLabels, clusterScore, sumOfDistance		
		
def euclideanDistance(x,y):
	return np.sqrt(np.sum((x-y)**2))

def sphericalKMeans(data, k, maxIterations = 100, noOfRandomRestarts = 10):
	for i,x in enumerate(data):
		#remove zero vectors:
		if not np.any(x):
			print "zero vector."
			data[i,] = data[i,]+1
		#normalize vectors:
		l = la.norm(x)
		data[i,] = data[i,]/l	
	#obtain random centroid indices
	centroidIndices = random.sample(range(data.shape[0]),k)
	#extract the initial centroids using above random indices
	centroids = data[centroidIndices,]
	#assign data points to nearest centroids
	clusterLabels = np.zeros(shape=(data.shape[0]))
	clusterScore = 0
	iterCount = 0
	converged = False
	sumOfDistance = 0
	while (not converged) and (iterCount < maxIterations):
		currentClusterScore = 0
		currentSumOfDistance = 0
		currentClusterLabels = np.zeros(shape=(data.shape[0]))
		clusters = defaultdict(list)		
		for i,x in enumerate(data):
			distances = []
			for j,c in enumerate(centroids):
				#print x
				#print c
				distance = 1 - spatial.distance.cosine(x,c)
				distances.append(distance)
			d = np.array(distances)
			currentClusterLabels[i] = (d.argmax())
			clusters[d.argmax()].append(i)
			sqD = (d.max())
			currentClusterScore+=sqD
			currentSumOfDistance+=d.max()
		
		#initialize datastructure to keep new centroids
		currentCentroids = np.zeros(shape=centroids.shape)
				
		for c,k in enumerate(clusters.keys()):
			currentCentroids[c] = np.sum(np.array(data[clusters[k],]),axis=0)
			m = la.norm(currentCentroids[c])
			currentCentroids[c] = currentCentroids[c]/m
		#if cluster centroids have not changed then break
		if np.array_equal(centroids, currentCentroids):
			converged = True			
			clusterScore = currentClusterScore
			sumOfDistance = currentSumOfDistance
			clusterLabels = currentClusterLabels
			centroids = currentCentroids
			iterCount +=1
		else:		
			clusterScore = currentClusterScore
			sumOfDistance = currentSumOfDistance
			clusterLabels = currentClusterLabels
			centroids = currentCentroids
			iterCount +=1
	return centroids, clusterLabels, clusterScore, sumOfDistance

if __name__ == "__main__":
	dummy = np.zeros(shape=(12,2))
	dummy[0,] = np.array([1,2])
	dummy[1,] = np.array([2,1])
	dummy[2,] = np.array([2,3])
	dummy[3,] = np.array([1.5,4])
	dummy[4,] = np.array([11,20])
	dummy[5,] = np.array([13,22.5])
	dummy[6,] = np.array([12,25])
	dummy[7,] = np.array([10,23])
	dummy[8,] = np.array([100,3])
	dummy[9,] = np.array([102,3])
	dummy[10,] = np.array([102.5,3.5])
	dummy[11,] = np.array([101,4])
	
	#dummy = np.zeros(shape=(9,2))
	#dummy[0,] = np.array([1,2])
	#dummy[1,] = np.array([2,1])
	#dummy[2,] = np.array([2,3])
	#dummy[3,] = np.array([11,20])
	#dummy[4,] = np.array([13,22.5])
	#dummy[5,] = np.array([12,25])
	#dummy[6,] = np.array([100,3])
	#dummy[7,] = np.array([102,3])
	#dummy[8,] = np.array([101,4])
	np.random.shuffle(dummy)
	print "dummy"
	print dummy
	centroids, clusterLabels, clusterScore, sumOfDistance = clusterByStandardKMeans(dummy,3)
	print clusterLabels
