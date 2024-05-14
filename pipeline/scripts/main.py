# BD 2024

# Wrapper script for the Custom Dataset Construction Pipeline


# local file imports
import get_abi_data as abi
import gen_amvs as amv
import gen_rgb_comps as rgb

import os


# directory configuration parameters
base_dir = "./"                         # base working directory
ds_base_dir = base_dir + "GOES-R"       # main directory for data
ds_name = "output_dataset"              # name of output dataset
out_ds_base_dir = base_dir + ds_name    # main directory for output from OCTANE and MPL
prefix = "OR_ABI-L1b-RadM2-M6"          # prefix denoting the ABI sector being used

# data aggregation parameters
# python dictionary object to denote desired days and hours to be used
data_to_get = {'4-03': ['all'], '4-04': ['all'], '4-05': ['all'], '4-06': ['all'], '4-07': ['all']}
timestep_size = 5                       # timestep size in minutes
channels = ['C08', 'C09', 'C11']        # channels used for OCTANE input



# set input directories to their absolute paths 
base_dir = os.path.abspath(base_dir)
ds_base_dir = os.path.abspath(ds_base_dir)
out_ds_base_dir = os.path.abspath(out_ds_base_dir)



# extract and organize data from raw
abi.get_raw_abi(raw_abi_dir = os.path.abspath(ds_base_dir), dataset_name = ds_name, output_dir = out_ds_base_dir,
                prefix = prefix, desired_data = data_to_get, channels = channels, timestep_size = timestep_size)

os.chdir(base_dir)

# generate AMVs via OCTANE
octane_out_dir = os.path.join(out_ds_base_dir, "OCTANE-out/")
if not os.path.isdir(octane_out_dir):
    os.mkdir(octane_out_dir)
amv.gen_octane_all_abi_out(out_ds_base_dir, data_to_get, channels, timestep_size)     # generate AMVs for all data in ABI-out
    


# generate RGB composites via MPL

# make directory if it doesn't exist
mpl_out_dir = os.path.join(out_ds_base_dir, "MPL-out/")
if not os.path.isdir(mpl_out_dir):
    os.mkdir(mpl_out_dir)

# go thru all days and hours in OCTANE-out directory
for day in os.listdir(octane_out_dir):
    rgb.gen_rgb_composites_for_subdirs(os.path.join(octane_out_dir, day), os.path.join(mpl_out_dir, day))
