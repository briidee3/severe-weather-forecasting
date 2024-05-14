BD 2023-24

# Custom Dataset Construction Pipeline

## Purpose:
- Automate the process of constructing image-based datasets composed of Atmospheric Motion Vectors (AMVs) derived from GOES-16 Satellite Image Time-Series (SITS) data

## Installation:
### Python packages
- The version of Python utilized for this version of the pipeline is Python 3.10
- The following packages are used throughout the pipeline, thus must be installed for its use:
    - `numpy`
    - `xarray`
    - `matplotlib`
    - `netCDF4`
### OCTANE:
- [OCTANE](https://github.com/JasonApke/OCTANE) requires (on Debian Linux) the following packages to be installed:
    - `libnetcdf-c++4-dev`
    - `netcdf-bin`
    - `netcdf-doc`
    - `make`
    - NVIDIA CUDA drivers:
        - Versions tested: 11.8, 12.2
        - Check for install with `nvcc --version`
            - If the first line you see is something like "NVIDIA (R) Cuda compiler driver", this should be all set
- A modified version of OCTANE (in the `OCTANE-master` directory) exists within the `pipeline` directory. To use OCTANE, you will need to build it, as detailed below.
#### Building OCTANE:
- First, make sure the packages listed above are installed.
- When ready to build OCTANE, go into the `OCTANE-master` directory and do the following (on the command line):
    - Go into `OCTANE-master/src/` directory (i.e. via `cd`)
    - Run `make`
    - The built executable, `octane`, should be in `OCTANE-master/build/`
        - If you run into issues with this, I'd recommend to first ensure you've properly followed all of the steps, and that the issue isn't with something from one of those (such as not having `nvcc` installed). If it still doesn't work, I'd recommend checking the `Makefile` in `OCTANE-master/src` to make sure things are properly configured. If that still doesn't help, then check the error output in the console, and follow it from there.
    - Copy the built executable file (`OCTANE-master/build/octane`) to the `pipeline` directory (i.e. `pipeline/octane`).
- An implementation of this process is demonstrated in the included 


## How to use:
- Prior to use of the pipeline, make sure you have the a directory (folder) set up as follows:
    - Inside whatever you're using as a base directory (i.e. the directory containing the data and the pipeline scripts; in this case, I'll refer to it as `.`), have a directory named `GOES-R`. If you would like to use a different name for the directory, then you will need to edit `ds_base_dir` in `main.py`, as detailed further below.
        - This directory (`GOES-R`) should contain subfolders for each day of data being used (e.g. `4-07`, `4-08`, `4-09`, `4-10`).
            - In this example, from the base directory, the day `4-07` may be found at `./GOES-R/4-07`
        - Put all data pertaining to a given day within its respective subfolder/subdirectory within the `GOES-R` directory.
            - In this example, the folder `4-07` contains the following:
                - `OR_ABI-L1b_g16_meso_20220407_00.tar.gz`
                - `OR_ABI-L1b_g16_meso_20220407_01.tar.gz`
                - `OR_ABI-L1b_g16_meso_20220407_02.tar.gz`
                - ...
                - `OR_ABI-L1b_g16_meso_20220407_23.tar.gz`
            - It is important that these files remain as archives (i.e. `.tar.gz`) and that they keep their original naming scheme (as it is utilized throughout the process) prior to use of the pipeline.
            - The name of the day folder is actually arbitrary; so long as the names of the folders line up with the names of the parameters stored in the `data_to_get` parameter in `main.py`, it should work out alright. The format used throughout this guide is largely for purposes of demonstration.
- The main script to run is `main.py`. Prior to its use, it is recommended that the user change the parameters (located at the top of the script) so as to reflect the data they're working with as well as desired settings:
    - `base_dir`: The base working directory. Default is `./`.
    - `ds_base_dir`: The main directory where the raw data is stored. In the above example, it is `GOES-R`.
    - `ds_name`: The name of the output dataset. Entirely arbitrary. Default is `output_dataset`.
    - `out_ds_base_dir`: The main directory for output from the pipeline. By default, it creates a new directory (if it doesn't exist) named by `ds_name` within the `base_dir`.
    - `prefix`: This is the prefix which can be found on the raw data `.nc` files stored within the `.tar.gz` archives. This will differ depending on which sectors of data you will be using from the GOES-16 ABI. Default is `OR_ABI-L1b-RadM2-M6`, which corresponds to mesoscale sector M2.
        - This is everything before the `CXX` in the name of the `.nc` files being used. 
        - For example, for the file `OR_ABI-L1b-RadM2-M6C16_G16_s20220970335549_e20220970336018_c20220970336063.nc`, it would be `OR_ABI-L1b-RadM2-M6`. 
        - This is not automatically acquired because the raw archived data may contain multiple different sectors of data; thus, in order to use the desired sector of the raw data being used, this will likely need to be changed.
    - `data_to_get`: Python dictionary object used to denote which days and which hours to be gathered and utilized. Formatted as follows:
        - For each day, denote it as `'M-DD': [<hours>]`, where each day is separated by a comma, and the hours are denoted in square brackets following a colon separating it from the day.
            - The "days" are effectively the names of the folders in the `ds_base_dir` directory (e.g. `GOES-R`).
            - `M` is the month, `DD` is the day.
                - Example: `'4-07'`
                - This is used to identify the folder for a given day being used.
                - Don't forget to add the `'` (or `"`) around the day!
            - For the desired hours for a given day, denote them as either `'all'`, or as a two digit number ranging from `'00'` to `'23'`
                - Example: `['00', '05', '14']`
                - As with the date, make sure to wrap the number in either `'` or `"`.
                - If multiple select hours are desired, separate them with a comma, all within the same set of square brackets.
            - Examples for day and hours:
                - `'4-10': ['00', '04', '19', '23']`
                - `'10-08': ['all']`
            - Example of full `data_to_get`: 
                - `{ '4-07': ['all'], '4-08': ['all'], '4-09': ['00', '01', '02', '03', '04'], '10-08': ['14', '18', '23']}`
    - `timesteps`: Time in minutes between timesteps. Can be any integer multiple of the timestep size of the raw data being used that is divisible by 60 (for number of minutes in an hour).
        - For example, with mesoscale data of raw timestep size of 1 minute, timestep size can be 1, 2, 3, 4, 5, 6, 10, 12, 15, 20, or 30.
        - Another example, for data with raw timestep size of 15 minutes, timestep size can be 15 or 30.
    - `channels`: The three channels to be used as input to OCTANE in the form of a list containing the channels formatted as `CXX`, where `XX` is the channel number.
        - Examples:
            - `['C08', 'C09', 'C11']`
            - `['C07', 'C08', 'C09']`
            - `['C08', 'C09', 'C10']`    
    


## Important notes/considerations:
- Thus far this pipeline has only been tested with mesoscale sector M2 data (i.e. 1 minute base timesteps). Some light modifications may be needed to allow use of other sectors.
