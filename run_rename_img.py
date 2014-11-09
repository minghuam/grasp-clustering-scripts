import os
import sys
import subprocess

img_dir = "../_YHG/img"

img_folders = os.listdir(img_dir)
img_folders = sorted(img_folders)
for folder in img_folders:
	imgs = os.listdir(os.path.join(img_dir, folder))
	for img in imgs:
		src = os.path.join(img_dir, folder, img)
		dest = os.path.join(img_dir, folder, img.split('.')[0] + '.jpg')
		print src, " => ", dest
		os.rename(src, dest)