import os
import sys
import subprocess

vid_dir = "../_YHG/vid"
img_dir = "../_YHG/img"

vids = os.listdir(vid_dir)
vids = sorted(vids)
for vid in vids:
	name = vid.split('.')[0]
	src_vid = os.path.join(vid_dir, vid)
	dest_dir = os.path.join(img_dir, name)
	if not os.path.exists(dest_dir):
		os.mkdir(dest_dir)
	cmd = ['ffmpeg', '-i', src_vid, '-qscale', '1', os.path.join(dest_dir, '%d.jpg')]
	print cmd
	subprocess.call(cmd)