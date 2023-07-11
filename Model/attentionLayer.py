import os
from os.path import dirname
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt

import torch
import torch.nn as nn

import mne
import math


##################################################################################################
##################################################################################################
##################################################################################################

class AttentionLayer(nn.Module):

    def __init__(self, dk, dv, batch):
        super().__init__()

        self.dk = dk
        self.dv = dv

        self.W_q = nn.Linear(batch, 1, dk)
        self.W_k = nn.Linear(batch, 1, dk)
        self.W_v = nn.Linear(batch, 1, dv)

        self.softmax = nn.Softmax(dim=-1)

    def forward(self, q, k, v):
        print("Q size: " + str(q.size()))
        print("K size: " + str(k.size()))
        print("V size: " + str(v.size()))

        q = self.W_q(q.transpose(0,1))
        k = self.W_k(k.transpose(0,1))
        v = self.W_v(v.transpose(0,1))

        print("Q size: " + str(q.size()))
        print("K size: " + str(k.size()))
        print("V size: " + str(v.size()))

        k = k.transpose(0,1)

        res = torch.matmul(q,k) / math.sqrt(self.dk)
        res = self.softmax(res)

        out = torch.matmul(res, v)

        return out, res

        