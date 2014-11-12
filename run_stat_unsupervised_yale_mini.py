import os
import sys
import numpy as np
import matplotlib.pyplot as plt

from parse import *
from statistics import *

param_file = '../_YHG_MINI/params/All.txt'
label_file = '../_YHG/fullDatasetBlack.csv'
group_dir = '../_YHG_MINI/groups/'


group_results = [\
	'HAND_HANDHOG100_R100_C500_T40_fdpp/single/',\
	'HAND_HANDHOG100_R100_C500_T40_kmeans/single/', \
	'HAND_HANDHOG100_R100_C500_T40_nrpc/single/', \
	'HAND_HANDHOG100_R100_C500_T40_dpmm/single/' \
]

alogs = ['FDPP', 'KMEANS', 'NRPC', 'DPMM']

params = parse_params(param_file)
labels = parse_yale_labels(label_file, params)

# count grasp types
grasp_set = set()
for label in labels:
	for g in labels[label]:
		grasp_set.add(g[0])
print 'grasp types: ',len(grasp_set)

# statistics
grasp_stats_types = list()
grasp_stats_purity = list()
grasp_stats_nmi = list()
grasp_stats_pr = list()
for i in range(len(group_results)):
	print '\n***************',group_results[i],'***************'
	seq = parse_sequence_bbox(os.path.join(group_dir, group_results[i]))

	# change video name...
	for i in xrange(0, len(seq)):
		seq[i][0] = params[seq[i][0]][0]

	grasp_stats_types.append(stat_grasp_types(seq, labels))
	grasp_stats_purity.append(stat_purity(seq, labels, 3))
	grasp_stats_nmi.append(stat_nmi(seq, labels, 2))
	grasp_stats_pr.append(stat_PR(seq, labels, 2))

plt.figure(1)
width = 0.8
plot_index = 241

# draw number of clusters
cluster_size = [s[0] for s in grasp_stats_purity]
ax = plt.subplot(plot_index)
plot_index += 1
plt.title('YALE: Number of Clusters')
ax.bar(range(len(cluster_size)), cluster_size, width = width)
ax.set_xticks(np.arange(len(cluster_size)) + width/2)
ax.set_xticklabels(alogs, rotation=0)

# draw types of grasps
grasp_types = [len(s) for s in grasp_stats_types]
ax = plt.subplot(plot_index)
plot_index += 1
plt.title('Types of Grasp')
ax.bar(range(len(grasp_types)), grasp_types, width = width)
ax.set_xticks(np.arange(len(grasp_types)) + width/2)
ax.set_xticklabels(alogs, rotation=0)

# draw purity
purity = [float(s[1])/float(s[2]) for s in grasp_stats_purity]
ax = plt.subplot(plot_index)
plot_index += 1
plt.title('Purity')
ax.bar(range(len(purity)), purity, width = width)
ax.set_xticks(np.arange(len(purity)) + width/2)
ax.set_xticklabels(alogs, rotation=0)

# draw nmi
nmi = [s[-1] for s in grasp_stats_nmi]
ax = plt.subplot(plot_index)
plot_index += 1
plt.title('NMI')
ax.bar(range(len(nmi)), nmi, width = width)
ax.set_xticks(np.arange(len(nmi)) + width/2)
ax.set_xticklabels(alogs, rotation=0)

# draw precision
precision = [s[-4] for s in grasp_stats_pr]
ax = plt.subplot(plot_index)
plot_index += 1
plt.title('Precision')
ax.bar(range(len(precision)), precision, width = width)
ax.set_xticks(np.arange(len(precision)) + width/2)
ax.set_xticklabels(alogs, rotation=0)

# draw recall
recall = [s[-3] for s in grasp_stats_pr]
ax = plt.subplot(plot_index)
plot_index += 1
plt.title('Recall')
ax.bar(range(len(recall)), recall, width = width)
ax.set_xticks(np.arange(len(recall)) + width/2)
ax.set_xticklabels(alogs, rotation=0)

# draw F1
f1 = [s[-1] for s in grasp_stats_pr]
ax = plt.subplot(plot_index)
plot_index += 1
plt.title('F1')
ax.bar(range(len(f1)), f1, width = width)
ax.set_xticks(np.arange(len(f1)) + width/2)
ax.set_xticklabels(alogs, rotation=0)

# draw accuracy
accuracy = [s[-2] for s in grasp_stats_pr]
ax = plt.subplot(plot_index)
plot_index += 1
plt.title('Accuracy')
ax.bar(range(len(accuracy)), accuracy, width = width)
ax.set_xticks(np.arange(len(accuracy)) + width/2)
ax.set_xticklabels(alogs, rotation=0)

plt.show()
