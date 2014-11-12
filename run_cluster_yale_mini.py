#!/usr/bin/python

import subprocess
import os

args_list1 = [\
'-groupsingle -srate 100 -maxgrp 500 -rad 0.39 -bbox HAND -feat HANDHOG -alg fkdpp -k 5',\
'-groupsingle -srate 100 -maxgrp 500 -rad 0.39 -bbox HAND -feat HANDHOG -alg fkdpp -k 10',\
'-groupsingle -srate 100 -maxgrp 500 -rad 0.39 -bbox HAND -feat HANDHOG -alg fkdpp -k 20',\
'-groupsingle -srate 100 -maxgrp 500 -rad 0.39 -bbox HAND -feat HANDHOG -alg fkdpp -k 30',\
'-groupsingle -srate 100 -maxgrp 500 -rad 0.39 -bbox HAND -feat HANDHOG -alg fkdpp -k 50',\
'-groupsingle -srate 100 -maxgrp 500 -rad 0.39 -bbox HAND -feat HANDHOG -alg fkdpp -k 80',\
'-groupsingle -srate 100 -maxgrp 500 -rad 0.39 -bbox HAND -feat HANDHOG -alg fkdpp -k 100',\
'-groupsingle -srate 100 -maxgrp 500 -rad 0.39 -bbox HAND -feat HANDHOG -alg fkdpp -k 120',\
'-groupsingle -srate 100 -maxgrp 500 -rad 0.39 -bbox HAND -feat HANDHOG -alg fkdpp -k 150',\
'-groupsingle -srate 100 -maxgrp 500 -rad 0.39 -bbox HAND -feat HANDHOG -alg fkmeans1 -k 5', \
'-groupsingle -srate 100 -maxgrp 500 -rad 0.39 -bbox HAND -feat HANDHOG -alg fkmeans1 -k 10', \
'-groupsingle -srate 100 -maxgrp 500 -rad 0.39 -bbox HAND -feat HANDHOG -alg fkmeans1 -k 20', \
'-groupsingle -srate 100 -maxgrp 500 -rad 0.39 -bbox HAND -feat HANDHOG -alg fkmeans1 -k 30', \
'-groupsingle -srate 100 -maxgrp 500 -rad 0.39 -bbox HAND -feat HANDHOG -alg fkmeans1 -k 50', \
'-groupsingle -srate 100 -maxgrp 500 -rad 0.39 -bbox HAND -feat HANDHOG -alg fkmeans1 -k 80', \
'-groupsingle -srate 100 -maxgrp 500 -rad 0.39 -bbox HAND -feat HANDHOG -alg fkmeans1 -k 100', \
'-groupsingle -srate 100 -maxgrp 500 -rad 0.39 -bbox HAND -feat HANDHOG -alg fkmeans1 -k 120', \
'-groupsingle -srate 100 -maxgrp 500 -rad 0.39 -bbox HAND -feat HANDHOG -alg fkmeans1 -k 150'
]

args_list2 = [\
'-groupsingle -srate 100 -maxgrp 500 -rad 0.40 -bbox HAND -feat HANDHOG -alg fdpp -ts 500', \
'-groupsingle -srate 100 -maxgrp 500 -rad 0.40 -bbox HAND -feat HANDHOG -alg kmeans -ts 500', \
'-groupsingle -srate 100 -maxgrp 500 -rad 0.40 -bbox HAND -feat HANDHOG -alg nrpc -ts 500', \
'-groupsingle -srate 100 -maxgrp 500 -rad 0.40 -bbox HAND -feat HANDHOG -alg dpmm -ts 500' \
]

# bandwidth = 3000

work_dir = '../bbox_ide'
exe = "./bin/Debug/bbox_ide"

os.chdir(work_dir)
subprocess.call(['pwd'])

for args in args_list2[:]:
	cmd = exe + ' ' + args;
	cmd = cmd.split(' ')
	print cmd
	subprocess.call(cmd)
