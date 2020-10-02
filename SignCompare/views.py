from django.shortcuts import render , redirect
from django.views.decorators.cache import never_cache
from django.conf import settings
import random
import os
from .processing import *

@never_cache
def index(request):

    if request.method == "POST":
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
        return render(request, 'index.html')

@never_cache
def result(request,resultId):
    try:
        resultBaseDir = os.path.join(settings.BASE_DIR,"media",str(resultId))
        matchPercent1,matchPercent2 = 0,0
        imageLoc1,imageLoc2 = "",""

        #Fetch the match percent results from result.txt file
        with open(os.path.join(resultBaseDir,"result.txt"),"r") as file:
            matchPercent1 = file.readline()
            matchPercent2 = file.readline()

        #Get imageLoc1 and imageLoc2 from result direcory
        for filename in os.listdir(resultBaseDir):
            #Look for filename starting with i
            if(filename[0] == "i"):
                if(filename[3] == "1"):
                    imageLoc1 = resultId + "/" + filename  #Input Image1 location
                else:
                    imageLoc2 = resultId + "/" + filename  #Input Image2 location

        return render(request, 'result.html', {"imageLoc1":imageLoc1, "imageLoc2":imageLoc2, "matchPercent1":matchPercent1, "matchPercent2":matchPercent2})
    except:
        return redirect('index')

@never_cache
def errorView(request, exception):
    return render(request,'error.html', {})