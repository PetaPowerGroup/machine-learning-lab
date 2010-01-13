import re
import os.path
import subprocess
from ID3 import *
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="kermit"
__date__ ="$2009.12.15 19:16:02$"

import os
#from os import listdir

supportedExtensions=[]
supportedGenres=[]
folderLocation=""
classificationTestMethod=""
outputFileName=""
callSonicAnnotator=0
sonicAnnotatorCommand=""
scaleCommand=""
classifier=""
libsvmTrainCommand=""
# kreshvmTrainCommand=""
kreshvmParameterC=1
kreshvmParameterType=2
kreshvmParameterThird=3
kreshvmTestCommand=""
dataDivisionCommand=""


def check_extension(pathToFile):
    #416uroprint "extension is " + os.path.splitext(pathToFile)[1]
    if os.path.splitext(pathToFile)[1] in supportedExtensions:
        #print "file format supported"
        return 1
    else:
        #print "file format not supported, skipping"
        return 0

def exists_in_supported_genres(targetGenre):
    print "Here"
    print supportedGenres
    foundSuitableMatch=0
    for genre in supportedGenres:
        print "Checking " + genre
        p=re.compile(".*"+genre+".*", re.IGNORECASE)
        if p.match(targetGenre):
            foundSuitableMatch=1
            break
    return foundSuitableMatch

def remove_extension(fileName):
    #print "Vracam " + os.path.splitext(fileName)[0]
    return os.path.splitext(fileName)[0]

def calculate_number_of_features(filename):
    maxFeatures=0
    featuresFile=open(filename, "r")
    featuresString=featuresFile.readline()
    print featuresString
    while featuresString:
        listOfFeatures=featuresString.split(" ")
        if len(listOfFeatures)>maxFeatures:
            maxFeatures=len(listOfFeatures)
        featuresString=featuresFile.readline()
    featuresFile.close()
    return maxFeatures-2
#
# -----------------------------------------------------------------------------------------
#
# From id3 tag
#

def set_class_from_id3(folderLocation, fileName, outputFile):
    pathToFile=os.path.join(folderLocation, fileName)
    print "Processing file " + pathToFile
    if check_extension(pathToFile):
        print "actual work"
        #targetGenre=""
        try:
	  id3info = ID3(pathToFile)
          print "genre in ID3: " + id3info['GENRE']
          foundSuitableMatch=0
          for genre in supportedGenres:
            p=re.compile(".*"+genre+".*", re.IGNORECASE)
            if p.match(id3info['GENRE']):
                #targetGenre=id3info['GENRE']
                outputFile.write(remove_extension(fileName)+">>"+str(supportedGenres.index(genre)+1)+"\n")
                foundSuitableMatch=1
                break
        except InvalidTagError, message:
          print "Invalid ID3 tag:", message
        if not foundSuitableMatch:
            print "COULDN'T DECIDE ON GENRE: " + id3info['GENRE']

def recursively_determine_class_from_id3(folderLocation, outputFile):
#    if folderLocation.find("\n")>0:
#        folderLocation=folderLocation[0:len(folderLocation)-1]
    print "Searching folder "+ folderLocation
    for fileName in os.listdir(folderLocation):
        print "\n" + fileName + "\n";
        newPath=os.path.join(folderLocation, fileName)
        if os.path.isfile(newPath):
            set_class_from_id3(folderLocation, fileName, outputFile)
        if os.path.isdir(newPath):
            recursively_determine_class_from_id3(newPath, outputFile)
#        else:
#            print "NE ULAZIM U " + newPath

#
# -----------------------------------------------------------------------------------------
#
# From folder name
#

def recursively_set_class(classID, folderLocation, outputFile):
    print "Searching folder "+ folderLocation
    for fileName in os.listdir(folderLocation):
        print "\n" + fileName + "\n";
        newPath=os.path.join(folderLocation, fileName)
        if os.path.isfile(newPath) and check_extension(newPath):
            outputFile.write(remove_extension(fileName)+">>"+str(classID)+"\n")
        if os.path.isdir(newPath):
            recursively_set_class(classID, newPath, outputFile)

def determine_class_from_folder_name(folderLocation, outputFile):
    classID=1
    for fileName in os.listdir(folderLocation):
        newPath=os.path.join(folderLocation, fileName)
        if os.path.isdir(newPath):
            print "genre from folder name is " + fileName
            if (exists_in_supported_genres(fileName)):
                print "uzimam folder u obzir"
                recursively_set_class(classID, newPath, outputFile)
            classID=classID+1


#
# ------------------------------------------
#
# main - reading from conf file
#
def remove_newline_from_strings(targetList):
    newList=[]
    for element in targetList:
        #print "element is " + element
        if element.find("\n")>0:
            newList.append(element.split("\n")[0])
        else:
            newList.append(element)
    return newList

def remove_comments_and_newlines_from(targetList):
    newList=[]
    comment=re.compile("#.*")
    empty=re.compile("\n")
    for element in targetList:
        #print "element is " + element
        if not (comment.match(element) or empty.match(element)):
            newList.append(element)
    return newList

def read_from_conf_file():
    configFile=open('conf-file.txt', 'r')
    configLines = configFile.readlines()
    configLines=remove_newline_from_strings(configLines)
    configLines=remove_comments_and_newlines_from(configLines)

    globals()["folderLocation"]=configLines[0]
    print "Folder location is " + folderLocation

    globals()["supportedExtensions"]=configLines[1].split(" ")
    print "supported extensions:" + str(supportedExtensions)

    globals()["supportedGenres"]=configLines[2].split(",")
    print "supported genres:" + str(supportedGenres)

    globals()["outputFileName"]=configLines[3]
    print "opening file " + outputFileName

    globals()["classificationTestMethod"]=configLines[4]
    print "class determination mehod is: " + classificationTestMethod
    configFile.close()

    globals()["callSonicAnnotator"]=int(configLines[5])
    print "Call sonic annotator: " + str(globals()["callSonicAnnotator"])

    globals()["sonicAnnotatorCommand"]=configLines[6]

    globals()["scaleCommand"]=configLines[7]

    globals()["classifier"]=configLines[8]

    globals()["libsvmTrainCommand"]=configLines[9]

    # globals()["kreshvmTrainCommand"]=configLines[10]

    globals()["kreshvmParameterC"]=float(configLines[10])

    globals()["kreshvmParameterType"]=float(configLines[11])

    globals()["kreshvmParameterThird"]=float(configLines[12])

    globals()["kreshvmTestCommand"]=configLines[13]

    globals()["dataDivisionCommand"]=configLines[14]

if __name__ == "__main__":
    read_from_conf_file()

    
    if callSonicAnnotator==1:
        # extract actual songs' genres and write them to file
        outputFile=open(outputFileName, "w")
        print classificationTestMethod
        if classificationTestMethod=="folder":
            determine_class_from_folder_name(folderLocation, outputFile)
        else:
            if classificationTestMethod=="id3":
                recursively_determine_class_from_id3(folderLocation, outputFile)
        outputFile.close()

        # extract features
        print "calling sonic annotator to extract features..."
        #print os.path.join(os.getcwd(),sonicAnnotatorCommand + " " + folderLocation)
        #subprocess.call(os.path.join(os.getcwd(),sonicAnnotatorCommand + " " + folderLocation), shell=True)
        print "command: "+ sonicAnnotatorCommand
        subprocess.call(sonicAnnotatorCommand + " " + folderLocation, shell=True)
    else:
        print "will try to use existing features..."
        # copy existing features from last_session to root

    # format file
    print "uzorci.exe\nformating file..."
    subprocess.call("uzorci.exe", shell=True)
    # empty last_session
    # copy all .csv files and uzorci_razred.txt from root to last_session

    # calling the classifier
    if classifier=="libsvm":
        # using libsvm classifier
        # scale data
        print "command: "+ scaleCommand+"\nscaling data..."
        subprocess.call(scaleCommand + " skup_svih_znacajki.txt > skaliran_skup_svih_znacajki.txt", shell=True)
        # train and validate classifier
        print "command: "+ libsvmTrainCommand+"\ntraining and validating..."
        subprocess.call(libsvmTrainCommand + " skaliran_skup_svih_znacajki.txt", shell=True)

    elif classifier=="kreshvm":
        # using our classifier "kreshvm"
        # divide data
        subprocess.call(dataDivisionCommand, shell=True)

        # scale training data
        subprocess.call(scaleCommand + " skup_za_ucenje.txt > skaliran_skup_za_ucenje.txt", shell=True)
        subprocess.call("del skup_za_ucenje.txt", shell=True)
        subprocess.call("rename skaliran_skup_za_ucenje.txt skup_za_ucenje.txt", shell=True)
        #rename("skaliran_skup_za_ucenje.txt", "skup_za_ucenje.txt")

        # scale testing data
        subprocess.call(scaleCommand + " skup_za_testiranje.txt > skaliran_skup_za_testiranje.txt", shell=True)
        subprocess.call("del skup_za_testiranje.txt", shell=True)
        subprocess.call("rename skaliran_skup_za_testiranje.txt skup_za_testiranje.txt", shell=True)
        #rename("skaliran_skup_za_testiranje.txt", "skup_za_testiranje.txt")

        # train the svm
        numberOfFeatures=calculate_number_of_features("skup_svih_znacajki.txt")
        kreshvmTrainCommand="kreshvm_train.exe " + str(numberOfFeatures) + " " + str(kreshvmParameterC) + " " + str(kreshvmParameterType)
        if not kreshvmParameterType==1:
            kreshvmTrainCommand= kreshvmTrainCommand + " " + str(kreshvmParameterThird)
        print "command: "+ kreshvmTrainCommand +"\ntraining kreshvm..."
        subprocess.call(kreshvmTrainCommand, shell=True)

        # test the efficiency of the svm
        print "command: "+ kreshvmTestCommand+"\ntesting kreshvm..."
        subprocess.call(kreshvmTestCommand, shell=True)

        # delete unneccesary files
        
