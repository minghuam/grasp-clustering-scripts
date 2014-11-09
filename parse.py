""" This file parses the output of hand detection and clustering
"""

import os
import sys

def parse_yale_labels(f, params):
	""" Parse grasp labels for YALE dataset
	
	Args:
		f: YALE dataset label file
		params: Dataset parameters

	Returns:
		A dict mapping vid to grasp tuples
	"""
	vids = [p[0] for p in params]
	labels = dict()
	with open(f) as fr:
		first_line = True
		for line in fr.readlines():
			if first_line:
				first_line = False
				continue
			words = line.split(',')
			vid = int(words[3])
			grasp = words[0]
			if vid in vids and grasp != 'no grasp':
				if vid not in labels:
					labels[vid] = list()
				ts = words[4].split(':')
				start_time = int(ts[0])*60 + float(ts[1]) + 1/25.0
				duration = float(words[6])
				end_time = start_time + duration - 1/25.0
				labels[vid].append([grasp, int(start_time*25), int(end_time*25)])

	"""
	for vid in labels:
		start = min([l[1] for l in labels[vid]])
		end = max([l[2] for l in labels[vid]])
		print vid, start, end
	"""
	return labels

def parse_utg_labels(d, params):
	""" Parse grasp labels in a directory

	Args:
		d: A directory which contains label files
		params: Dataset parameters

	Returns:
		A dict mapping vid to grasp tuples
	"""
	param_vids = [p[0] for p in params]
	labels = dict()
	for root, dirs, files in os.walk(d):
		for name in files:
			if name.endswith('.txt'):
				vid = int(name.split('_')[0])
				if vid not in param_vids:
					continue;
				if vid not in labels:
					labels[vid] = list()
				f = os.path.join(root, name)
				fr = open(f)
				for line in fr.readlines():
					words = line.split('\t')
					if len(words) == 3:
						labels[vid].append([words[0], int(words[1]), int(words[2])])
				fr.close()
	return labels

def fix_utg_labels(labels, params):
	""" Fix missing frame labels for the UTG dataset
	
	Args:
		labels: A list of lable tuples
		params: Dataset params

	Returns:
		A dict with continuous frame labels
	"""
	frames = dict()
	for param in params:
		frames[param[0]] = [param[1], param[2]]

	new_labels = dict()

	for vid in labels:
		if vid not in new_labels:
			new_labels[vid] = list()
		for i in range(len(labels[vid])):
			label = labels[vid][i]
			if i == 0:
				start = frames[vid][0]
				end = (labels[vid][i+1][1] + label[2])/2 - 1
				new_labels[vid].append([label[0], start, end])
			elif i == len(labels[vid]) - 1:
				start = (labels[vid][i-1][2] + label[1])/2
				end = frames[vid][1]
				new_labels[vid].append([label[0], start, end])
			else:
				start = (labels[vid][i-1][2] + label[1])/2
				end = (labels[vid][i+1][1] + label[2])/2 - 1
				new_labels[vid].append([label[0], start, end])

	#print new_labels
	return new_labels

def merge_utg_labels(labels, params):
	# print label set in python dict format
	"""
	label_set = set()
	for vid in labels:
		for label in labels[vid]:
			label_set.add(label[0])
	print label_set
	for label in label_set:
		print "'{0}':'{0}',\\".format(label,label)
	"""
	grasp_map = { \
		'thumb-index finger':'precision-thumb-fingers',\
		'thumb-3 finger':'precision-thumb-fingers',\
		'medium wrap':'medium wrap',\
		'#small diameter':'power-diameter',\
		'index finger extension':'index finger extension',\
		'large diameter':'power-diameter',\
		'ring':'ring',\
		'power sphere':'power sphere',\
		'#tip pinch':'precision-thumb-fingers',\
		'thumb-4 finger':'precision-thumb-fingers',\
		'light tool':'light tool',\
		'thumb-2 finger':'precision-thumb-fingers',\
		'tripod':'tripod',\
		'adduction':'adduction',\
		'#writing tripod':'#writing tripod',\
		'parallel extension':'precision-thumb-fingers',\
		'lateral pinch':'lateral pinch',\
		'extension type':'extension type',\
		'precision disk':'precision disk',\
		'lateral tripod':'tripod',\
	}

	new_labels = dict()
	for vid in labels:
		if vid not in new_labels:
			new_labels[vid] = list()
		for label in labels[vid]:
			label[0] = grasp_map[label[0]]
			new_labels[vid].append(label)

	return new_labels

def parse_params(f):
	"""Parse parameter file
	example: ../_UTG/	201			1	3387
	
	Returns:
		A list of tuples: [video_index(int), start_frame(int), end_frame(int)]
	"""
	fr = open(f)
	params = list()
	for line in fr.readlines():
		words = line.split('\t')
		if len(words) == 6:
			params.append([int(words[1]), int(words[4]), int(words[5])])
	fr.close()
	return params

def parse_sequence_knn(d):
	"""Parse KNN sequence file in a directory
	example: 1 23		32	0.17440		0	317	352	160	
	
	Returns:
		A list of tuples: [video_index(int), frame_index(int), cluster_index(int)]
	"""
	f = os.path.join(d, "sequence_knn.txt")
	fr = open(f)
	seq = list()
	for line in fr.readlines():
		words = line.split('\t')
		if len(words) > 3:
			wwords = words[0].split(' ')
			seq.append([int(wwords[0]), int(wwords[1]), int(words[2])])
	return seq

def parse_sequence_bbox(d):
	"""Parse cluster files in a directory
	example file name: bbox_info_0.txt
	example line: 0 101 0 395 116 352 160 0.136084
	
	Returns:
		A list of tuples: [video_index(int), frame_index(int), cluster_index(int)]
	"""
	seq = list()
	for root, dirs, files in os.walk(d):
		for name in files:
			if name.endswith('.txt') and name.startswith('bbox_info'):
				cluster = int(name.split('.')[0].split('_')[2])
				f = os.path.join(root, name)
				fr = open(f)
				for line in fr.readlines():
					words = line.split(' ')
					vid = int(words[0])
					frame = int(words[1])
					seq.append([vid, frame, cluster])
				fr.close()
	return seq

