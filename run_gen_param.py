""" List image directory and generage parameter file for a dataset
"""

import os

img_dir = "../_YHG/img"
param_dir = "../_YHG/"

for root, dirs, files in os.walk(img_dir):
	dirs = sorted(dirs)
	for d in dirs:
		size = len(os.listdir(os.path.join(root, d)))
		print "{0}	{1}			{2}	{3}".format(param_dir, d, 1, size)