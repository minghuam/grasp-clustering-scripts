import os
import sys
import shutil

src_filter_dir = "../_YHG/z_filter"
src_img_dir = "../_YHG/img"
src_feat_dir = "../_YHG/features"
src_bbox_dir = "../_YHG/bbox/hand"

mini_img_dir = "../_YHG_MINI/img"
mini_bbox_dir = "../_YHG_MINI/bbox/hand"
mini_feat_dir = "../_YHG_MINI/features/"
feat = "bbox_HAND_feat_HANDHOG"

# parse source images
imgs = os.listdir(src_filter_dir)
for img in imgs:
	names = img.split('_')
	vid = names[0]
	frame = names[1]
	src_dir = os.path.join(src_img_dir, vid)
	dest_dir = os.path.join(mini_img_dir, vid)
	if not os.path.exists(dest_dir):
		os.mkdir(dest_dir)	
	print os.path.join(src_dir, frame)
	shutil.copy(os.path.join(src_dir, frame), dest_dir)

	bf = list("00000000");
	fs = frame.split('.')[0];
	for i in range(len(fs)):
		bf[len(bf)-1-i] = fs[len(fs)-1-i]
	bbox_file = "bbox_{0}_{1}.txt".format(vid, ''.join(bf))
	feat_file = "{0}_{1}.xml".format(feat, ''.join(bf))

	print bbox_file
	print feat_file

	if os.path.exists(os.path.join(src_bbox_dir, bbox_file)):
		shutil.copy(os.path.join(src_bbox_dir, bbox_file), mini_bbox_dir)

	dest_dir = os.path.join(mini_feat_dir, vid)
	if not os.path.exists(dest_dir):
		os.mkdir(dest_dir)
		os.mkdir(os.path.join(dest_dir, feat))

	src_feat_file = os.path.join(src_feat_dir, vid, feat, feat_file)
	if os.path.exists(src_feat_file):
		print src_feat_file
		dest_feat_dir = os.path.join(mini_feat_dir, vid, feat)
		shutil.copy(src_feat_file, dest_feat_dir)