import os
import sys
from parse import *

data_dir = '../_YHG/'
label_file = '../_YHG/fullDatasetBlack.csv'
param_file = '../_YHG/params/All.txt'
output_file = '../_YHG/params/output.txt'

params = parse_params(param_file)
labels = parse_yale_labels(label_file, params)


with open(output_file, 'wb') as fr:
	for vid in labels:
		label = labels[vid]
		for grasp in label:
			line = "{0}	{1:03d}			{2}	{3}\n".format(data_dir, vid, grasp[1], grasp[2])
			fr.write(line)

'''
with open(output_file, 'wb') as fr:
	for vid in labels:
		label = labels[vid]
		grasp0 = label[0]
		grasp1 = label[len(label)-1]
		line = "{0}	{1:03d}			{2}	{3}\n".format(data_dir, vid, grasp0[1], grasp1[2])
		fr.write(line)
'''