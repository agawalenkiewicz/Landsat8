#!/bin/bash
module load python3.5/canopy-2.1.3
path=/glusterfs/surft/users/mp877190/data/datastore/EE/LANDSAT_8_C1/hunterston_checked/* 
for f in $path  
do echo This is the folder $f
[ -d $f ] && cd "$f/scenes" && ls *  
meta=`find *_MTL.txt` && echo $meta 
bands=${meta:0:40}'_B{}.TIF' && echo $bands  
output=${meta:0:40} && echo $output
python /home/users/mp877190/getting_netcdf/Landsat_code/main_hunterston.py "$f/scenes" $bands $meta $output
cd ..
done