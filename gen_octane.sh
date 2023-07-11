#!/bin/bash

# Bri D'Urso 2023
# This script is to be used to programmatically generate AMVs for GOES ABI data
# from the Mesoscale2 sector via OCTANE, by Jason Apke.
#
# This will primarily be used for experimentation for generating Atmospheric
#  Motion Vectors (AMVs) for use in my (BD) Tornado Forecasting via ML research project.

# this version tested and working as of 7-10-23


if [ $# -eq 0 ]; then
	echo "gen_octane.sh"
	echo ""
	echo "Bri D'Urso 2023"
	echo ""
	echo "How to use:"
	echo "  Example:"
	echo "    ./gen_octane.sh 09 20220961700549 20220961701549"
	echo '         where "09" is the GOES ABI channel,'
	echo '         "20220961700549" is the first timestep (by filename)'
	echo '         and "20220961701549" is the second timestep (by filename)'
	echo ""
	echo "  Argument 1:"
	echo "    GOES ABI channel (two digit number)"
	echo "    Examples:"
	echo "      09"
	echo "      10"
	echo "      11"
	echo "  Argument 2:"
	echo "    First GOES ABI timestep (by filename, e.g. from s20220961700549)"
	echo "    Examples:"
	echo "      20220961700549"
	echo "      20220961701549"
	echo "      20220961702549"
	echo "  Argument 3:"
	echo "    Second GOES ABI timestep (by filename, e.g. from s20220961701549)"
	echo "    Examples:"
	echo "      20220961701549"
	echo "      20220961702549"
	echo "      20220961703549"
	echo "  Argument 4:"
	echo "    (optional) Data home directory"
	echo "    Examples:"
	echo "      /home/user/doc/data/dataset"
	echo "      ./data/here"
	echo "      /content/drive/MyDrive/data/"
	echo ""
	echo "  Examples:"
	echo "    ./gen_octane.sh 09 20220961700549 20220961701549"
	echo "    ./gen_octane.sh 11 20220961702549 20220961703549 /data/folder"
	echo "    ./gen_octane.sh 07 20220961704549 20220961705549"
	echo ""
	echo ""
	
	exit 0
fi

# prefix of file name location
path="/content/drive/MyDrive/Colab Notebooks/tornado-forecasting/data/ABI/test_set_3/"
prefix="OR_ABI-L1b-RadM2-M6C"

# allow prefix to be passed as argument
if [ -n "$4" ]; then
    path=$4
fi


# channel as taken from arg1 (e.g. 08, 09, 10, 11)
channel=$1

# timesteps as taken from ABI data filename (e.g. 20220961700549)
timestep_one=$2
timestep_two=$3

# used to get full file names
filename_one="${prefix}${channel}_G16_s${timestep_one}*.nc"
filename_two="${prefix}${channel}_G16_s${timestep_two}*.nc"

#get full file names
cd "$path"
full_filename_one="${path}$(find . -name "$filename_one")"
full_filename_two="${path}$(find . -name "$filename_two")"


output_filename="/content/OCTANE-out/amvout_${channel}-${timestep_one}-${timestep_two}.nc"


echo "ABI Data file names: "
echo "  $full_filename_one $filename_one"
echo "  $full_filename_two"
echo "Output filename: ${output_filename}"


# run octane for channel $1 at time $2 from base dir in Google Colab ('/content')
cd /content/drive/MyDrive/Colab\ Notebooks/tornado-forecasting/OCTANE-master/build
# run octane with basic settings
./octane -alpha 5 -lambda 1 -i1 "$full_filename_one" -i2 "$full_filename_two" -o "$output_filename"

echo ""

exit 0