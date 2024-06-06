# modified to run with torchrun instead of torch.distributed.launch (approx. lines 49-52)   -BD

import os
from config import cfg

# GPUs need to be placed before Torch
os.environ["CUDA_VISIBLE_DEVICES"] = cfg.gpu
#os.environ["CUDA_LAUNCH_BLOCKING"] = True      # force synchronous computation

import torch
from torch import nn
from model import Model
from loss import Loss
from train_and_test import train_and_test
from net_params import nets
import random
import numpy as np
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler
from util.load_data import load_data
import argparse


#torch.utils.data.distributed.init_process_group(backend = "nccl")   # trying to fix errors with distributed processing -BD


# fix init
def fix_random(seed):
    os.environ['PYTHONHASHSEED'] = str(seed)
    random.seed(seed)  # Fixed random.random() generated random numbers
    np.random.seed(seed)  # Fixed np.random() generated random numbers
    torch.manual_seed(seed)  # Fixed CPU-generated random numbers
    torch.cuda.manual_seed(seed)  # Fixed GPU-generated random numbers - single card
    torch.cuda.manual_seed_all(seed)  # Fixed GPU-generated random numbers - multi-card
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.enabled = False


fix_random(2022)

# params
gpu_nums = cfg.gpu_nums
batch_size = cfg.batch
train_epoch = cfg.epoch
valid_epoch = cfg.valid_epoch
LR = cfg.LR

# model
model = Model(nets[0], nets[1], nets[2])

# run: python -m torch.distributed.launch --nproc_per_node=4 --master_port 39985 main.py
#parser = argparse.ArgumentParser()
#parser.add_argument("--local_rank", type=int, default=-1, help='node rank for distributed training')
#args = parser.parse_args()
local_rank = "cuda:0"   #int(os.environ["LOCAL_RANK"])      # changed to work properly on a local 1 GPU setup
torch.cuda.set_device(local_rank)
print('local_rank: ', local_rank)

# parallel group
#torch.distributed.init_process_group(backend="nccl")

# model parallel
model = model.cuda()
#model = nn.parallel.DistributedDataParallel(model, find_unused_parameters=True, device_ids=[local_rank],       # BD: removing DDP due to deadlocking issue
#                                            output_device=local_rank)
model = nn.DataParallel(model, device_ids=[local_rank], output_device=local_rank)

threads = cfg.dataloader_thread
train_data, valid_data, test_data = load_data()
train_sampler = DistributedSampler(train_data, shuffle=True)
valid_sampler = DistributedSampler(valid_data, shuffle=False)
train_loader = DataLoader(train_data, num_workers=threads, batch_size=batch_size, shuffle=False, pin_memory=True,
                          sampler=train_sampler)
test_loader = DataLoader(test_data, num_workers=threads, batch_size=batch_size, shuffle=False, pin_memory=False)
valid_loader = DataLoader(valid_data, num_workers=threads, batch_size=batch_size, shuffle=False, pin_memory=True,
                          sampler=valid_sampler)
loader = [train_loader, test_loader, valid_loader]

# optimizer
if cfg.optimizer == 'SGD':
    optimizer = torch.optim.SGD(model.parameters(), lr=LR, momentum=0.9)
elif cfg.optimizer == 'Adam':
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)
else:
    optimizer = None

# loss
criterion = Loss().cuda()

# train valid test
train_and_test(model, optimizer, criterion, train_epoch, valid_epoch, loader, train_sampler)
