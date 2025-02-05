# BD: This file has been created for use with GOES ABI and GLM data
#   and has been based off of the other load_*.py files developed by the creators
#   of the MS-RNN github repo. (most was actually just copied and refactored from load_kth.py)


import os
import cv2
import sys
sys.path.append("..")
from config import cfg
import numpy as np
import random
import torch
from itertools import cycle



def load_GOES():
    train_data = GOES(train = True, seq_len = cfg.in_len + cfg.out_len)
    test_data = GOES(train = False, seq_len = cfg.in_len + cfg.eval_len)
    valid_data = test_data
    return train_data, valid_data, test_data


# load RGB composite of OCTANE output AMVs derived from ABI (GOES-16, M2)
def load_file(data_root, data_type, seq_len):#, T = 1):    # T is n_skip, or number of frames to skip (should probably be just 1 for now)
    if data_type == 'test':
        file_path = os.path.join(os.path.join(os.path.dirname(data_root), 'file_lists'), 'test_data_list.txt')
    else:
        file_path = os.path.join(os.path.join(os.path.dirname(data_root), 'file_lists'), 'train_data_list.txt')
    with open(file_path) as f:
        vid_list = f.readlines()
    seq_list = []
    clip_dict = {}
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
        #n_skip = T
        for i in range(i_s, i_e - seq_len + 2):#, n_skip):
            istart = i
            iend = i + seq_len  # "not -1, so when read is just range(istart, iend)"
            seq_list.append({'class': c, 'name': name, 'start': istart, 'end': iend})
            if name not in clip_dict.keys():
                clip_dict[name] = []
            clip_dict[name].append([istart, iend])
    print('Total sequences: %d' % len(seq_list))
    print('Total sets: %d' % len(clip_dict))
    return seq_list, clip_dict


def flatten_rgb_image(img):
    # bgr not rgb, since we use cv2 images here
    b = img[:,:,0]
    g = img[:,:,1]
    r = img[:,:,2]
    new_img = np.concatenate((b, g))
    new_img = np.concatenate((new_img, r))

    return new_img


class GOES(object):
    def __init__(self, train, seq_len):
        self.data_root = cfg.GLOBAL.DATASET_PATH + '/'
        self.classes = ['clouds']   # currently not separating into individual classes; may be done later
        if train:
            self.train = True
            data_type = 'train'
            self.sets = list(range(1, 8))                                           # modify this depending on what subsets to be used for training
        else:
            self.train = False
            data_type = 'test'
            self.sets = list(range(8, 12))                                          # modify this depending on what subsets to be used for testing
        random.seed(123)
        self.seq_list, self.clip_dict = load_file(self.data_root, data_type, seq_len)
        self.seed_set = False

    # get sequence of images in folder as per `vid`
    def get_sequence(self, index):
        vid = self.seq_list[index]
        c = vid['class']
        name = vid['name']
        istart = vid['start']
        iend = vid['end']
        # directory with images
        dname = '%s/%s/%s' % (self.data_root, 'MPL-organized', vid['name'])
        # list of images in directory
        frames = os.listdir(dname)
        frames.sort()
        seq = []
        # put together sequence of images
        for i in range(istart, iend):
            fname = '%s/%s' % (dname, frames[i - 1])
            im = cv2.imread(fname)
            im = cv2.resize(im, (cfg.width, int(cfg.height / 3)))  # divide by 3 due to next step (flattening rgb image)
            #im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            # partition image by color (RGB/BGR) (results in larger image)
            im = flatten_rgb_image(im)
            seq.append(im)  # append as RGB (or in the case of cv2/opencv, BGR)     # S x H x W
        return np.expand_dims(np.array(seq), 1)     # done for use with pytorch rnn     # S x C x H x W
    
    def __getitem__(self, index):
        if self.train:
            return torch.from_numpy(self.get_sequence(index))   # "the dataloader in main handles shuffle"
        else:
            return torch.from_numpy(self.get_sequence(index))
        
    def __len__(self):
        return len(self.seq_list)

