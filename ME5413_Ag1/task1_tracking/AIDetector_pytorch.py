import torch
import numpy as np
from models.experimental import attempt_load
from utils.general import non_max_suppression, scale_coords, letterbox
from utils.torch_utils import select_device
from utils.BaseDetector import baseDet
from transformers import AutoImageProcessor, DetrForObjectDetection

class Detector(baseDet):

    def __init__(self):
        super(Detector, self).__init__()
        self.init()
        self.build_config()
        

    def init(self):
        model = DetrForObjectDetection.from_pretrained("./detr-resnet-50")
        
        self.device = '0' if torch.cuda.is_available() else 'cpu'
        self.device = select_device(self.device)
        
        self.m = model
        self.image_processor = AutoImageProcessor.from_pretrained("./detr-resnet-50")

    def imgprocess(self, img):

        inputs = self.image_processor(images=img, return_tensors="pt")

        return inputs

    def detect(self, im):

        inputs = self.imgprocess(im)

        outputs = self.m(**inputs)
        target_sizes = torch.tensor([im.size[::-1]])
        pred = self.image_processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[0]

        pred_boxes = []

        for score, label, box in zip(pred["scores"], pred["labels"], pred["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            lbl = self.m.config.id2label[label.item()]
            conf = round(score.item(), 3)
            x1, y1 = int(box[0]), int(box[1])
            x2, y2 = int(box[2]), int(box[3])
            pred_boxes.append(
                (x1, y1, x2, y2, lbl, conf))

        return im, pred_boxes

