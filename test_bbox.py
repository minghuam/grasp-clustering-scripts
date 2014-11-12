import os
import sys
import subprocess
import cv2
import cv2.cv as cv

from parse import *

label_file = '../_YHG/fullDatasetBlack.csv'
"""
param_file = '../_YHG_MINI/params/All.txt'
bbox_dir = "../_YHG_MINI/bbox/hand"
img_dir = "../_YHG_MINI/img"
"""

param_file = '../_YHG/params/All.txt'
bbox_dir = "../_YHG/bbox/hand"
img_dir = "../_YHG/img"
feat_dir = "../_YHG/features"
feat = "bbox_HAND_feat_HANDHOG"

bbox_video_dir = "../_YHG/bbox"

bbox_files = os.listdir(bbox_dir)

#vid = "001"
if len(sys.argv) < 2:
	vid = "001"
else:
	vid = sys.argv[1]

params = parse_params(param_file)
labels = parse_yale_labels(label_file, params)

labels = labels[int(vid)]
print labels

vid_bbox_files = [f for f in bbox_files if f.startswith("bbox_" + vid)]
vid_bbox_files = sorted(vid_bbox_files)
vid_feat_files = os.listdir(os.path.join(feat_dir, vid, feat))
vid_feat_files = sorted(vid_feat_files)

write_to_video = False
output_video_file = os.path.join(bbox_video_dir, vid+".avi")
if write_to_video:
	vid_writer = cv2.VideoWriter(output_video_file, cv.CV_FOURCC('X', 'V', 'I', 'D'), 25, (640, 480))

index = 0
while True:
	bf = vid_bbox_files[index]
	frame = int(bf.split('_')[2].split('.')[0])

	feat_file = "{0}_{1:08d}.xml".format(feat, frame)
	if feat_file not in vid_feat_files:
		print 'skip: {0}, no feature file found!'.format(index+1)
		index += 1
		if index > len(vid_bbox_files) - 1:
			break
		continue

	img_path = os.path.join(img_dir, vid, str(frame) + '.jpg')
	I = cv2.imread(os.path.join(img_dir, vid, str(frame) + '.jpg'))

	with open(os.path.join(bbox_dir, bf)) as fr:
		lines = fr.readlines()
		for line in lines:
			words = line.split('\t')
			x = int(words[3])
			y = int(words[4])
			w = int(words[5])
			h = int(words[6])
			cv2.rectangle(I, (x,y), (x+w, y+h), (0,0,255), 2)
			cv2.putText(I, vid + '/' + str(frame), (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
			grasp_type = 'no grasp'
			for grasp in labels:
				if frame >= grasp[1] and frame <= grasp[2]:
					grasp_type = grasp[0]

			cv2.putText(I, grasp_type, (10,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

	if write_to_video:
		print "{0}/{1}".format(index+1, len(vid_bbox_files))
		vid_writer.write(I)
		index += 1
		if index > len(vid_bbox_files) - 1:
			break
	else:
		cv2.imshow('image', I)

		cv2.waitKey(0)

		#feat_path = os.path.join(feat_dir, vid, feat, feat_file)
		#subprocess.call(['./draw_hog', feat_path])

		key = cv2.waitKey(0) & 255
		
		if key == 27:
			break
		elif key == 81: # left
			index -= 1
		elif key == 83: # right
			index += 1
		elif key == 82: # up
			index += 10
		elif key == 84: # down
			index -= 10
		
		if index < 0:
			index = len(vid_bbox_files) - 1

		if index > len(vid_bbox_files) - 1:
			index = 0