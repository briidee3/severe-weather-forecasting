# BD 2023-24

# Generate Atmospheric Motion Vectors (AMVs) via OCTANE (Optical flow Code for Tracking, Atmospheric motion vector, and Nowcasting Experiments, by Jason Apke)


import subprocess
import os



# make and fill OCTANE-out directory with AMVs
def gen_octane_all_abi_out(out_ds_base_dir, desired_data, channels, timestep_size):
  octane_out_base_dir = os.path.join(out_ds_base_dir, "OCTANE-out/")

  # make OCTANE-out directory
  if not os.path.isdir(octane_out_base_dir):
    os.mkdir(octane_out_base_dir)

  # ABI raw base directory
  abi_out_dir = os.path.join(out_ds_base_dir, "ABI-out/")

  # used for storing data pertaining to the last hour's first and last timestep (for use getting inter-hour AMVs)
  prev_hour = [ 
                  ["a", "b", "c"], 
                  ["a", "b", "c"], 
                  "12345678", octane_out_base_dir, abi_out_dir
              ]
  
  # go thru all days in ABI-out directory, generate AMVs
  for day in os.listdir(abi_out_dir):   # go thru day directories in ./output_dataset/ABI-out
    
    # make dir for day
    cur_day_dir = os.path.join(octane_out_base_dir, day)
    if not os.path.isdir(cur_day_dir):
      os.mkdir(cur_day_dir)
    
    for hour in os.listdir(os.path.join(abi_out_dir, day)):
      # generate AMVs for all hours in current day folder
      cur_hour = gen_octane_all_in_dir_3ch(dir_path = os.path.join(abi_out_dir, day, hour),
                                  out_ds_dir = os.path.join(octane_out_base_dir, day), num_steps = int(60 / timestep_size), channels = channels)
      
      # get AMVs between hours (currently only doing this if hours == 'all')
      if day[0] == 'all':
        # if prev_hour is the last hour from the previous day or is the previous hour in the current day, get the AMVs between the hours
        if (int(cur_hour[2]) % 100 == 0 and int(prev_hour[2]) % 100 == 23) or int(prev_hour[2]) % 100 + 1 == int(cur_hour[2]):
          gen_octane_between_hours(prev_hour[1], cur_hour[0], channels)     # get AMV between first timestep of current hour and last timestep of previous hour
      
      prev_hour = cur_hour
            

# generate AMVs for 3 channels in ABI-out sub-directory
def gen_octane_all_in_dir_3ch(dir_path, out_ds_dir, num_steps = 12, channels = ['C08', 'C09', 'C11']):

  # get list of files
  file_names = os.listdir(dir_path)
  file_names.sort()

  # get string to denote current hour from file name
  # not using first file (i.e. file_names[0]) due to edge cases; use of multiple channels necessitates at least 3 files per timestep anyways, so this should cause no issue
  curr_hour = file_names[1].split('_')[3][1:10]

  # make new directory in OCTANE-out for this day/hour
  octane_out_dir = os.path.join(out_ds_dir, curr_hour)
  if not os.path.isdir(octane_out_dir):     # check if dir exists
    os.mkdir(octane_out_dir)  # if not, make it

  # generate AMVs for all but the last (inter-hour/day) timestep
  for i in range(0, num_steps - 1):
    if i < (num_steps - 1):   # if next file name exists
      # first channel
      timestep_ch1_one = file_names[i]
      timestep_ch1_two = file_names[i + 1]
      # second channel
      timestep_ch2_one = file_names[i + num_steps]  # add num_steps to go to file num_steps ahead (next channel)  # extra + 1 to account for scripting error
      timestep_ch2_two = file_names[i + 1 + num_steps]
      # third channel
      timestep_ch3_one = file_names[i + num_steps + num_steps]
      timestep_ch3_two = file_names[i + 1 + num_steps + num_steps]
      # output filename
      output_filename = octane_out_dir + "/amvout-" + channels[0][1:3] + "-" + channels[1][1:3] + "-" + channels[2][1:3] + timestep_ch1_one.split('_')[3][1:] + '_' + timestep_ch1_two.split('_')[3][1:] + '.nc'  # only need one channel (since labelling is only using timesteps, and they're the same between channels)

      # assuming ./octane is in base directory
      print('\nRunning for {}...\n'.format(output_filename))
      run = subprocess.run(["./octane", "-i1", (dir_path + '/' + timestep_ch1_one), "-i2", (dir_path + '/' + timestep_ch1_two), "-ic21", (dir_path + '/' + timestep_ch2_one), "-ic22", (dir_path + '/' + timestep_ch2_two), "-ic31", (dir_path + '/' + timestep_ch3_one), "-ic32", (dir_path + '/' + timestep_ch3_two), "-alpha", "5", "-lambda", "1", "-o", output_filename])
      print('\nDone with {}...\n'.format(run))
    else:
      print("\nDone with directory {}\n".format(dir_path))
    
  # return last timestep and first timestep for use getting AMVs between hours and days (formatted as a list of the last timestep of all three channels)
  return [ 
    [file_names[0], file_names[num_steps], file_names[num_steps * 2]],                           # first timestep of the hour
    [file_names[num_steps - 1], file_names[num_steps * 2 - 1], file_names[num_steps * 3 - 1]],   # last timestep of the hour
    curr_hour, octane_out_dir, dir_path
  ]

# generate AMVs for last timestep of prev hour and first timestep of current hour
def gen_octane_between_hours(first_timestep, second_timestep, channels):

  dir_path = [first_timestep[4], second_timestep[4]]

  # output filename
  output_filename = first_timestep[3] + "/amvout-" + channels[0] + "-" + channels[1] + "-" + channels[2] + first_timestep[0].split('_')[3][1:] + '_' + second_timestep[0].split('_')[3][1:] + '.nc'  # only need one channel (since labelling is only using timesteps, and they're the same between channels)

  # run octane between these timesteps
  print('\nRunning for {}...\n'.format(output_filename))
  run = subprocess.run(["./octane", "-i1", (dir_path[0] + '/' + first_timestep[0]), "-i2", (dir_path[1] + '/' + second_timestep[0]), 
                          "-ic21", (dir_path[0] + '/' + first_timestep[1]), "-ic22", (dir_path[1] + '/' + second_timestep[1]), 
                          "-ic31", (dir_path[0] + '/' + first_timestep[2]), "-ic32", (dir_path[1] + '/' + second_timestep[2]), 
                          "-alpha", "5", "-lambda", "1", "-o", output_filename])
  print('\nDone with {}...\n'.format(run))




