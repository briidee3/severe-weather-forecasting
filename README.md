# Tornado Forecasting with Machine Learning (and Fluid Mechanics)

CS480 Research Project, Summer '23

### The general idea of what I'm doing here:
- Datasets: [PERiLS_2022 GOES ABI](https://doi.org/10.26023/GQMQ-Q2T1-TB0B) and [PERiLS_2022 GOES GLM](https://doi.org/10.26023/52N0-7C8Q-5J0R)
- Feature engineering:
    - AMVs (Atmospheric Motion Vectors) via [OCTANE](https://github.com/JasonApke/OCTANE)
    - SPOD (Spectral Proper Orthogonal Decomposition) analysis via [PySPOD](https://github.com/MathEXLab/PySPOD)
- Prediction:
    - [MS-LSTM](https://github.com/mazhf/MS-RNN/tree/main) (and possibly similar variants)
- Classification:
    - TBD

This repo is primarily (most likely) going to be used for my own personal use in keeping track of things, version control and all that sorta stuff. 

Also, ***everything is currently a work in progress***.


### Current status:

`CS480_Tornado_Prediction_via_Satellite_Telemetry_Experimentation(1).ipynb` is where most of the testing and experimentation has been taking place thus far. *(Also, when looking at it on Github, most of the page is taken up by output from different stages of processing data, so it's best to view it in a JupyterLab sort of environment)*

#### CURRENTLY DONE (7-27-23):
- Put together a prototype dataset (`dataset/GOES-ABI_test-set-5.zip`) for immediate testing purposes.
- Create a custom data loader (`MS-RNN_experimenting/util/load_goes.py`) for loading said dataset
- Successfully ran said dataset through MS-ConvLSTM
    - Includes training and testing
    - MS-LSTM itself was having issues (seems to be a batching issue, still need to figure that out)
    - Output for the run (including metrics and visualizations of results) are located at `MS-RNN_experimenting/save/GOES-ABI_test-set-5/MS-ConvLSTM`

- Compiled and utilized [OCTANE](https://github.com/JasonApke/OCTANE/tree/master)
    - Got a successful automated setup running in Google CoLab for its use
    - Successfully ran to produce AMVs for 3 channel data (ABI M2 C08, C09, and C11)
- Visualized OCTANE output (namely *U* and *V* (used deliberately instead of just speed and direction))
    - Visualized speed and direction
    - Decided directly using *U* and *V* would be better for training purposes (especially when feeding data as images)
    - RGB composites of *U*, *V*, and *Rad* were made for each timestep in the aforementioned prototype custom dataset
 
- Lots of experimentation and trial and error
    - Learning how to use several APIs (i.e. SatPy, CartoPy, GeoPy, netCDF4, PySPOD, etc.) for messing around with the raw ABI data
    - Lots (and lots (and lots)) of bugfixing


 #### IN PROGRESS (7-27-23):
 - Fix batching issue with MS-LSTM
 - Finish script to automate data aggregation for compilation of next dataset(s)


#### TO DO (7-27-23):
 - Put together new dataset(s)
     - Finish script to automate data aggregation for compilation of next dataset(s)
     - Make more robust (and larger sample sizes) to try to improve training results (and to allow more flexibility in handling and loading)
         - Allow variable timesteps
         - Allow partitioning (i.e. cutting data into smaller pieces, so as to help out with processing)
     - Maybe just make a literal dataset, as well as a new data loader, this time based off of `load_hko.py`
         - Would be more effective for translating literal data (as is your goal) (for example, *U*, *V*, PySPOD outputs, etc.)
 - Changes to data handling/preprocessing in MS-RNN_experimenting
     - Figure out how to partition data samples for more efficient processing (and so that it doesn't use too much VRAM)
     - Allow processing of multi-dimensional images (i.e. RGB/RGBA) (as opposed to black and white composites of RGB composites (ha))
     - Allow use of `.nc` datasets as data (instead of just images)
         - Would allow for much more flexibility
 - Finish script(s) for preprocessing GLM data
     - Finish getting visualizations of GLM data per AMV timestep
         - Use as the blue channel (instead of *Rad*)
 - Integrate TSR-VFD
 - Finish implementation of PySPOD
     - Automate running it on OCTANE AMV output
     - Deliberate correlation between PySPOD output and AMV data
         - Dataset vs image?



BD 2023
