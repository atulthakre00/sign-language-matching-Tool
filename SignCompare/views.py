from django.shortcuts import render , redirect
from django.views.decorators.cache import never_cache
from django.conf import settings
import random
import os
from .processing import *

@never_cache
def index(request):
    print("c1")
    if request.method == "POST":
        print("c2")
        currentProcessName = generateHash()  # Create a random name for current process directory using hash
        currentProcessDir = os.path.join(settings.BASE_DIR, "media",currentProcessName)  # get absolute path for current process directory
        os.mkdir(currentProcessDir)  # create directory for current process

        #Taking image objects from user uploaded images
        uploadedImage1 = request.FILES['imageFile1']
        uploadedImage2 = request.FILES['imageFile2']

        #Finding the extensions of the uploaded images
        imageExtension1 = os.path.splitext(uploadedImage1.name)[1]
        imageExtension2 = os.path.splitext(uploadedImage2.name)[1]

        #Path where the uploaded images will be saved
        imageLoc1 = os.path.join(currentProcessDir,"inp1"+imageExtension1)
        imageLoc2 = os.path.join(currentProcessDir, "inp2" + imageExtension2)

        #Write uploaded image in current process directory
        writeImage(uploadedImage1, imageLoc1)
        writeImage(uploadedImage2, imageLoc2)

        imageMatching(imageLoc1,imageLoc2,currentProcessDir)

        return redirect('result', currentProcessName)
    else:
        print("c6")
        return render(request, 'index.html')

@never_cache
def result(request,resultId):
    try:
        resultBaseDir = os.path.join(settings.BASE_DIR,"media",str(resultId))
        string1Length,string2Length,lcsLength = 0,0,0
        matchPercent1,matchPercent2 = 0,0
        imageLoc1,imageLoc2 = "",""
        convtImageLoc1,convtImageLoc2 = "",""
        imageString1,imageString2 = "",""

        #Fetch the match percent results from result.txt file
        with open(os.path.join(resultBaseDir,"result.txt"),"r") as file:
            string1Length = file.readline()
            string2Length = file.readline()
            lcsLength = file.readline()
            matchPercent1 = file.readline()
            matchPercent2 = file.readline()

        #Fetch the image string 1 from string1.txt file
        with open(os.path.join(resultBaseDir,"string1.txt")) as file:
            imageString1 = file.readline()

        # Fetch the image string 2 from string1.txt file
        with open(os.path.join(resultBaseDir,"string2.txt")) as file:
            imageString2 = file.readline()

        #Get imageLoc1 and imageLoc2 from result direcory
        for filename in os.listdir(resultBaseDir):
            #Look for filename starting with i
            if(filename[0] == "i"):
                if(filename[3] == "1"):
                    imageLoc1 = resultId + "/" + filename  #Input Image1 location
                else:
                    imageLoc2 = resultId + "/" + filename  #Input Image2 location
            elif(filename[0] == "c"):
                if (filename[5] == "1"):
                    convtImageLoc1 = resultId + "/" + filename  # Converted Image1 location
                else:
                    convtImageLoc2 = resultId + "/" + filename  # converted Image2 location

        return render(request, 'result.html', {"imageString2":imageString2, "imageString1":imageString1, "lcsLength":lcsLength, "string1Length":string1Length, "string2Length":string2Length , "convtImageLoc1":convtImageLoc1, "convtImageLoc2":convtImageLoc2, "imageLoc1":imageLoc1, "imageLoc2":imageLoc2, "matchPercent1":matchPercent1, "matchPercent2":matchPercent2})
    except:
        return redirect('index')

@never_cache
def errorView(request, exception):
    return render(request,'error.html', {})
