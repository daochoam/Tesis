import matplotlib.pyplot as plt
import numpy as np
import cv2

class Gabor_Filter:
    def __init__(self):
        self.__K_size = np.array([3.,5.],dtype=np.int32)
        self.__Sigma= np.array([1, 2 * np.sqrt(2.0)], dtype=np.double)
        self.__Theta=np.arange(0, np.pi, np.pi / 8)
        self.__Lamda=np.array([3.,5.,7.], dtype=np.double)
        self.__Gamma=np.array([0.05,0.5,2.0], dtype=np.double)
        self.__Psi=0.0
        self.__Ktype=cv2.CV_32F
    
    def set_k(self,k_size):
        self.__K_size = k_size
    
    def set_sigma(self,sigma):
        self.__Sigma = sigma
    
    def set_theta(self,theta):
        self.__Theta = theta
    
    def set_lamda(self,gamma):
        self.__Gamma = gamma
    
    def set_psi(self,psi):
        self.__Psi = psi
    
    def set_ktype(self):
        self.__Ktype = cv2.CV_64F

    def get_k(self):
        return self.__K_size
    
    def get_sigma(self):
        return self.__Sigma
    
    def get_theta(self):
        return self.__Theta
    
    def get_lamda(self):
        return self.__Gamma
    
    def get_psi(self):
        return self.__Psi
    
    def get_ktype(self):
        return self.__Ktype

    def Filters_Gabor(self,*args):
        """
        Filters_Gabor(self,k_size,sigma,theta,lamda,gamma,psi,normalized,ktype):
        --> ksize - size of gabor filter (n, n)
        --> sigma - standard deviation of the gaussian function
        --> theta - orientation of the normal to the parallel stripes
        --> gamma - spatial aspect ratio
        --> psi - phase offset
        --> ktype - type and range of values that each pixel in the gabor kernel can hold
        """
        filters = []
        for K in self.__K_size:
            for T in self.__Theta:
                for S in self.__Sigma:
                    for L in self.__Lamda:
                        for G in self.__Gamma:
                                params = {'ksize':(K, K), 'sigma':S, 'theta':T, 'lambd':L, 'gamma':G, 'psi':self.__Psi, 'ktype':self.__Ktype}
                                kernels = cv2.getGaborKernel(**params)
                                kernels /= np.linalg.norm(kernels)
                                filters.append((kernels,params))
        return filters
    
    def Process_Gabor(self,image,filters):
        Acc = np.zeros_like(image)
        for kern,params in filters:
            fimg = cv2.filter2D(image, cv2.CV_8UC3, kern)
            np.maximum(Acc, fimg, Acc)
        return Acc