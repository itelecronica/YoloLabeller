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

    def mask_to_polygon(self, mask: np.array, nameMask):

        h,w = mask.shape
        contours ,_= cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        polygons = []
        clases = []
        kernel = np.ones((3,3), np.uint8)
        mask = cv2.erode(mask, kernel)
        i = 0
        if len(contours)==0:
            self.generateWhiteTxt(nameMask)
        for object in contours:
            x, y, width, height = cv2.boundingRect(object)
            #print(x, y, width, height)
            
            is_pellet = False
            
            
            coords = []
            #polygon = []
            nclase = 5
            for point in object:
                coords.append(int(point[0][0]))
                coords.append(int(point[0][1]))
                #coords = [int(point[0][0]),int(point[0][1])]
                #polygon.append(coords)
            
            area = cv2.contourArea(object)
            #print("Area " + str(area))

            if area > 330 and area < 7000 :
                nclase = 0
                limit = 80.0
            elif area >= 7000:
                nclase = 0
                limit = 80.0
            else:
                nclase = 0
                limit = 38.0
            
            
            #img = mask[y:y+height, x: x+width]
            mask_cut = np.zeros_like(mask)
            cv2.drawContours(mask_cut,[object],0,255,-1)
            img_mask = mask_cut[y:y+height, x: x+width]
            is_pellet = self.checkBlack(img_mask,height,width, limit)
            is_pellet = True
            if is_pellet:
                if nclase != 5:
                    #print (coords)
                    self.generateTxtFile(coords,nameMask,h,w, nclase, x, y, width, height, i)
            i +=1
        return polygons, clases
        #return np.array(polygons, dtype='object').tolist()

    def checkBlack(self, img, h, w, limit):

        number_of_black_pix = np.sum(img == 0) 
        '''print(f"Numero de pixeles {number_of_black_pix}")
        print(h,w)'''
        percente_black_px = (float(number_of_black_pix/float(h*w)))*100.0
        #print (f"Porcentaje de px negros {percente_black_px}")
        if percente_black_px < limit:
            return True
        else: return False
        
    def generateWhiteTxt(self, nameImg):
        #nameImg = nameImg.replace("png","txt")
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
        '''path_txt2 = output_path_labels2 + nameImg
        if os.path.isfile(path_txt2):
            try: 
                f2 = open(path_txt2, "a")
            except:
                print("Error abriendo txt")
        else:
            try: 
                f2 = open(path_txt2, "w")
            except:
                print("Error abriendo txt")

        f2.write(str(nClase) + " ")
        x = float(x) + float(width)/2.0
        y = float(y) + float(height)/2.0
        x1, x2 = float(x)/float(w), float(width)/float(w)
        y1, y2 = float(y)/float(h), float(height)/float(h)
        f2.write(str(x1) + " " + str(y1) + " " + str(x2)+ " " + str(y2) + "\n")
        f2.close()'''