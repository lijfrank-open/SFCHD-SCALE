import warnings
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.checkpoint import checkpoint
import os
import math
# from torch.nn.functional import interpolate, conv2d
import cv2
from torchvision import transforms
import numpy as np

class SpatialAttention(nn.Module):
    def __init__(self, kernel_size=3):
        super().__init__()
        assert kernel_size in (3, 5, 7), "kernel size must be 3 or 5 or 7"

        self.conv = nn.Conv2d(2,
                              1,
                              kernel_size,
                              padding=kernel_size // 2,
                              bias=False)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        
        avgout = torch.mean(x, dim=1, keepdim=True) #torch.Size([8, 1, 608, 480])
        maxout, _ = torch.max(x, dim=1, keepdim=True)

        attention = torch.cat([avgout, maxout], dim=1) #torch.Size([8, 2, 608, 480])

        attention = self.conv(attention) #torch.Size([8, 1, 608, 480])

        return self.sigmoid(attention) * x


class Parallel_conv(nn.Module):
    def __init__(self, in_channels, ):
        super(Parallel_conv, self).__init__()
        
        self.encoder = nn.Sequential(nn.Conv2d(3, 16, 3, padding=1),
                                     nn.LeakyReLU(inplace=True),
                                     nn.Conv2d(16, in_channels, 3, padding=1),
                                     nn.LeakyReLU(inplace=True),
                                    )

        self.conv1 = nn.Conv2d(in_channels,
                             in_channels,
                             kernel_size=1,
                             padding=0)
        self.conv2 = nn.Conv2d(in_channels,
                             in_channels,
                             kernel_size=3,
                             padding=3 // 2)
        self.conv3 = nn.Conv2d(in_channels,
                             in_channels,
                             kernel_size=5,
                             padding=5 // 2)
        
    def forward(self, x):
        x = self.encoder(x)
        x1 = self.conv1(x)
        x2 = self.conv2(x)
        x3 = self.conv3(x)
        # x1_4 = self.mm1(x1)
        x = torch.cat([x1, x2, x3], dim=1)
        return x
class SA_double_attention(nn.Module):
    def __init__(self, in_channels=32):
        super().__init__()
        self.parallel_conv = Parallel_conv(in_channels)

        self.attention1 = nn.Sequential(
            SpatialAttention(3)
        )
        self.attention2 = nn.Sequential(
            SpatialAttention(5)
        )
        self.decoder = nn.Sequential(nn.Conv2d(in_channels * 6, in_channels*3, 3, padding=1),
                                     nn.LeakyReLU(inplace=True),
                                     nn.Conv2d(in_channels * 3, in_channels, 3, padding=1),
                                     nn.LeakyReLU(inplace=True),
                                     nn.Conv2d(in_channels, 3, 3, padding=1))

    def forward(self, x):
        x = self.parallel_conv(x)
        attention1 = self.attention1(x)
        attention2 = self.attention2(x)
        cat_attention = torch.cat([attention1, attention2], dim = 1)
        x = self.decoder(cat_attention)
        return x


class SEBlock(nn.Module):
    def __init__(self, channel, reduction=16):
        super(SEBlock, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(channel, channel // reduction, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(channel // reduction, channel, bias=False),
            nn.Sigmoid()
        )

    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)  # Squeeze
        y = self.fc(y)  # Excitation
        return x * y.view(b, c, 1, 1)  # Scale

class CBL(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride=1):
        super().__init__()

        self.conv = nn.Conv2d(in_channels,
                             out_channels,
                              kernel_size,
                              stride,
                              kernel_size // 2,
                              bias=False)
        self.bn = nn.BatchNorm2d(out_channels)
        self.act = nn.LeakyReLU(0.1, inplace=True)

    def forward(self, x):
        return self.act(self.bn(self.conv(x)))

class Resblock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, 1)
        self.block = nn.Sequential(
            # CBL(in_channels, in_channels // 2, kernel_size=1),
            # CBL(in_channels // 2, out_channels, kernel_size=3))
            CBL(in_channels, in_channels, kernel_size=1),
            CBL(in_channels, out_channels, kernel_size=3))
    def forward(self, x):
        x1 = self.conv(x)
        # print('ffffffffff')
        # print(x1.shape)
        # print(self.block(x).shape)
        return x1 + self.block(x)  # res

class CA(nn.Module):
    def __init__(self, in_channels=32):
        super().__init__()

        self.res1 = Resblock(3, in_channels)
        self.se_block = SEBlock(channel=in_channels)
        self.res2 = Resblock(in_channels, 3)
    def forward(self, x):
        x = self.res1(x)
        x = self.se_block(x)

        x = self.res2(x)
        return x


class CA_skip(nn.Module):
    def __init__(self, in_channels=32):
        super().__init__()

        self.res1 = Resblock(3, in_channels)
        self.se_block = SEBlock(channel=in_channels)
        self.res2 = Resblock(in_channels, 3)
    def forward(self, x):
        x1 = self.res1(x)
        x = self.se_block(x1)
        x = x + x1
        x = self.res2(x)
        return x

class PArallel_Attention_double_SA(nn.Module):
    def __init__(self,):
        super(PArallel_Attention_double_SA, self).__init__()
        
        # self.pretrained = pretrained
        # assert not (init_cfg and pretrained), \
        #     'init_cfg and pretrained cannot be setting at the same time'
        # if isinstance(pretrained, str):
        #     warnings.warn('DeprecationWarning: pretrained is deprecated, '
        #                   'please use "init_cfg" instead')
        #     self.init_cfg = dict(type='Pretrained', checkpoint=pretrained)
        # elif pretrained is None:
        #     if init_cfg is None:
        #         self.init_cfg = [
        #             dict(type='Kaiming', layer='Conv2d'),
        #             dict(
        #                 type='Constant',
        #                 val=1,
        #                 layer=['_BatchNorm', 'GroupNorm'])
        #         ]
        # else:
        #     raise TypeError('pretrained must be a str or None')

        self.sa = SA_double_attention(in_channels=32)
        self.ca = CA(in_channels=32)

    def forward(self, img_low):
        # print('hhhhhhh')
        # print(img_low.shape)
        sa_map = self.sa(img_low)
        ca_map = self.ca(img_low)
        out = sa_map + ca_map
        return out
    