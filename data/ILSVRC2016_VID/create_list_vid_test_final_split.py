import argparse
import os
from random import shuffle
import shutil
import subprocess
import sys
import pdb
import math

CURDIR = os.path.dirname(os.path.realpath(__file__))

# If true, re-create all list files.
redo = False
# The root directory which holds all information of the dataset.
data_dir = "/mnt/disk_06/shangxuan/vid_imagenet2016"
# The directory name which holds the image sets.
imgset_list = "ImageSets/image_list.txt"
# The direcotry which contains the images.
img_dir = "Images"
img_ext = "JPEG"
# The directory which contains the annotations.
anno_dir = "Annotations"
anno_ext = "xml"

test_list_file = "{}/test_final_split".format(CURDIR)
test_name_size_file = "{}/test_name_size_final_split".format(CURDIR)
num_splits = 4

# get the image list
dataset = 'test'
imgset_file = "{}/{}/{}".format(data_dir, dataset, imgset_list)
with open(imgset_file) as fid:
    img_index_all = [line for line in fid.readlines()]

# test image list file
datasets = ["test"]
img_files = []
anno_files = []
for dataset in datasets:
    imgset_file = "{}/{}/{}".format(data_dir, dataset, imgset_list)
    count = 0
    with open(imgset_file, "r") as f:
        for line in f.readlines():
            name = line.strip("\n").split(" ")[0]
            img_file = "{}/{}/{}.{}".format(dataset, img_dir, name, img_ext)
            assert os.path.exists("{}/{}".format(data_dir, img_file))
            img_files.append(img_file)

            count += 1
            if count % 10000 ==0:
                print "Processed {} files.".format(count)

assert len(img_files) == len(img_index_all)

num_per_split = int( math.ceil(len(img_files) / num_splits) )
count = 0
for i in range(num_splits):
    idx = min(count+num_per_split, len(img_files))
    img_files_split = img_files[count:idx]
    img_index_split = img_index_all[count:idx]
    count += num_per_split
    test_list_file_split = '{}_{}.txt'.format(test_list_file, i)
    with open(test_list_file_split, "w") as f:
        for j in xrange(len(img_files_split)):
            f.write("{} 0\n".format(img_files_split[j]))
    print "Images written to {}".format(test_list_file_split)

    dataset = 'test'
    imgset_file_split = "{}/{}/ImageSets/image_list_split_{}.txt".format(data_dir, dataset, i)
    with open(imgset_file_split, "w") as f:
        for j in xrange(len(img_index_split)):
            f.write("{}\n".format(img_index_split[j]))
    print "Images written to {}".format(imgset_file_split)

    # Testing image size file 
    
    test_name_size_file_split = '{}_{}.txt'.format(test_name_size_file, i)
    
    cmd = "{}/../../build/tools/get_image_size --name_id_file={} {} {} {}".format(
        CURDIR, imgset_file_split, data_dir, test_list_file_split, test_name_size_file_split)
    print cmd
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
