# BD: This file has been created for use with GOES ABI and GLM data
#   and has been based off of the other load_*.py files in this directory.

# It appears these were made for preprocessing and cleaning data before being used,
#   so that is essentially what I will attempt to do here


# TODO: 
#   - 

import os
import cv2
import sys
sys.path.append("..")
from config import cfg
import numpy as np
from torch.utils.data import Dataset
from util.meteo import dBZ2Pixel


