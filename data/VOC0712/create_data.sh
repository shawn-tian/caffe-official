cur_dir=$(cd $( dirname ${BASH_SOURCE[0]} ) && pwd )
root_dir=$cur_dir/../..

cd $root_dir
echo "cur_dir: $cur_dir, root_dir: $root_dir"
redo=1
data_root_dir="$HOME/visenzeWork/voc_data/voc_data_ssd/VOCdevkit/"
out_db_dir="/mnt/disk_06/shangxuan/train_jobs/voc/db/"
dataset_name="VOC0712"
mapfile="$root_dir/data/$dataset_name/labelmap_voc.prototxt"
anno_type="detection"
db="lmdb"
min_dim=0
max_dim=0
width=0
height=0

extra_cmd="--encode-type=jpg --encoded"
if [ $redo ]
then
  extra_cmd="$extra_cmd --redo"
fi
for subset in trainval #test trainval
do
  python $root_dir/scripts/create_annoset.py --anno-type=$anno_type \
  --label-map-file=$mapfile --min-dim=$min_dim --max-dim=$max_dim \
  --resize-width=$width --resize-height=$height --check-label \
  $extra_cmd $data_root_dir $root_dir/data/$dataset_name/$subset.txt \
  $out_db_dir/ssd_$db/$dataset_name"_"$subset"_"$db examples/$dataset_name
done
