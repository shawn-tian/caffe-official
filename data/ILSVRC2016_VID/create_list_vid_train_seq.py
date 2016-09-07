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

#train_list_file = "{}/vid_train+det30_trainval_all_seq.txt".format(CURDIR)
train_list_file = "{}/vid_train_seq.txt".format(CURDIR)
val_list_file = "{}/vid_val.txt".format(CURDIR)
val_name_size_file = "{}/vid_val_name_size.txt".format(CURDIR)
test_list_file = "{}/test.txt".format(CURDIR)
test_name_size_file = "{}/test_name_size.txt".format(CURDIR)
train_name_size_file = "{}/vid_train_name_size_seq.txt".format(CURDIR)
# Create training set.
# We follow Ross Girschick's split in R-CNN.

# remove duplicated image list files
if 0:
    imgset_file = "{}/{}/{}".format(data_dir, "train", imgset_list)
    img_list = set()
    with open(imgset_file, "r") as f:
        for line in f.readlines():
            name = line.strip("\n").split(" ")[0]
            img_list.add(name)
    print("image list size: {}".format(len(img_list)))
    idx = 1
    fid_out = open(imgset_file+'_rm', 'w')
    for item in img_list:
        fid_out.write(item + " " + str(idx)  + '\n' );
        idx += 1
    fid_out.close()
    sys.exit(0)

if redo or not os.path.exists(train_list_file):
    datasets = ["train"] #, "det30_train_val/train", "det30_train_val/val"]
    img_files = []
    anno_files = []
    im_id = []
    for dataset in datasets:
        imgset_file = "{}/{}/{}".format(data_dir, dataset, imgset_list)
        count = 0
        with open(imgset_file, "r") as f:
            for line in f.readlines():
                name = line.strip("\n").split(" ")[0]
                anno_file = "{}/{}/{}.{}".format(dataset, anno_dir, name, anno_ext)
                # Ignore image if it does not have annotation. These are the negative images in ILSVRC.
                if not os.path.exists("{}/{}".format(data_dir, anno_file)):
                    continue
                img_file = "{}/{}/{}.{}".format(dataset, img_dir, name, img_ext)
                assert os.path.exists("{}/{}".format(data_dir, img_file))
                img_files.append(img_file)
                anno_files.append(anno_file)

                count += 1
                if count % 1000 ==0:
                    print "Processed {} files.".format(count)

    # Shuffle the images.
    idx = [i for i in xrange(len(img_files))]
    # shuffle(idx)
    with open(train_list_file, "w") as f:
        for i in idx:
            f.write("{} {}\n".format(img_files[i], anno_files[i]))
    print "In total {:d} images loaded.".format(len(img_files))
else:
    print "Training image list file already exists: {}".format(train_list_file)

# get training image name size file for testing 
if redo or not os.path.exists(train_name_size_file):
    dataset = 'train'
    imgset_file = "{}/{}/{}".format(data_dir, dataset, imgset_list)
    cmd = "{}/../../build/tools/get_image_size --name_id_file={} {} {} {}".format(
            CURDIR, imgset_file, data_dir, train_list_file, train_name_size_file)
    print cmd
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
else:
    print "Training image size file already exists: {}".format(train_name_size_file)

sys.exit(0)
# if redo or not os.path.exists(val_list_file):
#     datasets = ["val2"]
#     subset = "val"
#     img_files = []
#     anno_files = []
#     for dataset in datasets:
#         imgset_file = "{}/{}/{}.txt".format(data_dir, imgset_dir, dataset)
#         with open(imgset_file, "r") as f:
#             for line in f.readlines():
#                 name = line.strip("\n").split(" ")[0]
#                 img_file = "{}/{}/{}.{}".format(img_dir, subset, name, img_ext)
#                 assert os.path.exists("{}/{}".format(data_dir, img_file))
#                 anno_file = "{}/{}/{}.{}".format(anno_dir, subset, name, anno_ext)
#                 assert os.path.exists("{}/{}".format(data_dir, anno_file))
#                 img_files.append(img_file)
#                 anno_files.append(anno_file)
#     with open(val_list_file, "w") as f:
#         for i in xrange(len(img_files)):
#             f.write("{} {}\n".format(img_files[i], anno_files[i]))

# if redo or not os.path.exists(val_name_size_file):
#     dataset = 'val2'
#     imgset_file = "{}/{}/{}.txt".format(data_dir, imgset_dir, dataset)
#     cmd = "{}/../../build/tools/get_image_size --name_id_file={} {} {} {}".format(
#             CURDIR, imgset_file, data_dir, val_list_file, val_name_size_file)
#     print cmd
#     process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
#     output = process.communicate()[0]

if redo or not os.path.exists(val_list_file):
    datasets = ["val"]
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
                anno_file = "{}/{}/{}.{}".format(dataset, anno_dir, name, anno_ext)
                assert os.path.exists("{}/{}".format(data_dir, anno_file))
                img_files.append(img_file)
                anno_files.append(anno_file)
                
                count += 1
                if count % 1000 ==0:
                    print "Processed {} files.".format(count)

    with open(val_list_file, "w") as f:
        for i in xrange(len(img_files)):
            f.write("{} {}\n".format(img_files[i], anno_files[i]))
        print "Images written to {}".format(val_list_file)
else:
    print "Testing image list file already exists: {}".format(val_list_file)

if redo or not os.path.exists(val_name_size_file):
    dataset = 'val'
    imgset_file = "{}/{}/{}".format(data_dir, dataset, imgset_list)
    cmd = "{}/../../build/tools/get_image_size --name_id_file={} {} {} {}".format(
            CURDIR, imgset_file, data_dir, val_list_file, val_name_size_file)
    print cmd
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
else:
    print "Testing image size file already exists: {}".format(val_name_size_file)
