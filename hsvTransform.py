def correct(inputIm, sizeX,sizeY,saveAs):

	photo = inputIm.load()
	editablePhoto = np.zeros((sizeX,sizeY,3),'float')
	hsvArray=np.zeros((sizeX,sizeY,3),'float')
				
	for i in range(0,sizeX):
		for j in range(0,sizeY):
			for k in range(0,3):
				editablePhoto[i,j,k] = photo[i,j][k]
				editablePhoto[i,j,k] = ((editablePhoto[i,j,k])/255)
			rNew=editablePhoto[i,j,0]
			gNew=editablePhoto[i,j,1]
			bNew=editablePhoto[i,j,2]

			tempArray=np.zeros((3),'float')

			for k in range(0,3):
				hsvArray[i,j,k]=colorsys.rgb_to_hsv(editablePhoto[i,j,0],editablePhoto[i,j,1],editablePhoto[i,j,2])[k]

			
			greenRatio = (hsvArray[i,j,0] - (60/360))/gNew
			blueRange = greenRatio*bNew
			hsvArray[i,j,0] = 0.5 + blueRange

			tempArray=np.zeros((3),'float')
			for k in range(0,3):
				tempArray[k]=hsvArray[i,j,k]
			tempArray.tolist()
			tempArray = (colorsys.hsv_to_rgb(tempArray[0],tempArray[1],tempArray[2]))

			for k in range(0,3):
				editablePhoto[i,j, k] = tempArray[k]*255

	NormalPhoto = normalise(editablePhoto, sizeX, sizeY)
	arrayToImage(NormalPhoto,sizeX,sizeY,saveAs)


inputIm = Image.open(user_choice.input)
sizeX = inputIm.size[0]
sizeY = inputIm.size[1]
correct(inputIm,sizeX,sizeY,"outImg.4")