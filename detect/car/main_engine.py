from car.utils.datasets_detection import *
from car.utils.datasets import *
from car.utils.utils import *

from car.ml_engine import MLEngine


import torch
import torchvision
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.autograd import Variable

from PIL import Image
import cv2
import os

class MainEngine:
    def __init__(self, cfg):
        self.input_type = cfg['main_engine']['input_type']
        self.camera_number = cfg['main_engine']['device_number']
        self.input_path = cfg['main_engine']['input_path']
        self.window_horizontal_size = cfg['main_engine']['window_horizontal_size']
        self.window_vertical_size = cfg['main_engine']['window_vertical_size']
         
        self.show_on_gui = False
        self.Tensor = torch.cuda.FloatTensor

        self.ml_engine = MLEngine(cfg['ml_engine'])

    def detect(self, frame):
        # RGBimg = changeBGR2RGB(frame)
        # imgTensor = transforms.ToTensor()(RGBimg)
        imgTensor = transforms.ToTensor()(frame)
        imgTensor, _ = pad_to_square(imgTensor, 0)
        imgTensor = resize(imgTensor, 416)

        imgTensor = imgTensor.unsqueeze(0)
        imgTensor = Variable(imgTensor.type(self.Tensor))

        detections, distances = self.ml_engine.predict(imgTensor, frame)
        return detections, distances

    def run(self, img):

        self.detect(img)
    
