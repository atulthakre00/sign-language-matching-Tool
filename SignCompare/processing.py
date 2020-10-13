from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.conf import settings
import random
import cv2 as cv2
import base64
import os

#Generates a random 128 bit hash value
def generateHash():
    hash = random.getrandbits(128)
    return str(hash)

#Write imageObject to imagePath
def writeImage(imageObject,imagePath):
    with open(imagePath, 'wb+') as imageFile:
        for chunk in imageObject.chunks():
            imageFile.write(chunk)

# Returns length of longest common subsequence
def findLcs(list1, list2):
    len1 = len(list1)
    len2 = len(list2)
    lcsStates = [[0 for j in range(len2 + 1)] for i in range(len1 + 1)]

    for i in range(len1):
        for j in range(len2):
            if list1[i] == list2[j]:
                lcsStates[i + 1][j + 1] = lcsStates[i][j] + 1
            else:
                if lcsStates[i][j + 1] >= lcsStates[i + 1][j]:
                    lcsStates[i + 1][j + 1] = lcsStates[i][j + 1]
                else:
                    lcsStates[i + 1][j + 1] = lcsStates[i + 1][j]
    return lcsStates[-1][-1]

#Resizes imageObject read using cv2.imread with minimal distortion and returns resized imageObejct
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

#Takes imageLocation as input and converts it to bmp. returns imageObject
def convertToBmp(filename):
    inputImage = cv2.imread(filename, 0)

    initialWidth = inputImage.shape[1]
    initialHeight = inputImage.shape[0]
    # aspectRatio = initialWidth / initialHeight
    # # newWidth = int(initialWidth/20)
    # newWidth = 30
    # if initialWidth >= 1000:
    #     newWidth = 100
    # elif initialWidth < 1000 and initialWidth > 500:
    #     newWidth = 100
    # elif initialWidth <= 500 and initialWidth > 200:
    #     newWidth = 100
    # elif initialWidth <= 200:
    #     newWidth = 100
    # newHeight = int(newWidth / aspectRatio)
    #
    # dsize = (newWidth, newHeight)
    #inputImage = cv2.resize(inputImage, dsize)
    inputImage = image_resize(inputImage, width=50, height=50, inter=cv2.INTER_AREA)
    inputImage = cv2.cvtColor(inputImage, cv2.COLOR_GRAY2BGR)
    inputImage = cv2.fastNlMeansDenoisingColored(inputImage, None, 10, 10, 7, 15)
    inputImage = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)
    inputImage = cv2.medianBlur(inputImage,5)
    th2 = cv2.adaptiveThreshold(inputImage,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                cv2.THRESH_BINARY,11,2)

    return(th2)

#Takes imageLocation as input and returns a base64 string representing the image
def imageToString(filename):
    with open(filename, 'rb') as binary_file:
        binary_file_data = binary_file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        base64_message = base64_encoded_data.decode('utf-8')
    return(base64_message)


#Takes 2 imageLoc as input and returns matching percents of 2 images
def imageMatching(imageLoc1,imageLoc2,baseDir):
    #imageObjects of input images
    inputImage1 = cv2.imread(imageLoc1,0)
    inputImage2 = cv2.imread(imageLoc2, 0)

    #bmpImageObjects of input images
    bmpImage1 = convertToBmp(imageLoc1)
    bmpImage2 = convertToBmp(imageLoc2)

    #bmpImageLoc of bmpImages
    bmpImageLoc1 = os.path.join(baseDir,"convt1.bmp")
    bmpImageLoc2 = os.path.join(baseDir, "convt2.bmp")

    #Store the bmpImages at bmpImageLoc to use it in next step
    cv2.imwrite(bmpImageLoc1,bmpImage1)
    cv2.imwrite(bmpImageLoc2,bmpImage2)

    #Get the image string from the images at bmpImageLoc
    imageString1 = imageToString(bmpImageLoc1)
    imageString2 = imageToString(bmpImageLoc2)

    #Get the length of image strings
    lengthString1 = len(imageString1)
    lengthString2 = len(imageString2)
    # print("lengthString1:",lengthString1)
    # print("lengthString2:", lengthString2)

    #Find lcs length of imageString1 and imageString2
    lengthLcs = findLcs(imageString1, imageString2)
    # print("lengthLcs:",lengthLcs)

    #Calculate Matching percent with respect to imageString1 and imageString2
    matchWithImage1 = (lengthLcs / lengthString1) * 100
    matchWithImage2 = (lengthLcs / lengthString2) * 100
    # print("{:.2f}".format(matchWithImage1))
    # print("matchWithImage2: {:.2f} %".format(matchWithImage2))

    # Store the result in a text file
    with open(os.path.join(baseDir, "result.txt"),"w") as result:
        result.writelines([str(lengthString1)+"\n", str(lengthString2)+"\n", str(lengthLcs)+"\n", "{:.2f}\n".format(matchWithImage1),"{:.2f}".format(matchWithImage2)])

    # Store the string 1 in a text file
    with open(os.path.join(baseDir, "string1.txt"),"w") as result:
        result.writelines([imageString1])

    # Store the string 2 in a text file
    with open(os.path.join(baseDir, "string2.txt"),"w") as result:
        result.writelines([imageString2])
