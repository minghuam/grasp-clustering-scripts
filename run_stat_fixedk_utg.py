import os
import sys
import numpy as np
import matplotlib.pyplot as plt

from parse import *
from statistics import *

param_file = '../_UTG/params/All.txt'
label_dir = '../_UTG/labels/'
group_dir = '../_UTG/groups/'

nk = [5,10,20,30,50,80,100,120,150]
group_results_fkdpp = ['HAND_HANDHOG100_R100_C500_T31_fkdpp_k{0}/single/'.format(k) for k in nk]
group_results_fkmeans = ['HAND_HANDHOG100_R100_C500_T31_fkmeans1_k{0}/single/'.format(k) for k in nk]


params = parse_params(param_file)
#print params

labels = parse_utg_labels(label_dir, params)
labels = fix_utg_labels(labels, params)

# count grasp types
grasp_set = set()
for label in labels:
	for g in labels[label]:
		grasp_set.add(g[0])
print 'grasp types: ',len(grasp_set)

# fkdpp
grasp_stats_kdpp = list()
grasp_types_kdpp = list()
for i in range(len(nk)):	
	#seq = parse_sequence_knn(os.path.join(group_dir, group_results_fkdpp[i]))
	seq = parse_sequence_bbox(os.path.join(group_dir, group_results_fkdpp[i]))
	#print seq
	# change video name...
	for i in xrange(0, len(seq)):
		seq[i][0] = params[seq[i][0]][0]
	gs = stat_grasp_types(seq, labels)
	grasp_stats_kdpp.append(gs)
	grasp_types_kdpp.append(len(gs))

print 'KDPP:',grasp_types_kdpp

# kmeans
grasp_stats_kmeans = list()
grasp_types_kmeans = list()
for i in range(len(nk)):	
	#seq = parse_sequence_knn(os.path.join(group_dir, group_results_fkmeans[i]))
	seq = parse_sequence_bbox(os.path.join(group_dir, group_results_fkmeans[i]))
	#print seq
	# change video name...
	for i in xrange(0, len(seq)):
		seq[i][0] = params[seq[i][0]][0]
	gs = stat_grasp_types(seq, labels)
	grasp_stats_kmeans.append(gs)
	grasp_types_kmeans.append(len(gs))

print 'KMEANS:',grasp_types_kmeans


width = 0.8
plt.figure(1)
plt.grid()
plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)
ax = plt.subplot(111)
plt.title('UTG: Number of Grasp Types')
ax.scatter(nk, grasp_types_kmeans, s = 50, c = 'b', marker = u'D')
ax.plot(nk, grasp_types_kmeans, c = 'b', linewidth=3, label = 'K-Means')
ax.scatter(nk, grasp_types_kdpp, s = 50, c = 'g', marker = u'D')
ax.plot(nk, grasp_types_kdpp, c = 'g', linewidth=3, label = 'K-DPP')
ax.set_xticks(np.array(nk) + width/2)
ax.set_xticklabels(nk, rotation=0)
ax.set_xlabel('K - Number of Clusters')
#ax.set_ylabel('Number of Grasp Types')
ax.legend(loc=4)

'''
ink = 3;
width = 0.8
plt.figure(2)
ax = plt.subplot(221)
ax.bar(range(len(grasp_stats_kdpp[ink])), grasp_stats_kdpp[ink].values(), width = width)
ax.set_xticks(np.arange(len(grasp_stats_kdpp[ink].keys())) + width/2)
ax.set_xticklabels(grasp_stats_kdpp[ink].keys(), rotation=90)

ax = plt.subplot(222)
ax.bar(range(len(grasp_stats_kmeans[ink])), grasp_stats_kmeans[ink].values())
ax.set_xticks(np.arange(len(grasp_stats_kmeans[ink].keys())) + width/2)
ax.set_xticklabels(grasp_stats_kmeans[ink].keys(), rotation=90)
'''

plt.show()



