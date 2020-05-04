#!/bin/bash
module load python3.5/canopy-2.1.3
#in path specify the path where your Landsat files are
path=/glusterfs/surft/users/mp877190/data/coral_reef/* 
for f in $path  
do echo This is the folder $f
[ -d $f ] && cd "$f/scenes" && ls *  
meta=`find *_MTL.txt` && echo $meta 
bands=${meta:0:40}'_B{}.TIF' && echo $bands  
output=${meta:0:40} && echo $output
#change code path to where your code is stored (whole path)
code_path=/home/users/mp877190/getting_netcdf/Landsat_code/main_coral_reef.py
python $code_path "$f/scenes" $bands $meta $output
cd ..
done
