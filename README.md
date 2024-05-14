# Severe Weather Forecasting via the Sole Use of Satellite Data
### (with the end goal of tornado prediction via satellite data alongside machine learning and fluid mechanics)


## Information regarding the project thus far
- Raw data source used for testing: [PERiLS_2022 GOES-16 ABI Mesoscale Sector Data](https://doi.org/10.26023/GQMQ-Q2T1-TB0B) and [PERiLS_2022 GOES GLM](https://doi.org/10.26023/52N0-7C8Q-5J0R)
    - The latter has yet to be fully implemented/integrated into the project
- Feature engineering and data handling:
    - Raw data automatically organized via Python scripts
    - AMVs (Atmospheric Motion Vectors) generated from 3 channels of the raw data via [OCTANE](https://github.com/JasonApke/OCTANE)
    - RGB Composition via MatPlotLib
    - Automation of the previous 3 bullet points via the Custom Dataset Construction Pipeline (check the `pipeline` directory for more info)
    - Not yet fully implemented:
        - GOES-16 GLM (Geostationary Lightning Mapper) data
        - SPOD (Spectral Proper Orthogonal Decomposition) analysis via [PySPOD](https://github.com/MathEXLab/PySPOD)
- Prediction:
    - Several multi-scale neural network models via a modified version of the [MS-RNN](https://github.com/mazhf/MS-RNN/tree/main) framework
- Classification:
    - TBD

## Custom Dataset Construction Pipeline:
- The Custom Dataset Construction Pipeline automates the process of generating AMVs (Atmospheric Motion Vectors) from raw GOES-16 ABI data via the use of several scripts designed to work in conjunction with one another. Further details regarding the pipeline, as well as how to use it, are detailed in the `README.md` file under the `pipeline` directory.


BD 2023-24
