!/bin/bash

# move files around while working with GOES ABI data from PERiLS_2022 dataset
# BD 2023



base_dir='./ABI-raw/'
prefix="OR_ABI-L1b-RadM2-M6C"

hours="$(ls $base_dir)"

for hour in hours;
do
	cd "${hour}"
	
	mkdir ./tmp/
	unrar rar.files to ./tmp/
	
	timesteps="$(ls .)"
	for timestep in timesteps;
	do
		curr_time="$(sed 's/)"
	done
	
	cd "${base_dir}"
done