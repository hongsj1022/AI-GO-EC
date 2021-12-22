import torchvision
from car.utils.utils import rescale_boxes
from car.models.model_dist import *
from car.models.roipool import *
from car.models.models import *
import os
import cv2
import time
import torch


class DetectionModel:
    '''
    @param cfg: cfg['models']['detection_model']
    '''
    def __init__(self, cfg):
        self.model = Darknet(cfg['model_def'], img_size=cfg['img_size']).to(torch.device('cuda'))
        self.model.load_state_dict(torch.load(cfg['path']))
        self.result = []

    def predict(self, img, ori_img):
        result = []
        with torch.no_grad():
            detections = self.model(img)
            detections = non_max_suppression(detections, 0.8, 0.4)
        self.result.clear()
        if detections is not None:
            self.result.extend(detections)
        
        if len(self.result):
            for detection in self.result:
                if detection is not None:
                    detections = rescale_boxes(detection, 416, (480, 640))
                    detections = detections[:, :4]
                    # for x1, y1, x2, y2 in detections:
                    #     box_h = x2-x1
                    #     img = cv2.rectangle(ori_img, (x1, y1+box_h), (x2, y1), (255, 0, 0), 2)
                    # cv2.imshow('img', img)
                    # cv2.waitKey(1)
                    
                    detections[:, 0] = detections[:, 0] / 640
                    detections[:, 1] = detections[:, 1] / 480
                    detections[:, 2] = detections[:, 2] / 640
                    detections[:, 3] = detections[:, 3] / 480
                    file_num = len(os.listdir("/home/aigo/toCore/car/images"))
                    if file_num >= 1000:
                        pass
                    else:
                        cv2.imwrite("/home/aigo/toCore/car/images/"+ str(file_num) + ".jpg", ori_img)

                    return detections            
                else:
                    return None


class DistanceModel:
    '''
    @Param cfg: cfg['models']['distance_model']
    '''
    def __init__(self, cfg):
        self.vgg16 = torchvision.models.vgg16(pretrained=True).to(torch.device('cuda'))
        self.vgg16.eval()
        self.feature_extractor = self.vgg16.features

        self.roipool = ROIPool((2, 2)).to(torch.device('cuda'))
        self.roipool.eval()

        self.distance_model = Dist().to(torch.device('cuda'))
        self.distance_model.load_state_dict(torch.load(cfg['path']))
        self.distance_model.eval()


    def predict(self, img, bboxes):
        feature_list = []
        distance_list = []
        with torch.no_grad():
            feature_map = self.feature_extractor(img)
            if bboxes is not None:
                for bbox in bboxes:
                    try:
                        #print(f'bboxes: {bboxes}\nbbox: {bbox}')
                        roi = self.roipool(feature_map, bbox)
                        feature_list.append(roi)
                    except:
                        return None
                for i in range(len(feature_list)):
                    output = self.distance_model(feature_list[i])
                    distance_list.append(output)
                file_num = len(os.listdir('/home/aigo/toCore/car/labels'))
                if file_num >= 1000:
                    pass
                else:
                    with open("/home/aigo/toCore/car/labels/" + str(file_num) + ".txt", "w") as f:
                        for idx, detection in enumerate(bboxes):
                            f.write(f'{detection} {distance_list[idx]}\n')

                return distance_list
            else:
                return None

class MLEngine:
    '''
    @Param cfg: cfg['models]
    '''
    def __init__(self, cfg):
        self.detection_model = DetectionModel(cfg['detection_model'])
        self.distance_model = DistanceModel(cfg['distance_model'])

    def predict(self, img, ori_img):
        detection_results = self.detection_model.predict(img, ori_img)
        distance_results = self.distance_model.predict(img, detection_results)
        '''
        if distance_results is not None:
            for x1, y1, x2, y2 in detection_results:
                box_h = x2-x1
                img2 = cv2.rectangle(ori_img, (x1, y1+box_h), (x2, y1), (255, 0, 0), 2)
            cv2.imshow('img', img2)
            cv2.waitKey(1)
        else:
            cv2.imshow('img', ori_img)
            cv2.waitKey(1)
        '''
        return detection_results, distance_results
