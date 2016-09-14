cur_dir=$(cd $( dirname ${BASH_SOURCE[0]} ) && pwd )
echo $cur_dir
root_dir=$cur_dir/../..

cd $root_dir
echo $root_dir
redo=false
data_root_dir="/mnt/disk_06/shangxuan/vid_imagenet2016"
dataset_name="ILSVRC2016_VID"
mapfile="$root_dir/data/$dataset_name/labelmap_vid.prototxt"
db="lmdb"
min_dim=0
max_dim=0
width=0
height=0

extra_cmd="--encode-type=jpg --encoded"
if $redo
then
  extra_cmd="$extra_cmd --redo"
fi

for dataset in test_final_split_0 test_final_split_1 test_final_split_2 test_final_split_3
do
  python $root_dir/scripts/create_annoset.py --anno-type="classification" \
  --label-map-file=$mapfile --min-dim=$min_dim --max-dim=$max_dim \
  --resize-width=$width --resize-height=$height --check-label \
  $extra_cmd $data_root_dir $root_dir/data/$dataset_name/$dataset".txt" \
  $data_root_dir/$db/$dataset_name"_"$dataset"_"$db examples/$dataset_name \
  2>&1 | tee $root_dir/data/$dataset_name/$dataset.log
done

#for dataset in vid_train+det30_trainval_all
# for dataset in vid_train_104708+det30_trainval
# do
#   python $root_dir/scripts/create_annoset.py --anno-type="detection" \
#   --label-map-file=$mapfile --min-dim=$min_dim --max-dim=$max_dim \
#   --resize-width=$width --resize-height=$height --check-label \
#   $extra_cmd $data_root_dir $root_dir/data/$dataset_name/$dataset".txt" \
#   $data_root_dir/$db/$dataset_name"_"$dataset"_"$db examples/$dataset_name \
#   2>&1 | tee $root_dir/data/$dataset_name/$dataset.log
# done
