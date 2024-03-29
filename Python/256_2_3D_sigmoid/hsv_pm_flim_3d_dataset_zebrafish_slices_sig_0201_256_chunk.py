# -*- coding: utf-8 -*-
"""HSV_PM_FLIM_3D_Dataset_zebrafish_1009_slices_sig.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LXvRObytkR-y8vV2TCiGCvuRkqvDk43n

# Used input images (intensity and lifetime values)
input max is 0-max (min to 0 and max = 1) and target max is 0-10nsec
divide the image into 256x256 chunks for 3D zebrafish data

Here target is hsv version 
hsv algo:
hmin = 0
hmax = 0.7

tau1 =  hmax + (hmin-hmax)*tau
hsv(:,:,1) = tau1
hsv(:,:,2) = 1
hsv(:,:,3) = intensity value
"""

# !pip install -q torch==1.2.0 torchvision
# !pip3 install torch
# !pip3 install torch torchvision
# !pip3 install scipy
#
# from os import path
# from wheel.pep425tags import get_abbr_impl, get_impl_ver, get_abi_tag
# platform = '{}{}-{}'.format(get_abbr_impl(), get_impl_ver(), get_abi_tag())
#
# accelerator = 'cu80' #'cu80' if path.exists('/opt/bin/nvidia-smi') else 'cpu'
# print('Platform:', platform, 'Accelerator:', accelerator)
#
# #!pip install --upgrade --force-reinstall -q http://download.pytorch.org/whl/{accelerator}/torch-1.2.0-{platform}-linux_x86_64.whl torchvision
# !pip3 install torch==1.2.0+cu92 torchvision==0.4.0+cu92 -f https://download.pytorch.org/whl/torch_stable.html
# import torch
# print('Torch', torch.__version__, 'CUDA', torch.version.cuda)
# print('Device:', torch.device('cuda:0'))

"""# Folder: https://drive.google.com/drive/u/1/folders/169wXLc62Kw_iT1n_cMx2TneSF7fY8p_z

# My Drive/Fall19/I_vs_lifetime/Dataset/3D_data/Zebrafish_images/PM_FLIM/
"""

import os
import sys
import time
import torch
import numpy as np


def to_numpy(input):
    if isinstance(input, torch.Tensor):
        if input.requires_grad:
            input = input.detach()
        return input.cpu().numpy()
    elif isinstance(input, np.ndarray):
        return input
    else:
        raise TypeError('Unknown type of input, expected torch.Tensor or '\
            'np.ndarray, but got {}'.format(type(input)))

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def mkdirs(paths):
    if isinstance(paths, list) and not isinstance(paths, str):
        for path in paths:
            mkdir(path)
    else:
        mkdir(paths)
        
        
"""
# Noise2Noise: UNet

# (input, target) = next(train_generator)

"""

import torch
import torch.nn.functional as F
from torchvision import transforms
from torch.optim.lr_scheduler import ReduceLROnPlateau
#from args_n2n_bpae import args, device
#from models.unet import UnetN2N, UnetN2Nv2
#from models.dense_ed import DenseED
#from utils.dataset import online_batch, fluore_to_tensor
#from utils.misc import mkdirs
#from utils.noise import add_noise
#from utils.plot import save_samples, save_stats
#from utils.metrics import cal_psnr

import numpy as np
from time import time
import json
import sys
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import argparse
import torch
import json
import random
import time
from pprint import pprint

# from google.colab import drive
# drive.mount('/content/gdrive', force_remount=True)
root_path = '/afs/crc.nd.edu/user/v/vmannam/Desktop/Fall19/Dataset/3D data/3D_Zebrafish/'
#root_path = '/content/gdrive/My Drive/Fall19/I_vs_lifetime/Dataset/3D_data/Zebrafish_images/PM_FLIM'
#/content/gdrive/My Drive/Fall19/I_vs_lifetime/Dataset/PM-FLIM

#Unet model with batch_norm:
import torch
import torch.nn as nn

def conv3x3(in_channels, out_channels):
    return nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1, bias=False)

class UpsamplingNearest2d(nn.Module):
    def __init__(self, scale_factor=2):
        super().__init__()
        self.scale_factor = scale_factor
    
    def forward(self, x):
        return nn.functional.interpolate(x, scale_factor=self.scale_factor, mode='nearest')

class UnetN2Nv2(nn.Module):
    """
    Lehtinen, Jaakko, et al. "Noise2Noise: Learning Image Restoration without 
    Clean Data." arXiv preprint arXiv:1803.04189 (2018).
    Add BatchNorm and Tanh out activation
    """
    def __init__(self, in_channels, out_channels):
        super(UnetN2Nv2, self).__init__()

        self.enc_conv0 = conv3x3(in_channels, 48)
        self.enc_relu0 = nn.LeakyReLU(0.1)
        self.enc_conv1 = conv3x3(48, 48)
        self.enc_bn1 = nn.BatchNorm2d(48)
        self.enc_relu1 = nn.LeakyReLU(0.1)
        self.pool1 = nn.MaxPool2d(kernel_size=2)
        # 128
        self.enc_conv2 = conv3x3(48, 48)
        self.enc_bn2 = nn.BatchNorm2d(48)
        self.enc_relu2 = nn.LeakyReLU(0.1)
        self.pool2 = nn.MaxPool2d(kernel_size=2)
        # 64
        self.enc_conv3 = conv3x3(48, 48)
        self.enc_bn3 = nn.BatchNorm2d(48)
        self.enc_relu3 = nn.LeakyReLU(0.1)
        self.pool3 = nn.MaxPool2d(kernel_size=2)
        # 32
        self.enc_conv4 = conv3x3(48, 48)
        self.enc_bn4 = nn.BatchNorm2d(48)
        self.enc_relu4 = nn.LeakyReLU(0.1)
        self.pool4 = nn.MaxPool2d(kernel_size=2)
        # 16
        self.enc_conv5 = conv3x3(48, 48)
        self.enc_bn5 = nn.BatchNorm2d(48)
        self.enc_relu5 = nn.LeakyReLU(0.1)
        self.pool5 = nn.MaxPool2d(kernel_size=2)
        # 8
        self.enc_conv6 = conv3x3(48, 48)
        self.enc_bn6 = nn.BatchNorm2d(48)
        self.enc_relu6 = nn.LeakyReLU(0.1)
        self.upsample5 = UpsamplingNearest2d(scale_factor=2)
        # 16
        self.dec_conv5a = conv3x3(96, 96)
        self.dec_bn5a = nn.BatchNorm2d(96)
        self.dec_relu5a = nn.LeakyReLU(0.1)
        self.dec_conv5b = conv3x3(96, 96)
        self.dec_bn5b = nn.BatchNorm2d(96)
        self.dec_relu5b = nn.LeakyReLU(0.1)
        self.upsample4 = UpsamplingNearest2d(scale_factor=2)
        # 32
        self.dec_conv4a = conv3x3(144, 96)
        self.dec_bn4a = nn.BatchNorm2d(96)
        self.dec_relu4a = nn.LeakyReLU(0.1)
        self.dec_conv4b = conv3x3(96, 96)
        self.dec_bn4b = nn.BatchNorm2d(96)
        self.dec_relu4b = nn.LeakyReLU(0.1)
        self.upsample3 = UpsamplingNearest2d(scale_factor=2)
        # 64
        self.dec_conv3a = conv3x3(144, 96)
        self.dec_bn3a = nn.BatchNorm2d(96)
        self.dec_relu3a = nn.LeakyReLU(0.1)
        self.dec_conv3b = conv3x3(96, 96)
        self.dec_bn3b = nn.BatchNorm2d(96)
        self.dec_relu3b = nn.LeakyReLU(0.1)
        self.upsample2 = UpsamplingNearest2d(scale_factor=2)
        # 128
        self.dec_conv2a = conv3x3(144, 96)
        self.dec_bn2a = nn.BatchNorm2d(96)
        self.dec_relu2a = nn.LeakyReLU(0.1)
        self.dec_conv2b = conv3x3(96, 96)
        self.dec_bn2b = nn.BatchNorm2d(96)
        self.dec_relu2b = nn.LeakyReLU(0.1)
        self.upsample1 = UpsamplingNearest2d(scale_factor=2)
        # 256
        self.dec_conv1a = conv3x3(96 + in_channels, 64)
        self.dec_bn1a = nn.BatchNorm2d(64)
        self.dec_relu1a = nn.LeakyReLU(0.1)
        self.dec_conv1b = conv3x3(64, 32)
        self.dec_bn1b = nn.BatchNorm2d(32)
        self.dec_relu1b = nn.LeakyReLU(0.1)
        self.dec_conv1c = conv3x3(32, out_channels)
        self.dec_act = nn.Sigmoid()

    def forward(self, x):
        out_pool1 = self.pool1(self.enc_relu1(self.enc_bn1(self.enc_conv1(self.enc_relu0(self.enc_conv0(x))))))
        out_pool2 = self.pool2(self.enc_relu2(self.enc_bn2(self.enc_conv2(out_pool1))))
        out_pool3 = self.pool3(self.enc_relu3(self.enc_bn3(self.enc_conv3(out_pool2))))
        out_pool4 = self.pool4(self.enc_relu4(self.enc_bn4(self.enc_conv4(out_pool3))))
        out_pool5 = self.pool5(self.enc_relu5(self.enc_bn5(self.enc_conv5(out_pool4))))
        out = self.upsample5(self.enc_relu6(self.enc_bn6(self.enc_conv6(out_pool5))))
        out = self.upsample4(self.dec_relu5b(self.dec_bn5b(self.dec_conv5b(self.dec_relu5a(self.dec_bn5a(self.dec_conv5a(torch.cat((out, out_pool4), 1))))))))
        out = self.upsample3(self.dec_relu4b(self.dec_bn4b(self.dec_conv4b(self.dec_relu4a(self.dec_bn4a(self.dec_conv4a(torch.cat((out, out_pool3), 1))))))))
        out = self.upsample2(self.dec_relu3b(self.dec_bn3b(self.dec_conv3b(self.dec_relu3a(self.dec_bn3a(self.dec_conv3a(torch.cat((out, out_pool2), 1))))))))
        out = self.upsample1(self.dec_relu2b(self.dec_bn2b(self.dec_conv2b(self.dec_relu2a(self.dec_bn2a(self.dec_conv2a(torch.cat((out, out_pool1), 1))))))))
        out = self.dec_conv1c(self.dec_relu1b(self.dec_bn1b(self.dec_conv1b(self.dec_relu1a(self.dec_bn1a(self.dec_conv1a(torch.cat((out, x), 1))))))))
        out = self.dec_act(out)
        return out


    @property
    def model_size(self):
        return self._model_size()

    def _model_size(self):
        n_params, n_conv_layers = 0, 0
        for param in self.parameters():
            n_params += param.numel()
        for module in self.modules():
            if 'Conv' in module.__class__.__name__ \
                    or 'conv' in module.__class__.__name__:
                n_conv_layers += 1
        return n_params, n_conv_layers

#definition from here

import torch
import torchvision
import torch.nn as nn
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
import torchvision.datasets
import numpy as np
#import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
import torch.nn.functional as F
import time
from scipy.linalg import hadamard
from pylab import *
from torch.autograd import gradcheck
from torch.autograd import Variable
from torchvision import models
from torch.optim.lr_scheduler import ReduceLROnPlateau

# Hyperparameters
epochs = 100
batch_size = 2
test_batch_size = 2
learning_rate = 0.0001
lr = learning_rate
weight_decay=0.00001
wd = weight_decay
tau_min = 0e-9
tau_max = 10e-9

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Assume that we are on a CUDA machine, then this should print a CUDA device:
print('device is: ',device)
in_channels=1
out_channels = 3 #3 for hsv images and 1 for gray images
model = UnetN2Nv2(in_channels, out_channels).to(device)
#print(model)
#print(model.model_size)
optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=wd, betas=[0.9, 0.99])
scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=5)
train_samples = 140
test_samples = 16
iters_per_epoch = int(np.ceil(train_samples/batch_size))
n_train_per_epoch = iters_per_epoch * batch_size
test_iters_per_epoch = int(np.ceil(test_samples/test_batch_size))
n_test = test_iters_per_epoch * test_batch_size 

loss_list = []
loss_test_list = []
loss_list_step = []
loss_test_list_step = []

"""# Take input of 360x360 and split of 256x256 using partition

# Unet of 256x256
"""

tstart = time.time()
iters = 0
samples_size = 156
#print(root_path)
train_samples = 140
test_samples = 16
im_size = 360
imsize = 128
train_batches = np.ceil(train_samples/batch_size)
test_batches = np.ceil(test_samples/test_batch_size)

import glob  
from PIL import Image
import random
from random import shuffle
import matplotlib.pyplot as plt

files = [f for f in glob.glob(root_path + "**/*.tif", recursive=True)]
files =np.array(files)

test_list = [5,15,25,35,45,55,64,73,82,91,100,112,120,130,140,150]
train_list = list(range(0,156))
for i in test_list:
  if i in train_list:
    train_list.remove(i)
    
# l1= list(range(0,samples_size))
# l22= np.array(l1)
random.shuffle(train_list)
#l2 = list(l22[0:train_samples])
#l3 = list(l22[train_samples:samples_size])
#l3 = list(range(train_samples+1, train_samples+1+test_samples ))

#hsv conversion
hmin= 0
hmax = 0.7

#training here
for epoch in range(1, epochs + 1):
    model.train()
    mse = 0.
    #input1 = []
    #target1 = []
    for step in range(iters_per_epoch):
        # 500 x 4 x 5 = 10000 images per epoch
        input1 = []
        target1 = []
        iters += 1
        if (step+1)*batch_size <train_samples:
          indx = train_list[step*batch_size: (step+1)*batch_size]
        else: 
          indx = train_list[train_samples-batch_size:train_samples]
        #print('indx here', indx)
        for i in range(batch_size):
          ip_str1 = 'PM_FLIM_'
          ip_str2 = str(indx[i]).zfill(3)
          ip_str22 = '.tif'
          ip_str3 = ip_str1+ip_str2+ip_str22
          #print('>>>> ip_str3',ip_str3)
          
          for f in files:
            pos1 = f.find(ip_str3)
            #print('>>> pos1 here', pos1)
            if pos1>0:
              pos2  = pos1
              f1 = f
              ip_str4 = 'imageLifetime_'
              pos3 = f1.find(ip_str4)
              if pos3>0:
                target_file = f1
              else:
                input_file = f1
        
          #im = plt.imread(input_file)
#           print('index is here', indx[i])
          #print('file input:',input_file)
          #print('file target:',target_file)
          
          im = Image.open(input_file)
          im = np.array(im)
          for i in range(im_size):
            for j in range(im_size):
              if np.isnan(im[i,j]) == True:
                im[i,j]=0
          m1 = im.min()
          m2 = im.max()
          im = (im-m1)/(m2-m1)

          op = Image.open(target_file)
          op = np.array(op)
          for i in range(im_size):
            for j in range(im_size):
              if np.isnan(op[i,j]) == True:
                op[i,j]=0
          
          op  = np.clip(op, tau_min, tau_max) #//added a clip function for lifetime outside of limits  
          m11 = op.min()
          m22 = op.max()
          op = (op-m11)/(m22-m11)
          #import scipy.io as io
          #io.savemat('target_act_image.mat', dict([('target_act_image',op)]))
          
          tau1 = hmax + (hmin-hmax)*op;
          op_hsv = np.zeros((3,im_size,im_size),dtype=float)
          op_hsv[0,:,:] = tau1
          op_hsv[1,:,:] = np.ones((im_size,im_size),dtype=float)
          op_hsv[2,:,:] = im
          
          
          s1 = 256
          h_bt = int(np.ceil(im.shape[0]/s1))
          w_bt = int(np.ceil(im.shape[1]/s1))
          
          #print('>>> h_bt',h_bt)
          #print('>>> w_bt',w_bt)

          imx1 = np.zeros((h_bt*w_bt, s1, s1),dtype=float)
          opx1 = np.zeros((h_bt*w_bt, 3, s1, s1),dtype=float)
          #print('>>>',imx1.shape)

          for i in range(h_bt):
            #print('i is here>>>',i)
            for j in range(w_bt):
              #print('j is here>>>',j)
              if i==h_bt-1 and j==w_bt-1:
                imx1[i*h_bt+j, :,:] = im[im.shape[0]-s1:im.shape[0], im.shape[1]-s1:im.shape[1]]
                opx1[i*h_bt+j, :, :,:] = op_hsv[:,op_hsv.shape[1]-s1:op_hsv.shape[1], op_hsv.shape[2]-s1:op_hsv.shape[2]]
              else:
                if i==h_bt-1:
                    imx1[i*h_bt+j, :, :] = im[im.shape[0]-s1:im.shape[0], j*s1:(j+1)*s1]
                    opx1[i*h_bt+j, :, :, :] = op_hsv[:,op_hsv.shape[1]-s1:op_hsv.shape[1], j*s1:(j+1)*s1]
                else:
                  if j == w_bt-1:
                    imx1[i*h_bt+j, :, :] = im[i*s1:(i+1)*s1, im.shape[1]-s1:im.shape[1]]
                    opx1[i*h_bt+j, :, :, :] = op_hsv[:,i*s1:(i+1)*s1, op_hsv.shape[2]-s1:op_hsv.shape[2]]
                  else:          
                    imx1[i*h_bt+j, :, :] = im[i*s1:(i+1)*s1, j*s1:(j+1)*s1]
                    opx1[i*h_bt+j, :, :, :] = op_hsv[:,i*s1:(i+1)*s1, j*s1:(j+1)*s1]
          
          
          input1.append(imx1)
          target1.append(opx1)
        #print('ims1',imx1.shape)
        input1 = np.array(input1)
        #print('>>>> ips',input1.shape)
        target1 = np.array(target1)
        input1 = input1.reshape(batch_size*h_bt*w_bt,s1,s1)
        target1 = target1.reshape(batch_size*h_bt*w_bt,3,s1,s1)
        input1 = np.expand_dims(input1, axis=1)
        #target1 = np.expand_dims(target1, axis=1)
        input = torch.from_numpy(input1).float()
        target = torch.from_numpy(target1).float()
        
        
        # ip1 = input.cpu()
#         ip1 = ip1.detach().numpy()
#         ip1 = np.squeeze(ip1, axis=1)
#
#         tar1 = target.cpu()
#         tar1 = tar1.detach().numpy()
        #tar1 = np.squeeze(tar1, axis=1)

        #print('>>>> ip shape',input.shape)
        #print('>>>> tar shape',target.shape)
        import scipy.io as io
        #io.savemat('input_image.mat', dict([('input_image',ip1)]))
        #io.savemat('target_image.mat', dict([('target_image',tar1)]))
        
        input, target = input.to(device), target.to(device)
        
        model.zero_grad()
        estimated = model(input)
        #print('>>>> est shape',estimated.shape)
        
        est1 = estimated.cpu()
        est1 = est1.detach().numpy()
        #est1 = np.squeeze(est1, axis=1)
        
        #io.savemat('est_image.mat', dict([('est_image',est1)]))
        
        loss = F.mse_loss(estimated, target)
        #sys.exit(0)
        loss.backward()
        optimizer.step()

        mse += loss.item()
        #if iters % args.print_freq == 0:
        #print('[{}][{}|{}][{}|{}] training '.format(iters, step, iters_per_epoch, epoch, epochs))
        loss_list_step.append(mse)
    rmse = np.sqrt(mse / iters_per_epoch)
    loss_list.append(rmse)
    #print('RMSE train value is: \n',rmse)
    scheduler.step(rmse)
    
    
#testing here
# test ------------------------------
    with torch.no_grad():
        model.eval()
        mse = 0.
        
        for step in range(test_iters_per_epoch):
            #input, target = next(test_generator) 
            input2 = []
            target2 = []
            iters += 1
            if train_samples+((step+1)*test_batch_size) <train_samples+test_samples:
              indx = test_list[step*test_batch_size: (step+1)*test_batch_size]
            else: 
              indx = test_list[test_samples-test_batch_size:test_samples+1]
            
            for i in range(test_batch_size):
              ip_str1 = 'PM_FLIM_'
              ip_str2 = str(indx[i]).zfill(3) 
              ip_str22 = '.tif'
              ip_str3 = ip_str1+ip_str2+ip_str22

              for f in files:
                pos1 = f.find(ip_str3)
                if pos1>0:
                  pos2  = pos1
                  f1 = f
                  ip_str4 = 'imageLifetime_'
                  pos3 = f1.find(ip_str4)
                  if pos3>0:
                    target_file = f1
                  else:
                    input_file = f1

              #print('file input:',input_file)
              #print('file target:',target_file)
              im = Image.open(input_file)
              im = np.array(im)
              for i in range(im_size):
                for j in range(im_size):
                  if np.isnan(im[i,j]) == True:
                    im[i,j]=0
              m1 = im.min()
              m2 = im.max()
              im = (im-m1)/(m2-m1)
              
              op = Image.open(target_file)
              op = np.array(op)
              for i in range(im_size):
                for j in range(im_size):
                  if np.isnan(op[i,j]) == True:
                    op[i,j]=0
              
              op  = np.clip(op, tau_min, tau_max) #//added a clip function for lifetime outside of limits  
              m11 = op.min()
              m22 = op.max()
              op = (op-m11)/(m22-m11)
              
              tau1 = hmax + (hmin-hmax)*op;
              op_hsv = np.zeros((3,im_size,im_size),dtype=float)
              op_hsv[0,:,:] = tau1
              op_hsv[1,:,:] = np.ones((im_size,im_size),dtype=float)
              op_hsv[2,:,:] = im

              s1 = 256
              h_bt = int(np.ceil(im.shape[0]/s1))
              w_bt = int(np.ceil(im.shape[1]/s1))

              imx1 = np.zeros((h_bt*w_bt, s1, s1),dtype=float)
              opx1 = np.zeros((h_bt*w_bt, 3, s1, s1),dtype=float)
              #print('>>>',imx1.shape)

              for i in range(h_bt):
                #print('i is here>>>',i)
                for j in range(w_bt):
                  if i==h_bt-1 and j==w_bt-1:
                    imx1[i*h_bt+j, :,:] = im[im.shape[0]-s1:im.shape[0], im.shape[1]-s1:im.shape[1]]
                    opx1[i*h_bt+j, :, :,:] = op_hsv[:,op_hsv.shape[1]-s1:op_hsv.shape[1], op_hsv.shape[2]-s1:op_hsv.shape[2]]
                  else:
                    if i==h_bt-1:
                        imx1[i*h_bt+j, :, :] = im[im.shape[0]-s1:im.shape[0], j*s1:(j+1)*s1]
                        opx1[i*h_bt+j, :, :, :] = op_hsv[:,op_hsv.shape[1]-s1:op_hsv.shape[1], j*s1:(j+1)*s1]
                    else:
                      if j == w_bt-1:
                        imx1[i*h_bt+j, :, :] = im[i*s1:(i+1)*s1, im.shape[1]-s1:im.shape[1]]
                        opx1[i*h_bt+j, :, :, :] = op_hsv[:,i*s1:(i+1)*s1, op_hsv.shape[2]-s1:op_hsv.shape[2]]
                      else:          
                        imx1[i*h_bt+j, :, :] = im[i*s1:(i+1)*s1, j*s1:(j+1)*s1]
                        opx1[i*h_bt+j, :, :, :] = op_hsv[:,i*s1:(i+1)*s1, j*s1:(j+1)*s1]
              

              input2.append(imx1)
              target2.append(opx1)

            input2 = np.array(input2)
            target2 = np.array(target2)
            input2 = input2.reshape(test_batch_size*h_bt*w_bt,s1,s1)
            target2 = target2.reshape(test_batch_size*h_bt*w_bt, 3, s1,s1)
            input2 = np.expand_dims(input2, axis=1)
            #target2 = np.expand_dims(target2, axis=1)
            input = torch.from_numpy(input2).float()
            target = torch.from_numpy(target2).float() 

            input, target= input.to(device), target.to(device)

            estimated = model(input)
            loss = F.mse_loss(estimated, target)
            mse += loss.item()
            loss_test_list_step.append(mse)
        rmse = np.sqrt(mse / test_iters_per_epoch)
        loss_test_list.append(rmse)
        #print('RMSE test value is: \n',rmse)
        
np.savetxt("3D_zebrafish_PM_FLIM_train_rmse_hsv_m2.txt", np.array(loss_list))
np.savetxt("3D_zebrafish_PM_FLIM_test_rmse_hsv_m2.txt", np.array(loss_test_list)) 
np.savetxt("3D_zebrafish_PM_FLIM_train_rmse_step_hsv_m2.txt", np.array(loss_list_step))
np.savetxt("3D_zebrafish_PM_FLIM_test_rmse_step_hsv_m2.txt", np.array(loss_test_list_step))

plt.figure(1)
x = np.arange(0, epochs * iters_per_epoch, 1)  # -> x label
############### ploting the figures #######################
plot(x, np.array(loss_list_step), 'b')
plt.xlabel('steps')
plt.ylabel('Loss ', color='b')
plt.title('Train_loss') 
plt.savefig('Train_loss_steps1_3D_zebrafish_PM_FLIM_hsv_m2.png')

plt.figure(2)
x1 = np.arange(0, epochs * test_iters_per_epoch, 1)  # -> x label
plot(x1, np.array(loss_test_list_step), 'r')
plt.xlabel('steps')
plt.ylabel('Loss ', color='r')
plt.title('Test_loss') 
plt.savefig('Test_loss_steps1_3D_zebrafish_PM_FLIM_hsv_m2.png')


l1 = np.array(loss_list_step)
l2 = np.array(loss_test_list_step)
c1 = np.ceil(train_samples/batch_size).astype(int)
c2 = np.ceil(test_samples/test_batch_size).astype(int)
x11 = np.reshape(l1.T, (epochs, c1))
x21 = np.reshape(l2.T, (epochs, c2))
x1mean = np.zeros(epochs)
x2mean = np.zeros(epochs)
for i in range(epochs):
    x1mean[i] = np.mean(x11[i, :])
    x2mean[i] = np.mean(x21[i, :])
    
np.savetxt("3D_zebrafish_PM_FLIM_train_rmse_epochs_hsv_m2.txt", np.array(x1mean))
np.savetxt("3D_zebrafish_PM_FLIM_test_rmse_epochs_hsv_m2.txt", np.array(x2mean))
def generateNumber(num):
    mylist = []
    for i in range(num):
        mylist.append(i)
    return mylist
plt.figure(3)
xp = np.array(generateNumber(epochs))
plt.plot(xp, x1mean, 'm*', label='Train_loss')
plt.plot(xp, x2mean, 'ks', label='Test_loss')
plt.xlabel('Num_epochs ')
plt.ylabel('Train and Test Loss ')
plt.title('Train and Test Loss ')
plt.legend(loc='best', frameon=False)
plt.savefig('3D_zebrafish_PM_FLIM_Train_Test_Loss_hsv_m2.png')

tend = time.time()
print('Total Execution time is = ', tend - tstart)  
torch.save(model,'3D_zebrafish_PM_FLIM_UNET_Model_norm_hsv_m2.pt')

# Model class must be defined somewhere
model = torch.load('3D_zebrafish_PM_FLIM_UNET_Model_norm_hsv_m2.pt')
model.eval()
#for step in range(test_iters_per_epoch):
#input, target = next(test_generator) 
input3 = []
target3 = []

test_list = [5,15,25,35,45,55,64,73,82,91,100,112,120,130,140,150]
random.shuffle(test_list)
test_indx1 = test_list[8]
indx = 73 #test_indx1 now not random here
bs=1
for i in range(bs):
  ip_str1 = 'PM_FLIM_'
  ip_str2 = str(indx).zfill(3)
  ip_str22 = '.tif'
  ip_str3 = ip_str1+ip_str2+ip_str22

  for f in files:
    pos1 = f.find(ip_str3)
    if pos1>0:
      pos2  = pos1
      f1 = f
      ip_str4 = 'imageLifetime_'
      pos3 = f1.find(ip_str4)
      if pos3>0:
        target_file = f1
      else:
        input_file = f1

  print('file input:',input_file)
  print('file target:',target_file)
  im = Image.open(input_file)
  im = np.array(im)
  for i in range(im_size):
    for j in range(im_size):
      if np.isnan(im[i,j]) == True:
        im[i,j]=0
  #im = Image.open(input_file)
  m1 = im.min()
  m2 = im.max()
  im = (im-m1)/(m2-m1)
  
  
        
  #op = plt.imread(target_file)
  op = Image.open(target_file)
  op = np.array(op)
  for i in range(im_size):
    for j in range(im_size):
      if np.isnan(op[i,j]) == True:
        op[i,j]=0
  op  = np.clip(op, tau_min, tau_max) #//added a clip function for lifetime outside of limits  
  m11 = op.min()
  m22 = op.max()
  #print('m22 is  here',m11)
  op = (op-m11)/(m22-m11)
 
  tau1 = hmax + (hmin-hmax)*op;
  op_hsv = np.zeros((3,im_size,im_size),dtype=float)
  op_hsv[0,:,:] = tau1
  op_hsv[1,:,:] = np.ones((im_size,im_size),dtype=float)
  op_hsv[2,:,:] = im
        
  s1 = 256
  h_bt = int(np.ceil(im.shape[0]/s1))
  w_bt = int(np.ceil(im.shape[1]/s1))


  imx1 = np.zeros((h_bt*w_bt, s1, s1),dtype=float)
  opx1 = np.zeros((h_bt*w_bt, 3, s1, s1),dtype=float)
  #print('>>>',imx1.shape)
  
  
  for i in range(h_bt):
    #print('i is here>>>',i)
    for j in range(w_bt):
      #print('j is here>>>',j)
      if i==h_bt-1 and j==w_bt-1:
        imx1[i*h_bt+j, :,:] = im[im.shape[0]-s1:im.shape[0], im.shape[1]-s1:im.shape[1]]
        opx1[i*h_bt+j, :, :,:] = op_hsv[:, op_hsv.shape[1]-s1:op_hsv.shape[1], op_hsv.shape[2]-s1:op_hsv.shape[2]]
      else:
        if i==h_bt-1:
            imx1[i*h_bt+j, :, :] = im[im.shape[0]-s1:im.shape[0], j*s1:(j+1)*s1]
            opx1[i*h_bt+j, :, :, :] = op_hsv[:, op_hsv.shape[1]-s1:op_hsv.shape[1], j*s1:(j+1)*s1]
        else:
          if j == w_bt-1:
            imx1[i*h_bt+j, :, :] = im[i*s1:(i+1)*s1, im.shape[1]-s1:im.shape[1]]
            opx1[i*h_bt+j, :, :, :] = op_hsv[:, i*s1:(i+1)*s1, op_hsv.shape[2]-s1:op_hsv.shape[2]]
          else:          
            imx1[i*h_bt+j, :, :] = im[i*s1:(i+1)*s1, j*s1:(j+1)*s1]
            opx1[i*h_bt+j, :, :, :] = op_hsv[:, i*s1:(i+1)*s1, j*s1:(j+1)*s1]
  
  
  print('imx1 shape',imx1.shape)
  x1 = Image.fromarray(im)
  imsave('x1.png', x1)
  #plt.show(x1)
  import scipy.io as io
  io.savemat('input_test_hsv_m2.mat', dict([('input_test_hsv_m2',im)]))
  x2 = Image.fromarray(op)
  imsave('x2.png', x2)
  #plt.show(x2)
  import scipy.io as io
  io.savemat('target_test_hsv_m2.mat', dict([('target_test_hsv_m2',op)]))
  #sys.exit(0)
  input3.append(imx1)
  target3.append(opx1)
  #print('>>>',len(input3))

  
input3 = np.array(input3)
target3 = np.array(target3)
input3 = input3.reshape(bs*h_bt*w_bt,s1,s1)
target3 = target3.reshape(bs*h_bt*w_bt,3,s1,s1)

input3 = np.expand_dims(input3, axis=1)
#target3 = np.expand_dims(target3, axis=1)
input = torch.from_numpy(input3).float()
target = torch.from_numpy(target3).float()

print('ip shape >>>>',input.shape)
print('op shape >>>>',target.shape)

input, target= input.to(device), target.to(device)

estimated = model(input)
loss_test = F.mse_loss(estimated, target)
print(loss_test)

estimated = estimated.cpu()
estimated = estimated.detach().numpy()
#estimated = np.squeeze(estimated, axis=1)
print('>>>>>',estimated.shape)


#Reconstruct here
est2 = np.zeros( (3, im.shape[0], im.shape[1]),dtype=float)
est_s =  est2.shape
#print('>>>><<<<',est_s)
for i in range(h_bt):
  #print('i is here>>>',i)
  for j in range(w_bt):
    if i!=h_bt-1 and j!=w_bt-1: #normal here
      est2[:,i*s1:(i+1)*s1, j*s1:(j+1)*s1] = estimated[i*h_bt+j, :, :,:]
    else:
      if i==h_bt-1 and j == w_bt-1: #bot edges are gone
        est2[:,i*s1:est_s[1],j*s1:est_s[2]] = estimated[i*h_bt+j,:, s1-(est_s[1]-i*s1):s1,s1-(est_s[2]-j*s1):s1]
      else:
        if j == w_bt-1: #y axis is gone
          est2[:,i*s1:(i+1)*s1,j*s1:est_s[2]] = estimated[i*h_bt+j,:, :,s1-(est_s[2]-j*s1):s1]
        else:  # i==h_bt-1   #x axis is gone
          est2[:,i*s1:est_s[1], j*s1:(j+1)*s1] = estimated[i*h_bt+j,:, s1-(est_s[1]-i*s1):s1,:]
          
# x3 = Image.fromarray(est2)
# imsave('x3.png', x3)
# plt.show(x3)
import scipy.io as io
io.savemat('estimated_test_hsv_m2_3d.mat', dict([('estimated_test_hsv_m2_3d',est2)]))