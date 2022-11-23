echo "Preprocesamiento de imagenes para MAIIA"
echo "preproces.sh images_path labels_path size step_size"

images_path=$1
labels_path=$2
size=$3
step_size=$4

output_dir=$5

aoi_path=$labels_path




satproc_extract_chips  $images_path  -o $output_dir  --size $size  --step-size $step_size --aoi $aoi_path  --labels $labels_path  --label-property "class"  --classes A   --rescale  --rescale-mode percentiles --lower-cut 2 --upper-cut 98
