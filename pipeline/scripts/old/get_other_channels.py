# script for moving files around for GOES ABI data
# BD 7-25-2023


import os
import subprocess
import threading


# get other channels for current dir's ABI timesteps
def get_other_channels(hour = '4-07_20', channels = ['C09', 'C11']):

    os.chdir(hour)
    ts = os.listdir('.')
    timesteps = []
    tarfile = ''
    
    print(os.listdir('.'))
    
    # make tmp directory for extraction
    if not os.path.isdir('./tmp'):
        os.makedirs('./tmp')
    
    # format timesteps list
    nts = []     # not time steps (indices)
    for timestep in ts:
        # remove tar pkg from timesteps list
        if timestep.endswith('.tar.gz'):
            # get tarfile name
            tarfile = timestep
            nts.append(timestep)
        elif timestep.endswith('.nc'):
            # get numerical timesteps
            timesteps.append(timestep.split('_')[3][1:])
        else:   # for some reason this never gets called????
            # append index for use after this loop
            nts.append(timestep)
    
    print(nts)
    # now, remove unwanted elements (i.e. those without ".nc") using the indices gathered during the loop
    #for n in nts:     
    #    timesteps.remove(n)
    # remove tmp folder
    #if 'tmp' in timesteps:
    #    timesteps.remove('tmp')
        
    
    
    print(timesteps)
            
    # extract the archive to temp folder
    print("\nExtracting tar for {}...".format(hour))
    print(tarfile + "\n")
    subprocess.run(["tar", "-xf", tarfile, "-C", "./tmp"])
    
    # move to ./tmp
    os.chdir('./tmp')
    # get timesteps, move files to directory
    for i in range(0, len(timesteps) - 1):
        # do for each channel
        for channel in channels:
            # queried file name
            curr_file = 'OR_ABI-L1b-RadM2-M6' + channel + '_G16_s' + timesteps[i] + "*"
            print(curr_file)
            # get full file name
            curr_file = str(subprocess.check_output(["find", "-name", curr_file])).split("./")[1].split("\\")[0]
            print(curr_file)
            # move curr_file to directory
            subprocess.run(["mv", curr_file, "../"])
    # move back to original directory
    os.chdir('..')
            
    
    # remove files in ./tmp
    subprocess.run(["rm", "-r", "tmp"])
    
    # go back to main dir (ABI-raw)
    os.chdir('..')
    print('\nFinished with {}...\n'.format(hour))
    



def run_all_hours():
    os.chdir('ABI-raw')

    # loop through and do it for each folder
    hours = os.listdir('.')
    #threads = []
    for hour in hours:     #i in #range(0, len(hours) - 1):
        #threads.append(threading.Thread(target = get_other_channels, args = (hours[i])))
        #threads[i].start()
        get_other_channels(hour)

    # notify when done
    #for thread in threads:
    #    thread.join()

    print("Finished!\n")


run_all_hours()