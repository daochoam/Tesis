from .Modules import Gabor_Filter, Seg_Image, Visual
import matplotlib.pyplot as plt
import numpy as np
import imutils
from imutils import perspective
import cv2

class Imag_Process(Gabor_Filter,Seg_Image,Visual):
    def __init__(self):
        Gabor_Filter.__init__(self)
        Seg_Image.__init__(self)
        Visual.__init__(self)