import cv2
import numpy as np
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.utils.visualizer import ColorMode, Visualizer
from detectron2 import model_zoo
from detectron2.projects import point_rend
import detectron2
import torch

from detectron2.utils.logger import setup_logger
setup_logger()


# You may need to restart your runtime prior to this, to let your installation take effect
# Some basic setup:
# Setup detectron2 logger
setup_logger()


class Detector:
    def __init__(self, model_type="OD", score_thresh=0.7):
        self.cfg = get_cfg()
        self.model_type = model_type
        self.score_thresh = score_thresh
        self.config_Detect = "COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"
        self.config_InsSeg = "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
        self.config_LIVS = "LVISv0.5-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_1x.yaml"

    def Predict(self):
        if self.model_type == "OD":  # Object Detection
            self.cfg.merge_from_file(
                model_zoo.get_config_file(self.config_Detect))
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
                self.config_Detect)
        elif self.model_type == "IS":  # Instance Segmentation
            self.cfg.merge_from_file(
                model_zoo.get_config_file(self.config_InsSeg))
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
                self.config_InsSeg)
        elif self.model_type == "LVIS":  # Instance Segmentation
            self.cfg.merge_from_file(
                model_zoo.get_config_file(self.config_LIVS))
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
                self.config_LIVS)
        elif self.model_type == "PR":  # Point Rend
            point_rend.add_pointrend_config(self.cfg)
            self.cfg.merge_from_file(
                "/opt/detectron2/projects/PointRend/configs/InstanceSegmentation/pointrend_rcnn_X_101_32x8d_FPN_3x_coco.yaml")
            self.cfg.MODEL.WEIGHTS = "detectron2://PointRend/InstanceSegmentation/pointrend_rcnn_X_101_32x8d_FPN_3x_coco/28119989/model_final_ba17b9.pkl"
        elif self.model_type == "ML2R":
            self.cfg.merge_from_file(
                model_zoo.get_config_file(self.config_InsSeg))
            self.cfg.MODEL.WEIGHTS = "/opt/models_NN/FAT_trained_Ml2R_bin_fine_tuned.pth"
            self.cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
            self.cfg.MODEL.SEM_SEG_HEAD.NUM_CLASSES = 1
            self.cfg.MODEL.ROI_BOX_HEAD.CLS_AGNOSTIC_BBOX_REG = True
            self.cfg.MODEL.ROI_MASK_HEAD.CLS_AGNOSTIC_MASK = True

        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = self.score_thresh

        if torch.cuda.is_available():
            self.cfg.MODEL.DEVICE = "cuda"
        else:
            # set device to cpu
            self.cfg.MODEL.DEVICE = "cpu"

        predictor = DefaultPredictor(self.cfg)
        return predictor

    def Image_Predict(self, imagesPath, predict):
        predictions = predict(imagesPath)
        return predictions

    def Image_Segment(self, imagesPath, prediction):
        if 'user_data' in [x for x in MetadataCatalog]:
            MetadataCatalog.remove('user_data')
        MetadataCatalog.get("user_data").set(thing_classes=[""])
        metadata = MetadataCatalog.get("user_data")
        viz = Visualizer(imagesPath[:, :, ::-1],
                         metadata=MetadataCatalog.get(
                             self.cfg.DATASETS.TRAIN[0]),
                         instance_mode=ColorMode.IMAGE)
        out = viz.draw_instance_predictions(prediction["instances"].to("gpu"))
        img = out.get_image()[:, :, ::-1]
        return img

    def Detect_Contours(self, predict):
        self.predict = predict
        contours = []
        for pred_mask in self.predict["instances"].pred_masks:
            # pred_mask is of type torch.Tensor, and the values are boolean (True, False)
            # Convert it to a 8-bit numpy array, which can then be used to find contours
            mask = pred_mask.numpy().astype('uint8')
            contour, _ = cv2.findContours(
                mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # contour is a tuple (OpenCV 4.5.2), so take the first element which is the array of contour points
            contours.append(contour[0])
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        return contours
