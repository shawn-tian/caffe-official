import argparse
import os
from random import shuffle
import shutil
import subprocess
import sys
import pdb

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

test_list_file = "{}/test_final.txt".format(CURDIR)
test_name_size_file = "{}/test_name_size_final.txt".format(CURDIR)

if redo or not os.path.exists(test_list_file):
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

    with open(test_list_file, "w") as f:
        for i in xrange(len(img_files)):
            f.write("{} 0\n".format(img_files[i]))
        print "Images written to {}".format(test_list_file)
else:
    print "Testing image list file already exists: {}".format(test_list_file)

if redo or not os.path.exists(test_name_size_file):
    dataset = 'test'
    imgset_file = "{}/{}/{}".format(data_dir, dataset, imgset_list)
    cmd = "{}/../../build/tools/get_image_size --name_id_file={} {} {} {}".format(
            CURDIR, imgset_file, data_dir, test_list_file, test_name_size_file)
    print cmd
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
else:
    print "Testing image size file already exists: {}".format(test_name_size_file)
