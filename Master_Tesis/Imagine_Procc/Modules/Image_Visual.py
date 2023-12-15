import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import cv2
class Visual:
    def __init__(self):
        self.image = None

    def Image_Show (self,image, name_window):
        self.image = image
        cv2.namedWindow(name_window, cv2.WINDOW_NORMAL)
        cv2.imshow(name_window, image)
    
    def Save_PNG (self,image, scale=1.0, dir='filename_dir'):
        W = int(image.shape[1] * scale)
        H = int(image.shape[0] * scale)
        file = cv2.resize(image, (W,H), cv2.INTER_AREA)
        cv2.imwrite(dir+'.png',file)
    
    def Visual_Draw (self,image,Contour_Boxes):
        Draw_Contour = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)

        for cnt in Contour_Boxes.Contours:
            cv2.drawContours(Draw_Contour, cnt, -1, (0, 255, 0), 3)
        
        for P_Box in Contour_Boxes.Points_Box:
            cv2.drawContours(Draw_Contour, [P_Box.astype("int")], -1, (255, 0, 0), 2)
        return Draw_Contour

    def Visual_HistHSV(self,HSV_Hist,Thresh_HSV,Graph_HSV='H',save='',Thresh=False,show=False,norm=[0,255]):
        H, S, V = HSV_Hist
        Thresh_H,Thresh_S,Thresh_V=Thresh_HSV
        if Graph_HSV == 'H':
            cv2.normalize(H, H,norm[0],norm[1], cv2.NORM_MINMAX)
            if Thresh_H==0:
                plt.plot(H, color ='blue')
            else:
                plt.fill(H, color="blue", alpha=0.6)
            if Thresh==True:
                l1=plt.axvline(Thresh_H,ymin=0.05, ymax=0.95, color = 'red')
                plt.text(Thresh_H,0.8*norm[1],str(Thresh_H),fontsize=20,color='r')
            plt.title("Matiz (H)",fontsize=20)
        if Graph_HSV == 'S':
            cv2.normalize(S, S, norm[0],norm[1], cv2.NORM_MINMAX)
            if Thresh_S==0:
                plt.plot(S, color ='blue')
            else:
                plt.fill(S, color="blue", alpha=0.6)
            if Thresh==True:
                l1=plt.axvline(Thresh_S,ymin=0.05, ymax=0.95, color = 'red')
                plt.text(Thresh_S,0.8*norm[1],str(Thresh_S),fontsize=20,color='r')
            plt.title("Saturación (S)",fontsize=20) 
        if Graph_HSV == 'V':
            cv2.normalize(V, V, norm[0],norm[1], cv2.NORM_MINMAX)
            if Thresh_V==0:
                plt.plot(V, color ='blue')
            else:
                plt.fill(V, color="blue", alpha=0.6)
            if Thresh==True:
                l1=plt.axvline(Thresh_V,ymin=0.05, ymax=0.95, color = 'red')
                plt.text(Thresh_V,0.8*norm[1],str(Thresh_V),fontsize=20,color='r')
            plt.title("Brillo (V)",fontsize=20)
        if Thresh==True:
            plt.legend(handles=[l1],labels=['Umbral'],loc='best',fontsize=20) 
        plt.xlabel("Bins",fontsize=20)    
        plt.ylabel("Densidad",fontsize=20)
        
        if save!='':
            plt.savefig(save+'.png')
        if show==True:
            plt.show()

    def Visual_GARG(self,Image,Grasp_Region,Show=[1],label=False):
        '''
            ** Show: Display Parameter
            ***** 0 --> Regions on black backgroundImage  
            ***** 1 --> Grasping Regions by Objects
            ***** 2 --> Contours Objects
            ***** 3 --> Approximate Bounding Rectangle
            ***** 4 --> Labels True
        '''
        font=cv2.FONT_HERSHEY_SIMPLEX
        if 0 in Show:
            Draw_RGrasp = np.zeros((Image.shape[0], Image.shape[1], 3), dtype=np.uint8)
        else:
            Draw_RGrasp=Image

        #### Grasping Regions by Objects
        if 1 in Show:
            for i in range(len(Grasp_Region.Centers_GraspReg)):
                for j in range(len(Grasp_Region.Centers_GraspReg[i])):
                    if Grasp_Region.Centers_GraspReg[i][j] == Grasp_Region.Center_Box[i]:
                        color=[0, 255, 0]
                        if 4 in Show:
                            cv2.putText(Draw_RGrasp,"Pc",(int(Grasp_Region.Centers_GraspReg[i][j][0])+10,int(Grasp_Region.Centers_GraspReg[i][j][1])+10), font, 2,color,5)
                    else:
                        color=[0, 0, 255]
                        if 4 in Show:
                            cv2.putText(Draw_RGrasp,"P "+str(j),(int(Grasp_Region.Centers_GraspReg[i][j][0])+10,int(Grasp_Region.Centers_GraspReg[i][j][1])+10), font, 2,color,5)
                    cv2.drawContours(Draw_RGrasp, [Grasp_Region.Grasp_Regions[i][j].astype("int")], -1, color, 4)
                        
        if 2 in Show:
            for i in range(len(Grasp_Region.Contours)):
                if 0 in Show:
                    color=[255, 255, 255]
                    cv2.drawContours(Draw_RGrasp, Grasp_Region.Contours[i], -1, color, cv2.LINE_8) 
                else: 
                    color=[0, 255, 0]
                    cv2.drawContours(Draw_RGrasp, Grasp_Region.Contours[i], -1, color, cv2.LINE_8)

        if 3 in Show:
            for i in range(len(Grasp_Region.Points_Box)):
                cv2.drawContours(Draw_RGrasp, [Grasp_Region.Points_Box[i].astype("int")], -1, (255, 0, 0), cv2.LINE_8)
                if 4 in Show:
                    cv2.circle(Draw_RGrasp,(int(Grasp_Region.Center_Box[i][0]), int(Grasp_Region.Center_Box[i][1])), 10, (0,0,255), cv2.FILLED)
                    cv2.putText(Draw_RGrasp,"Pc ",(int(Grasp_Region.Center_Box[i][0])+10, int(Grasp_Region.Center_Box[i][1])+10), font, 3,(0,0,255),10)
        return Draw_RGrasp

    def extend_df(self,dataframe):
        with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 5,
                       ):print(dataframe)
