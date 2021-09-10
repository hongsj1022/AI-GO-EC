from __future__ import division

from car.utils.datasets import *
from car.utils.datasets_detection import *

from car.models import *
from car.utils.utils import *
from car.roipool import *
from car.model_dis import *

import os, sys, time, datetime, argparse
import cv2
import torch, torchvision
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torch.autograd import Variable

from PIL import Image

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import NullLocator

if __name__ == '__main__':
    
    devi
