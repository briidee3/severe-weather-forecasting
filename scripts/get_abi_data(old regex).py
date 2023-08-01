# General tool for sorting through GOES ABI data and getting requested data compiled in a separate folder
# BD 7-28-2023


# TODO:
# - get script functioning properly
# - only extract from desired channels (ignore the rest)---this can be done with the tar bash command


import os
import subprocess



# parameters
raw_abi_base_dir = os.path.abspath('./GOES-R') #'C:\\Users\\briid\\Documents\\Research\\Tornado-prediction-with-ML\\Data\\GOES-R'
ds_name = 'GOES-test-set_ABI'
ds_base_dir = os.path.join(raw_abi_base_dir, ds_name)
# dict to hold desired days and hours to get
## example: desired_data = {'4-03': ['all'], '4-04': ['00', '05', '15', '22'], '4-05': ['all']}
data_to_get = {'4-03': ['all'], '4-04': ['all'], '4-05': ['all'], '4-06': ['all'], '4-07': ['all']}
timesteps = 5  # timestep (in minutes) between data steps
channels = ['C08', 'C09', 'C11']
    


# get dataset using other functions
def get_raw_abi(dataset_name = 'GOES-test-set_ABI', desired_data = data_to_get):
    # move to ABI data base directory
    os.chdir(raw_abi_base_dir)
    # set global variables for dataset directory and name
    ds_name = dataset_name
    ds_base_dir = os.path.join(raw_abi_base_dir, dataset_name)
    # make directory for dataset
    os.mkdir(ds_base_dir)
    
    # get data
    for day in desired_data:
        print("\nGetting day: %s\n" % day)
        get_day(day, desired_data[day])
    

# get data for given day and hours
def get_day(day = '4-03', hours = ['all']):   # hours is a tuple listing queried hours, i.e. ['00', '03', '10'] or just ['all']
    # make folder for day in dataset dir
    ds_day_dir = os.path.join(raw_abi_base_dir, ds_name, day)
    os.mkdir(ds_day_dir)
    
    # go into day folder in raw abi data dir
    os.chdir(os.path.join(raw_abi_base_dir, day))
    
    # get files for given hours
    file_list = os.listdir(os.path.join(raw_abi_base_dir, day))
    
    # make dictionary for the archive files     # e.g {'00': '...00.tar.gz', ...}   # not the most optimal, but it works and isn't terrible, which is all I need for this part right now
    hours_archives = {}
    for file in file_list:  # add all that end in two numbers followed by '.tar.gz'
        cur_hour = file[-9:-7]
        if file.endswith(".tar.gz") and cur_hour.isdigit():
            hours_archives[cur_hour] = file
    
    # make tmp dir to store hours
    if not os.path.isdir('./tmp'):
        os.makedirs('./tmp')
        
    # get all hours and move to new directory
    if 'all' in hours:
        # iterate through all 24 hours
        for i in range(0, 23):
            cur_hour = "{:02d}".format(i)    # two digit number format
            # get data for each hour
            print("\n\tGetting data for hour: %s\n" % cur_hour)
            get_hour(hours_archives[cur_hour], cur_hour_dir)
    else:
        for hour in hours:
            # get data for each hour
            print("\n\tGetting data for hour: %s\n" % hour)
            get_hour(hours_archives[hour])
            
    # when done, delete temp folder
    subprocess.run(["rm", "-r", "tmp"])


# extract hourly files from archive and move desired ones to new dataset directory
def get_hour(hour_archive = 'OR_ABI-L1b_g16_meso_20220403_00.tar.gz', cur_day_dir = '../../ds_name/4-03'):
    # extract hour to tmp folder
    print("\t\tExtracting archive: %s\n" % hour_archive)
   # subprocess.run(["tar", "-xf", hour_archive, "-C", "./tmp"])
    
    cur_hour = hour_archive[-9:-7]
    
    # make hour dir in dataset dir
    cur_hour_dir = os.path.join(cur_day_dir, cur_hour)
    os.mkdir(cur_hour_dir)
    
    # copy files for desired channels and timesteps
    for i in range(0, 60):  # 60 raw timesteps per hour
        # only get what's necessary for desired timesteps
        if (i % timesteps == 0):
            cur_minute = "{:02d}".format(i)     # ensure it's 2 digits
            for channel in channels:
                # use regex with `find` in bash to get full filename from limited info
                cur_regex_cmd = "'\.\/tmp\/(OR_ABI-L1b-RadM2-M6)" + channel + "(.{13})" + str(cur_hour) + str(cur_minute) + "(.{35})(\.nc)$'"
                print("\t\t\tDEBUG: cur_regex_cmd = %s\n" % cur_regex_cmd)
                cur_file = str(subprocess.check_output(["find", ".", "-type", "f", "-regextype", "posix-extended", "-regex", cur_regex_cmd]))#.split("/")[2].split("\\")[0]
                print("\t\t\tCurrently moving %s...\n" % cur_file)
                # move current file to proper location
              #  subprocess.run(["mv", cur_file, cur_hour_dir + "/"])
        
    # remove files in tmp folder
  #  subprocess.run(["rm", "-r", "./tmp/*"])
    

os.chdir(os.path.join(raw_abi_base_dir, '4-03'))
#os.mkdir('./tmp')
get_hour(cur_day_dir = '../../test')