# BD: This file has been created for use with GOES ABI and GLM data
#   and has been based off of the other load_*.py files developed by the creators
#   of the MS-RNN github repo. (most was actually just copied and refactored from load_kth.py)

# It appears these were made for preprocessing and cleaning data before being used,
#   so that is essentially what I will attempt to do here



# TODO: 
#   - create function to initialize/add tensor for PySPOD output
#       - probably best done by integrating into image input
#   - further analysis of load_hko.py (for refactoring code and reverse-engineering)
#       - incorporate functionalities from load_kth.py, so as to allow interpretation of the data
#         in subsections (i.e. different hours of different days)

import os
import cv2
import sys
sys.path.append("..")
from config import cfg
import numpy as np
import random
import torch



def load_GOES():
    train_data = GOES(train = True, seq_len = cfg.in_len + cfg.out_len)     # make sure seq_len is below 18 (for test_set_5)
    test_data = GOES(train = False, seq_len = cfg.in_len + cfg.eval_len)
    valid_data = test_data
    return train_data, valid_data, test_data


# load RGB composite of OCTANE output AMVs derived from ABI (GOES-16, M2)
def load_file(data_root, data_type, seq_len, T):        # seq_len can be any number 2-17 (for test_set_5)   # T is n_skip, or number of steps to skip (should probably be just 1 for now)
    if data_type == 'test':
        file_path = os.path.join(os.path.join(os.path.dirname(data_root), 'file_lists'), 'test_data_list.txt')
    else:
        file_path = os.path.join(os.path.join(os.path.dirname(data_root), 'file_lists'), 'train_data_list.txt')
    with open(file_path) as f:
        vid_list = f.readlines()
    seq_list = []
    clip_dict = {}
    # specific list of folders full of image data
    specific = os.listdir(os.path.join(os.path.dirname(data_root), 'MPL-out'))  # using all in folder because they will all be used (for now)
    # iterator
    num = 0
    # put together dictionary from txt list for info pertaining to videos
    for vid in vid_list:
        vid = vid[:-1]  # get rid of eol
        comps = vid.split(' ')
        name = comps[0] # name of sequence
        # start and end of iterations (num of image files)
        i_s = int(comps[1])
        i_e = int(comps[2])
        ID = name
        c = comps[3]
        # construct sequence (in dict), add to clip_dict for use by model
        if data_type == 'train':
            num += (i_e - seq_len + 1 - i_s + 1)
            for i in range(i_s, i_e - seq_len + 2):
                istart = i
                iend = i + seq_len  # "not -1, so when read is just range(istart, iend)"
                seq_list.append({'class': c, 'name': name, 'start': istart, 'end': iend})
                if name not in clip_dict.keys():
                    clip_dict[name] = []
                clip_dict[name].append([istart, iend])
        else:
            n_skip = T
            for i in range(i_s, i_e - seq_len + 2, n_skip):
                istart = i
                iend = i + seq_len  # "not -1, so when read is just range(istart, iend)"
                seq_list.append({'class': c, 'name': name, 'start': istart, 'end': iend})
                if name not in clip_dict.keys():
                    clip_dict[name] = []
                clip_dict[name].append([istart, iend])
    # shuffle order of sequences
    random.shuffle(seq_list)
    print('Total sequences: %d' % len(seq_list))
    print('Total \"videos\" (in this case, days): %d' % len(clip_dict))
    return seq_list, clip_dict


class GOES(object):
    def __init__(self, train, seq_len = 10, T = 1):     # default to fairly limited seq_len and T (steps) due to limitations of current dataset
        self.data_root = cfg.GLOBAL.DATASET_PATH
        self.classes = ['clouds']   # currently not separating into individual classes; may be done later
        if train:
            self.train = True
            data_type = 'train'
            self.hours = list(range(1, 15))   # for now, with test_set_5, we have 22 sets for training, each a different hour on a (sometimes) different day
        else:
            self.train = False
            data_type = 'test'
            self.hours = list(range(15, 23))
        random.seed(123)
        self.seq_list, self.clip_dict = load_file(self.data_root, data_type, seq_len, T)
        self.seed_set = False

    # get sequence of images in folder as per `vid`
    def get_sequence(self, index):
        vid = self.seq_list[index]
        c = vid['class']
        name = vid['name']
        istart = vid['start']
        iend = vid['end']
        # directory with images
        dname = '%s/%s/%s' % (self.data_root, 'MPL-out', vid['name'].split('_')[0]) # last one is weird due to scripting error
        # list of images in directory
        frames = os.listdir(dname)
        seq = []
        # put together sequence of images
        for i in range(istart, iend):
            fname = '%s/%s' % (dname, frames[i + 1])
            im = cv2.imread(fname)
            im = cv2.resize(im, (cfg.width, cfg.height))
            seq.append(im)  # append as RGB (or in the case of cv2/opencv, BGR)
        return np.expand_dims(np.array(seq), 1)
    
    def __getitem__(self, index):
        if self.train:
            return torch.from_numpy(self.get_sequence(index))   # "the dataloader in main handles shuffle"
        else:
            return torch.from_numpy(self.get_sequence(index))
        
    def __len__(self):
        return len(self.seq_list)

