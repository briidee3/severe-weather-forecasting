# testing, for use working with Geostationary Lightning Mapper (GLM) data
# BD 2023

import os
import subprocess
from datetime import datetime, timedelta
import re



data_to_get = {'4-07': ['all']}#, '4-04': ['all'], '4-05': ['all'], '4-06': ['all'], '4-07': ['all']}
ds_name = 'ts7_glm'
raw_glm_path = os.path.join(os.path.abspath('.'), '../GLM_4-03_4-07')#'./4-03/00')
timesteps = 5   # minutes


# get file data list
def get_dir_list(dir = raw_glm_path):
    cur_dir_list = os.listdir(dir)
    cur_dir_list = [os.path.join(dir, s) for s in cur_dir_list]
    return cur_dir_list


def get_hour(hour = '00', day = '4-03'):
    # hour dir
    cur_hour_dir = os.path.join(os.path.abspath('.'), day, hour)
    if not os.path.isdir(cur_hour_dir):
        os.mkdir(cur_hour_dir)
        
    # copy files for desired channels and timesteps
    for i in range(0, 60):  # 60 raw timesteps per hour
        # only get what's necessary for desired timesteps
        if (i % timesteps == 0):
            cur_minute = "{:02d}".format(i)     # ensure it's 2 digits
            cur_timesteps = [("{:02d}".format(n) + "|") for n in range(i, i + timesteps - 1)]
            
            
            # regex cmd to get files
            cur_regex_cmd = ".*(OR_GLM-L2-LCFA_G16_s)" + "(.{7})" + cur_hour + "(" + cur_minute + "|{})".format(''.join(cur_timesteps)) + "(.{35})(\.nc)$"    # cur
            r = re.compile(cur_regex_cmd)
            cur_file_list = list(filter(r.match, get_dir_list(os.path.join(raw_glm_path, day))))
            cur_file_list = [os.path.join(raw_glm_path, cur_file) for cur_file in cur_file_list]
            
            # dating info for make_GLM_grids.py
            startdate = datetime(2022, 4, int(day[-1:]), int(hour), int(cur_minute))
            duration = timedelta(0, 60 * timesteps)
            enddate = startdate + duration
            
            # run files thru glmtools script
            cmd = "python C:\\Users\\briid\\Documents\\Research\\Tornado-prediction-with-ML\\experimentation\\tornado-forecasting\\tools\\GLM\\glmtools\\examples\\grid\\make_GLM_grids.py --fixed_grid --split_events --goes_position=east --goes_sector=meso --ctr_lat=37.0 --ctr_lon=-86.5 --dx=2.0 --dy=2.0 --dt=300.0 --start=" + startdate.isoformat() + " --end=" + enddate.isoformat() + " " + ' '.join(cur_file_list)    
                # removed -o " + cur_hour_dir + "/GLM_grid_" + day + "_" + hour + cur_minute + ".nc" + ", since outputting to multiple files doesn't work
            print(cmd)
            
            subprocess.run(cmd.split())
    
    


# days
for day in data_to_get:
    # day dir
    cur_day_dir = os.path.join(os.path.abspath('.'), day)
    if not os.path.isdir(cur_day_dir):
        os.mkdir(cur_day_dir)
    
    # hour
    if 'all' in data_to_get[day]:
        # iterate through whole day
        for i in range(20, 24):
            cur_hour = "{:02d}".format(i)
            # get data for hour, run through program
            get_hour(cur_hour, day)
            
    # go back to base dir
    #os.chdir('../')
        