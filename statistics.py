""" Clustering evaluation statistics
"""

import os
import sys
import math
import operator

def stat_grasp_types(seq, labels):
	"""Count number of grasp types in seq
	For each cluster, we pick the majority grasp type as the type
	of this cluster. 

	Returns:
		A dictionary mapping grasp type(string) to count(int).
	"""
	clusters = dict()
	# calculate cluster dictionary
	# key: cluster, value: [vid, frame]
	for s in seq:
		if s[2] not in clusters:
			clusters[s[2]] = list()
		clusters[s[2]].append([s[0], s[1]])

	grasp_stat = dict()
	# voting for each cluster
	# TODO: better algorithms??
	for c in clusters:
		grasp_dict = dict()
		for vid_frame in clusters[c]:
			# get grasp type
			for grasp in labels[vid_frame[0]]:
				if vid_frame[1] >= grasp[1] and vid_frame[1] <= grasp[2]:
						if grasp[0] not in grasp_dict:
							grasp_dict[grasp[0]] = 0
						grasp_dict[grasp[0]] += 1
		if len(grasp_dict) > 0:
			grasp = max(grasp_dict, key=grasp_dict.get)
			# grasp, count
			if grasp not in grasp_stat:
				grasp_stat[grasp] = 0
			grasp_stat[grasp] += 1

	return grasp_stat


def stat_purity(seq, labels, cluster_size_threshold = 1):
	"""Calculate clustering purity
	http://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-clustering-1.html
	
	Args:
		seq: Clustering result sequence
		labels: Ground truth labels
		cluster_size_threshold: Clusters with size smaller than this will be ignored

	Returns:
		A tuple: [cluster_count(int), purity_count(int), all_count(int)]
	"""
	clusters = dict()
	# calculate cluster dictionary
	# key: cluster, value: [vid, frame]
	for s in seq:
		if s[2] not in clusters:
			clusters[s[2]] = list()
		clusters[s[2]].append([s[0], s[1]])

	all_count = 0
	purity_count = 0
	cluster_count = 0
	for c in clusters:
		if len(clusters[c]) < cluster_size_threshold:
			continue
		grasp_count = dict();
		# get majority grasp
		for vid_frame in clusters[c]:
			for grasp in labels[vid_frame[0]]:
				if vid_frame[1] >= grasp[1] and vid_frame[1] <= grasp[2]:
						if grasp[0] not in grasp_count:
							grasp_count[grasp[0]] = 0
						grasp_count[grasp[0]] += 1

		if len(grasp_count) > 0:
			max_grasp = max(grasp_count, key=grasp_count.get)
			#print 'cluster: {0}, major grasp: {1}, count:{2}'.format(c, max_grasp ,grasp_count[max_grasp])
			# get majority count
			this_majority  = 0
			this_all = 0
			cluster_count += 1
			for vid_frame in clusters[c]:
				for grasp in labels[vid_frame[0]]:
					if vid_frame[1] >= grasp[1] and vid_frame[1] <= grasp[2]:
						all_count += 1
						this_all += 1
						if grasp[0] == max_grasp:
							purity_count += 1
							this_majority += 1
			#print 'cluster: {0}, majority: {2}/{3}'.format(c,len(clusters[c]), this_majority, this_all)
	print 'Majority Count:',purity_count
	print 'All Count:', all_count
	print 'Purity:', float(purity_count)/all_count

	return [cluster_count, purity_count, all_count]

def stat_nmi(seq, labels, cluster_size_threshold = 1):
	"""Calculate clustering NMI
	http://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-clustering-1.html
	
	Args:
		seq: Clustering result sequence
		labels: Ground truth labels
		cluster_size_threshold: Clusters with size smaller than this will be ignored

	Returns:
		A tuple: [NW(int), NC(int), HW(float), HC(float), I(float), PERPLEXITY(float), NMI(float)]
	"""
	clusters = dict()
	# calculate cluster dictionary
	# key: cluster, value: [vid, frame]
	for s in seq:
		if s[2] not in clusters:
			clusters[s[2]] = list()
		clusters[s[2]].append([s[0], s[1]])


	W = list()
	NW = 0.0
	for c in clusters:
		if len(clusters[c]) < cluster_size_threshold:
			continue
		grasp_count = dict();
		# get majority grasp
		for vid_frame in clusters[c]:
			for grasp in labels[vid_frame[0]]:
				if vid_frame[1] >= grasp[1] and vid_frame[1] <= grasp[2]:
						if grasp[0] not in grasp_count:
							grasp_count[grasp[0]] = 0
						grasp_count[grasp[0]] += 1
						NW += 1
		if grasp_count > 0:
			W.append(grasp_count)

	C = dict()
	for vid in labels.keys():
		for grasp in labels[vid]:
			if grasp[0] not in C:
				C[grasp[0]] = 0
			C[grasp[0]] += (grasp[2] - grasp[1] + 1)
	#print C

	NC = float(sum(C.values()))

	I = 0.0
	for w in W:
		wk = sum(w.values())
		for c in C:
			cj = C[c]
			wk_cj = 0.0
			for wc in w:
				if wc == c:
					wk_cj += w[wc]
			if wk_cj > 0:
				#print wk,cj,wk_cj,NW,float(NW)*wk_cj/(wk*cj)
				P_wk_cj = wk_cj/NW
				P_wk = wk/NW
				P_cj = cj/NC
				I = I + P_wk_cj*math.log(P_wk_cj/(P_wk*P_cj), 2)

	HW = 0.0
	for w in W:
		wk = sum(w.values())
		if wk != 0:
			HW = HW - (wk/NW)*math.log(wk/NW, 2)
	
	HC = 0.0
	for c in C:
		cj = C[c]
		HC = HC - (cj/NC)*math.log(cj/NC, 2)

	NMI = I/(HW+HC)/2

	PERPLEXITY = math.pow(2, HW)

	print 'NW=',NW
	print 'NC=',NC
	print 'I=',I
	print 'HW=',HW
	print 'HC=',HC
	print 'PERPLEXITY=',PERPLEXITY
	print 'NMI=',NMI

	return [int(NW), int(NC), HW, HC, I, PERPLEXITY, NMI]

def stat_PR(seq, labels, cluster_size_threshold = 1):
	"""Calculate clustering Precision-Recall
	http://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-clustering-1.html
	
	Args:
		seq: Clustering result sequence
		labels: Ground truth labels
		cluster_size_threshold: Clusters with size smaller than this will be ignored

	return [TP, FP, TN, FN, PRECISION, RECALL, F1]

	Returns:
		A tuple: [TP(int), FP(int), TN(int), FN(int), PRECISION(float), RECALL(float), F1(float)]
	"""
	raw_clusters = dict()
	# calculate cluster dictionary
	# key: cluster, value: [vid, frame]
	for s in seq:
		if s[2] not in raw_clusters:
			raw_clusters[s[2]] = list()
		raw_clusters[s[2]].append([s[0], s[1]])

	cclusters = list()
	ccluster_size = list()
	for c in raw_clusters:
		if len(raw_clusters[c]) < cluster_size_threshold:
			continue	
		grasp_count = dict();
		# get majority grasp
		for vid_frame in raw_clusters[c]:
			for grasp in labels[vid_frame[0]]:
				if vid_frame[1] >= grasp[1] and vid_frame[1] <= grasp[2]:
						if grasp[0] not in grasp_count:
							grasp_count[grasp[0]] = 0
						grasp_count[grasp[0]] += 1
		if len(grasp_count) > 0:
			cclusters.append(sorted(grasp_count.items(), key=operator.itemgetter(1), reverse=True))
			ccluster_size.append(sum(grasp_count.values()))

	#print cclusters
	#print ccluster_size

	TP_FP = 0
	TP = 0
	for i in range(len(cclusters)):
		size = ccluster_size[i]
		if size > 1:
			TP_FP += (size*(size-1))
		size = cclusters[i][0][1]
		if size > 1:
			TP += (size*(size-1))
	FN = 0
	for i in range(len(cclusters)-1):
		for j in range(i+1, len(cclusters)):
			for member_i in cclusters[i]:
				for member_j in cclusters[j]:
					if member_i[0] == member_j[0]:
						FN += (member_i[1] * member_j[1])

	total = sum(ccluster_size)

	TOTAL = total * (total - 1)
	FP = TP_FP - TP
	TN = TOTAL - TP - FP - FN

	PRECISION = float(TP)/(TP + FP)
	RECALL = float(TP)/(TP + FN)
	ACCURACY = float(TP + TN)/(TOTAL)
	F1 = (1+1*1)*PRECISION*RECALL/(1*1*PRECISION + RECALL)

	#print 'TOTAL =',TOTAL
	print 'TP =',TP
	print 'FP =',FP
	print 'TN =',TN
	print 'FN =',FN
	print 'PRECISION =',PRECISION
	print 'RECALL =',RECALL
	print 'ACCURACY =',ACCURACY
	print 'F1 =',F1

	return [TP, FP, TN, FN, PRECISION, RECALL, ACCURACY, F1]