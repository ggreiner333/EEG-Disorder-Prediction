import os
from os.path import dirname
from pathlib import Path

import numpy as np
import torch
from torch.utils import data

import mne


from Model.dataset import MultiModalDataset
from Model.dataset import SplitDataset
from Model.mentalModel import MENTAL


##################################################################################################
##################################################################################################
##################################################################################################

batch = 20


test = np.loadtxt(os.path.join('TDBRAIN', 'complete_samples_EC.csv'), delimiter=",", dtype=float)

# Create Dataset and Dataset Loader
mm_dataset = MultiModalDataset('complete_samples_EC.csv', 'TDBRAIN')
dataset_loader = data.DataLoader(mm_dataset, batch_size=batch, shuffle=True)

main_dataset = SplitDataset('complete_samples_EC.csv', 'TDBRAIN')
main_loader  = data.DataLoader(main_dataset, batch_size=batch, shuffle=True)


my_mental = MENTAL(60, 3, 3, batch)

optimizer = torch.optim.Adam(my_mental.parameters(), lr=1e-7, weight_decay=1e-9)

epochs = 1000

for epoch in range(epochs):

    for (d_entry, n_entry, p_entry, label) in main_loader:

        h = (d_entry, d_entry)

        h[0].unsqueeze_(-1)
        h0 = h[0].transpose(1,2)
        h0 = h0.transpose(0,1)

        h[1].unsqueeze_(-1)
        h1 = h[1].transpose(1,2)
        h1 = h1.transpose(0,1)
        h1 = h1.squeeze(-1)

        h = (h0,h1)

        for p in p_entry:
            output, h = my_mental.forward(p, n_entry, h)

        output.squeeze_(-1)
        output.squeeze_(-1)
        print("---------------------------")
        print(output)
        print(label)
        print("---------------------------")
        loss = torch.nn.MSELoss()
        res = loss(output, label)

        optimizer.zero_grad()
        res.backward()
        optimizer.step()

    print("-----------------------")
    print("Epoch: " + str(epoch))
    print(" Loss: " + str(res) )
    print("-----------------------")

