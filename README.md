# Sign Language Matching Tool

### processing.py
This file contains functions for actual image processing that is applying image matching algorithm.

### generateHash()
It creates a 128 bit hash value which is used as name of present working directory for individual task of image matching.
The hash value is used to ensure that results of previously processed image can be checked in future without recalculating it.

### writeImage(imageObject,imagePath)
This function takes imageObject (obtained using cv2.imread method) and complete path where the image is to be stored.
It stores image irrespective of the extension of image. However the extension must be a part of imagePath string.

### findLcs(str1,str2)
It takes 2 strings as input and uses Dynamic Programming approach to return the length of LCS of 2 strings.
It runs in space and time complexity of order N^2.

### image_resize(image,width,height,inter)
It resizes image to the width and height given as input. 
It does not resize to exact width and heigh dimensions, rather it chooses dimensions closer to width and height,
for which distortion of image is minimum possible. 
Image is the object obtained using open-cv cv2.imread method.
inter is method used for resizing. By default cv2.INTER_AREA algorithm is used

### convertToBmp(filename)
Takes location of file as input. First it resizes the image to a lower dimension using image_resize() funcion. 
Denoising of the image is done using fastNlMeansDenoisingColored() method of open-cv library. It removes any pixelation or distortion present in the image.
Adaptive threshold converts it into a bmp matrix by automatically selecting a threshold value. 
Colors above a particular threshold intensity are colored as high bit value and others below the threshold are colored white.
It returns BMP image object.

### imageToString(filename)
It takes image location of the bmp image made earlier using convertToBmp() and then using base64 library in python converts it into a base 64 string. 
It returns a string.

### imageMatching(imageLoc1,imageLoc2,baseDir)
It takes both the image location and base working directory as input and performs all the above operations one after the other to calculate the matching percent
of the image.
