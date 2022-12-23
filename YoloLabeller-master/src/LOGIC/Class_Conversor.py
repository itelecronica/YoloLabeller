'''
Created on 20 jun. 2022

@author: Pablo
@comment: Conversor de mascaras a poligonos para generar TXT en formato de segmentacion YOLO
'''
import cv2, os

import numpy as np

class ConversorMasks:
    def __init__(self):
        return

    # funcion encargada de convertir la mascara en contornos y escribe el txt formato YOLO para segmentacion 
    def mask_to_polygon(self, mask: np.array, nameMask):

        h,w = mask.shape
        contours ,_= cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        polygons = []
        clases = []
        kernel = np.ones((3,3), np.uint8)
        mask = cv2.erode(mask, kernel)
        i = 0
        if len(contours)==0:
            self.generateWhiteTxt(nameMask) # Si mascara vacia, se genera un txt vacio
        for object in contours:
            x, y, width, height = cv2.boundingRect(object)
            is_pellet = False
            coords = []
            nclase = 5
            for point in object:
                coords.append(int(point[0][0]))
                coords.append(int(point[0][1]))
                
            area = cv2.contourArea(object)
            # en caso pellets, se decide por area de contorno a que clase pertenece cada uno
            if area > 330 and area < 7000 :
                nclase = 0
                limit = 80.0
            elif area >= 7000:
                nclase = 0
                limit = 80.0
            else:
                nclase = 0
                limit = 38.0
            
            mask_cut = np.zeros_like(mask)
            cv2.drawContours(mask_cut,[object],0,255,-1)
            img_mask = mask_cut[y:y+height, x: x+width]
            is_pellet = self.checkBlack(img_mask,height,width, limit)
            is_pellet = True
            if is_pellet:
                if nclase != 5:
                    self.generateTxtFile(coords,nameMask,h,w, nclase, x, y, width, height, i) # generacion de txt en formato Segmentation YOLO
            i +=1
        return polygons, clases


    def checkBlack(self, img, h, w, limit):

        number_of_black_pix = np.sum(img == 0) 
        
        percente_black_px = (float(number_of_black_pix/float(h*w)))*100.0
        #print (f"Porcentaje de px negros {percente_black_px}")
        if percente_black_px < limit:
            return True
        else: return False
        
    # generacion de TXT en blanco para mascaras sin contornos definidos    
    def generateWhiteTxt(self, nameImg):
        path_txt = nameImg.replace("png","txt")
        if os.path.isfile(path_txt):
            try: 
                f = open(path_txt, "w")
            except:
                print("Error abriendo txt")
        else:
            try: 
                f = open(path_txt, "w")
            except:
                print("Error abriendo txt")
        f.write(" ")
        f.close()

    # generacion de txt en formato Segmentation YOLO
    def generateTxtFile(self, points, nameImg, h, w, nClase, x, y, width, height, i):
        nameImg = nameImg.replace("png","txt")
        path_txt =  nameImg
        if os.path.isfile(path_txt):
            try:
                if i == 0:
                    f = open(path_txt, "w")
                else:
                    f = open(path_txt, "a")
            except:
                print("Error abriendo txt")
        else:
            try: 
                if i == 0:
                    f = open(path_txt, "w")
                else:
                    f = open(path_txt, "a")
            except:
                print("Error abriendo txt")

        f.write(str(nClase) + " ")
        for i in range(len(points)):
            if i%2 == 0:
                point_absolute = float(points[i])/float(w)
            else:
                point_absolute = float(points[i])/float(h)
            f.write(str(point_absolute) + " ")
        f.write("\n")
        f.close()
        
        