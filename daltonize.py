from PIL import Image
import numpy as np
import numpy
import argparse
import sys
import colorsys

#Matrix Multiplication Block (Common for all operations, just varying matrix)
def getImageArray(respectiveArray, editablePhoto, sizeX, sizeY):
	for i in range(0,sizeX):
		for j in range(0,sizeY):
			currMatrix = np.array((0,0,0),dtype=float)
			for k in range(0,3):
				currMatrix[k]=editablePhoto[i,j,k]
			lmsImage = np.dot(respectiveArray,currMatrix)
			for k in range(0,3):
				editablePhoto[i,j,k]=lmsImage[k]
	return editablePhoto

#Converting RGB to LMS
def convertToLMS(im,sizeX,sizeY):
	photo = im.load()
	editablePhoto = np.zeros((sizeX,sizeY,3),'float')
	for i in range(0,sizeX):
		for j in range(0,sizeY):
			for k in range(0,3):
				editablePhoto[i,j,k] = photo[i,j][k]
				editablePhoto[i,j,k] = ((editablePhoto[i,j,k])/255)

	lmsConvert = numpy.array([[17.8824,43.5161,4.11935],[3.45565,27.1554,3.86714],[0.0299566,0.184309,1.46709]])
	editablePhoto = getImageArray(lmsConvert, editablePhoto, sizeX, sizeY)

	NormalPhoto =  normalise(editablePhoto,sizeX,sizeY)
	return NormalPhoto

#Converting LMS to RGB
def convertToRGB(editablePhoto,sizeX,sizeY):
	rgb2lms = numpy.array([[17.8824,43.5161,4.11935],[3.45565,27.1554,3.86714],[0.0299566,0.184309,1.46709]])
	RGBConvert = numpy.linalg.inv(rgb2lms)
	#print(RGBConvert)
	editablePhoto = getImageArray(RGBConvert, editablePhoto, sizeX, sizeY)
	for i in range(0,sizeX):
		for j in range(0,sizeY):
			for k in range(0,3):
				editablePhoto[i,j,k]=((editablePhoto[i,j,k]))*255

	NormalPhoto = normalise(editablePhoto, sizeX, sizeY)
	return NormalPhoto

#Restructuring laterally inverted image
def normalise(editablePhoto,sizeX,sizeY):
	NormalPhoto =  np.zeros((sizeX,sizeY,3),'float')
	x=sizeX-1
	y=sizeY
	for i in range(0,sizeX):
		for j in range(0,sizeY):
			for k in range(0,3):
				NormalPhoto[x,j,k]=editablePhoto[i,j,k]
		x=x-1

	return NormalPhoto

#Simulating for protanopes
def ConvertToProtanopes(editablePhoto,sizeX,sizeY):
	protanopeConvert = numpy.array([[0,2.02344,-2.52581],[0,1,0],[0,0,1]])
	editablePhoto = getImageArray(protanopeConvert, editablePhoto, sizeX, sizeY)
	NormalPhoto = normalise(editablePhoto, sizeX, sizeY)
	return NormalPhoto

#Simulating Deutranopia
def ConvertToDeuteranopes(editablePhoto,sizeX,sizeY):
	DeuteranopesConvert = numpy.array([[1,0,0],[0.494207,0,1.24827],[0,0,1]])
	editablePhoto = getImageArray(DeuteranopesConvert, editablePhoto, sizeX, sizeY)
	NormalPhoto = normalise(editablePhoto, sizeX, sizeY)
	return NormalPhoto

#Simulating Tritanopia
def ConvertToTritanope(editablePhoto,sizeX,sizeY):
	TritanopeConvert = numpy.array([[1,0,0],[0,1,0],[-0.395913,0.801109,0]])
	editablePhoto = getImageArray(TritanopeConvert, editablePhoto, sizeX, sizeY)
	NormalPhoto = normalise(editablePhoto, sizeX, sizeY)
	return NormalPhoto

def arrayToImage(editablePhoto,sizeX,sizeY,saveAs):
	rgbArray = np.zeros((sizeX,sizeY,3),'uint8')
	for i in range(0,sizeX):
		for j in range(0,sizeY):
			for k in range(0,3):
				rgbArray[i,j,k] = editablePhoto[i,j,k]
	img = Image.fromarray(rgbArray)
	img.save(saveAs)

def daltonize(originalRgb, simRgb, sizeX, sizeY):
	photo = originalRgb.load()
	editablePhoto = np.zeros((sizeX,sizeY,3),'float')
	for i in range(0,sizeX):
		for j in range(0,sizeY):
			for k in range(0,3):
				editablePhoto[i,j,k] = photo[i,j][k]

	diffPhoto = simRgb - editablePhoto
	transMatrix = numpy.array([[0, 0, 0], [0.7, 1, 0], [0.7, 0, 1]])
	errCorrection = getImageArray(transMatrix, diffPhoto, sizeX, sizeY)
	finalImage = errCorrection + editablePhoto
	return finalImage

def main():
	#for i in range(1,6):
	#print("Processing Image " + str(i))
	inputIm = Image.open("4.jpg")
	sizeX = inputIm.size[0]
	sizeY = inputIm.size[1]

	
	lmsPhoto = convertToLMS(inputIm,sizeX,sizeY)
	
	simPhoto = ConvertToProtanopes(lmsPhoto,sizeX,sizeY)
	#simPhoto = ConvertToDeuteranopes(lmsPhoto,sizeX,sizeY)
	#simPhoto = ConvertToTritanope(lmsPhoto,sizeX,sizeY)

	rgbPhoto = convertToRGB(simPhoto,sizeX,sizeY)
	#rgbPhoto = daltonize(inputIm,rgbPhoto,sizeX,sizeY)
	arrayToImage(rgbPhoto,sizeX,sizeY,"outImage_RG" + str(4) + ".jpg")

if __name__ == '__main__':
	main()