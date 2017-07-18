import cv2
from PIL import Image
import numpy as np



def arrayToImage(img,sizeX,sizeY,saveAs):
    rgbArray = np.zeros((sizeX,sizeY,3),'uint8')
    for i in range(0,sizeX):
        for j in range(0,sizeY):
            for k in range(0,3):
                rgbArray[i,j,k] = img[i,j,k] * 255
    img = Image.fromarray(rgbArray)
    img.save(saveAs)

im = Image.open("inImage.jpg")
sizeX = im.size[0]
sizeY = im.size[1]
photo = im.load()
img = np.zeros((sizeX,sizeY,3),'float')
for i in range(0,sizeX):
    for j in range(0,sizeY):
        for k in range(0,3):
            img[i,j,k] = photo[i,j][k]
            img[i,j,k] = ((img[i,j,k])/255)

factor = 0.4
for i in range(0, sizeX):
    for j in range(0,sizeY):
        img[i,j,0] = ((1 - img[i,j,0]) * factor) + img[i,j,0]
        img[i,j,1] = ((1 - img[i,j,1]) * factor) + img[i,j,1]

        # Change in blue can be recctified for sure!
        if img[i,j,0] > img[i,j,1] :
            img[i,j,2] = img[i,j,2] - (img[i,j,2] * factor)
        else:
            img[i,j,2] = ((1 - img[i,j,2]) * factor) + img[i,j,2]

arrayToImage(img, sizeX, sizeY, "outImage6.jpg")


'''
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''