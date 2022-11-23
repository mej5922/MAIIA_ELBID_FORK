echo "Prediccion Preprocesado"
images_path=$1
output_dir=$2
size=$3
step_size=$4

satproc_extract_chips $images_path     -o $output_dir     --size $size     --step-size $step_size  --rescale     --rescale-mode percentiles --lower-cut 2 --upper-cut 98
