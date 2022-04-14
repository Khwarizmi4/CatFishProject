#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 18:57:03 2022

@author: admin
"""

import torch
from torch.utils.data import Dataset
from skimage import io
import torch.nn as nn # ALL neural network modules, nn.linear, nn.Conv2d, Batchnorm, Loss functions
import torch.optim as optim # For all Optimization algorithms, SGD, Adam, etc.
import torchvision.transforms as transforms # Transformations we can perform on our dataset
import torchvision
from torch.utils.data import DataLoader # Gives easier dataset management and creates minibatches
from CatfishEmbryoDataSet import CatfishEmbryosDataset

# Set device
device = torch.device ('cuda' if torch.cuda.is_available() else 'cpu')

# Hyperparameters
in_channel = 3
num_classes = 10
learning_rate = 1e-3
batch_size = 517
num_epochs = 1

# Loaded Data
dataset = CatfishEmbryosDataset(csv_file = 'CFD.csv', root_dir = '/Users/admin' ,
                                transform = transforms.ToTensor())

train_set, test_set = torch.utils.data.random_split(dataset, [521, 522])
train_loader = DataLoader(dataset = train_set, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(dataset = test_set, batch_size=batch_size, shuffle=True)

# Model
model = torchvision.models.googlenet(pretrained=True)
model.to(device)
# Loss and optimizer

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Train Network
for epoch in range(num_epochs):
    losses = []
    
    for batch_idx, (data, targets) in enumerate(train_loader):
        # Get data to cuda if possible
        data = data.to(device=device)
        targets = targets.to(device=device)
        
        # forward
        scores = model(data)
        loss = criterion(scores, targets)
        
        losses.append(loss.item())
        
        # backward
        optimizer.zero_grad()
        loss.backward()
        
        # gradient descent or adam step
        optimizer.step()

    print('Cost at epoch {epoch} is {sum(Losses)/Len(Losses)}')  
    
# Check accuracy on training to see how good our model is
def check_accuracy(loader, model):
    num_correct = 0
    num_samples = 0
    model.eval()
    
    with torch.no.grad:
        for x, y in loader:
            x = x.to(device=device)
            y = y.to(device=device)
            
            scores = model(x)
            _, predictions = scores.max(1)
            num_correct += (predictions == y).sum()
            num_samples += predictions.size(0)
            
        print
        
    model.train()
    
print("Checking accuracy on Training Set")
check_accuracy(train_loader, model)
print("Checking accuracy on Testing Set")
check_accuracy(test_loader, model)

