# BD 2023-24 

# Generate RGB composites from OCTANE output via MatPlotLib (MPL)


import matplotlib.pyplot as plt
import matplotlib
import xarray as xr
import netCDF4 as nc
import numpy as np
import os


# normalization function for AMVs
def normalize_amv(band):
    band_min = -50.0    # border between F1 and F2 tornado (meters / sec)
    band_max = 50.0     # border between F1 and F2 tornado (meters / sec)
    return np.clip(((band - band_min) / (band_max - band_min)), 0, 1)

# normalization function for radiance
def normalize_rad(band):
    band_min = 0
    band_max = 5
    return np.clip(((band - band_min) / (band_max - band_min)), 0, 1)


# generate rgb composite for OCTANE output AMV file
def gen_rgb_composite(amv_file_path, out_dir_path):
  # get path for saving file
  save_path = os.path.join(out_dir_path)
  print("AMV file path: %s\nSave path: %s\n out_dir_path: %s" % (amv_file_path, save_path, out_dir_path))

  # load AMVs from OCTANE-out
  raw_ds = nc.Dataset(amv_file_path)
  stored = xr.backends.NetCDF4DataStore(raw_ds)
  curr_ds = xr.open_dataset(stored)

  # load data into R G and B variables
  Rd = curr_ds['U'].data
  Gd = curr_ds['V'].data
  Bd = curr_ds['Rad'].data

  # clip between 0 and 1 (RGB data can only be in that range)
  Rd = normalize_amv(Rd)
  Gd = normalize_amv(Gd)
  Bd = normalize_rad(Bd)

  # don't display the plotted figure
  matplotlib.use('Agg')

  # stack the arrays
  RGB = np.dstack([Rd, Gd, Bd])

  # formatting for image name:
  # "rgb_comp_" + channels + "_" + timestep
  amv_file_name = amv_file_path.split("/")[-1]
  # check if file name is formatted as expected; if not, reject it
  if not amv_file_name[0:3] == "amv":
    print("ERROR: Unexpected file format!")
    exit()

  image_name = "/rgb_comp_" + amv_file_name[7:15] + "_" + amv_file_name.split('_')[1][0:15] + ".png"

  # plot and save composite image to appropriate directory
  #fig, ax = plt.subplots(1, 1)
  #ax.axis('off')
  #ax.im(RGB)
  #fig.savefig('/content/MPL-out/rgb-comp_{}.png'.format(timestep))
  plt.imsave(save_path + image_name, RGB, cmap='jet')
  plt.close()

  return 1

# generate rgb composites for all AMVs in directory
def gen_rgb_composites_for_dir(amv_dir_path, out_dir_path):
  file_names = os.listdir(amv_dir_path)
  i = 0   # iterator
  for file in file_names:
    i += 1
    print("{}. ".format(i))
    print("Generating composite for {}...".format(file))
    # gen composites
    gen_rgb_composite(os.path.join(amv_dir_path, file), out_dir_path)
    print("Done with {}\n".format(file))
  print("Done generating RGB composites for dir {}".format(amv_dir_path))

# generate rgb composites for subdirectories
def gen_rgb_composites_for_subdirs(amv_base_dir, out_base_dir):

  # make day dir if need be
  if not os.path.isdir(out_base_dir):
    os.mkdir(out_base_dir)

  # create folders, gen composites for dir
  for cur_dir in os.listdir(amv_base_dir):
    # create folder for day/hour
    out_dir = os.path.join(out_base_dir, cur_dir)
    # check if folder exists, if not, create it
    if not os.path.isdir(out_dir):
      os.mkdir(out_dir)
    # gen for all in dir
    gen_rgb_composites_for_dir(os.path.join(amv_base_dir, cur_dir), out_dir)