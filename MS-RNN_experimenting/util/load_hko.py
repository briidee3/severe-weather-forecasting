from torch.utils.data import Dataset
import os
import cv2
import sys
sys.path.append("..")
from config import cfg
import numpy as np
from datetime import datetime


def load_HKO():
    train_data = Data(mode='train')
    test_data = Data(mode='test')
    return train_data, test_data, test_data


class Data(Dataset):
    def __init__(self, mode='train'):
        super().__init__()
        self._data_path = os.path.join(cfg.GLOBAL.DATASET_PATH, mode)
        self._img_path_list = os.listdir(self._data_path)
        if 'MeteoNet' in cfg.dataset:
            self._img_path_list.sort(key=lambda x: int(datetime.strptime(x.split('.')[0], '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')))
        else:
            self._img_path_list.sort(key=lambda x: int(x.split('.')[0]))
        self.img_num = len(self._img_path_list)
        self.IN_LEN = cfg.in_len
        self.OUT_LEN = cfg.out_len
        self.stride = 6
        self.LEN = (self.IN_LEN + self.OUT_LEN) * self.stride

    def __getitem__(self, index):
        # train, test, and validity are all taken in order, and finally processed with Dataloder's shuffle
        img_1_batch_path_list = self._img_path_list[index * self.LEN: (index + 1) * self.LEN]
        img_1_batch_path_list = img_1_batch_path_list[0::self.stride]
        l = []
        for i in range(len(img_1_batch_path_list)):
            img_path = img_1_batch_path_list[i]
            img = cv2.imread(os.path.join(self._data_path, img_path), flags=0)  # H*W
            img = cv2.resize(img, (cfg.width, cfg.height))
            # The default parameter is 1, read RGB images, so it is three channels (3-dimensional array), flags=0, it is a single channel (2-dimensional array)
            l.append(img)
        l = np.array(l)  # S*H*W
        frames = np.expand_dims(l, 1)  # S*1*H*W
        # frames = quick_read_frames(img_1_batch_path_list)

        return frames  # S*C*H*W

    def __len__(self):
        return self.img_num // self.LEN