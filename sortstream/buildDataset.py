import csv
import os
from sortstream.preprocess import setupTextPreProcess, preprocessText
from sortstream.pdf2txt import pdf2txt
import random


def buildDataset(preprocess = True, filename = "dataset", appPath = ".", minPerClass = 5, maxPerClass = 100, verbose = False, data_folder = None):
    status = ""
    successfulBuildDataset = True
    #Get paths of data folders
    dirs = os.listdir(os.path.join(appPath))
    if not ("data" in dirs): 
        #make data folder and return error
        os.mkdir(os.path.join(appPath, "data"))
        status = "No 'data' folder found,\n please use the folder created"
        successfulBuildDataset = False
        print(status)
        return status, successfulBuildDataset
    
    if data_folder:
        home = os.listdir(data_folder)
    else:
        home = os.listdir(os.path.join(appPath, "data")) #TODO

    catFolders = []
    for item in home:
        if "." in item or item == "env" or item == "__pycache__":
            pass
        else:
            catFolders.append(item)
    
    if verbose:
        print("Data folders found: {0}".format(catFolders))

    if catFolders == []:
        status = "No subfolders found in data,\n please add training data in folders by category"
        successfulBuildDataset = False
        print(status)
        return status, successfulBuildDataset
    elif len(catFolders) <= 1:
        status = "Only 1 category subfolder found in data,\n please add at least 2 categories"
        successfulBuildDataset = False
        print(status)
        return status, successfulBuildDataset

    dataList = [["Category", "Text"]]
    #init preprocessor
    setupTextPreProcess()
    
    for category in catFolders:
        dataPaths = os.listdir(os.path.join(appPath,"data", category))
        random.shuffle(dataPaths)
        cnt = 0
        for path in dataPaths:
            validFile = False
            cnt += 1
            #Check file type
            #PDF
            #TODO add in Word document processing
            if path[-4:] == ".pdf":
                validFile = True
                #GET DATA
                pathToData = os.path.join(appPath, "data", category, path) #TODO
                text = pdf2txt(pathToData)
                if preprocess:
                    #preprocess text
                    text = preprocessText(text)
            
            if validFile and cnt <= maxPerClass:
                #add to storage list
                dataList.append([category, text])
        
        if cnt < minPerClass:
            status = "Please add at least {0} examples per category".format(minPerClass)
            print(status)
            successfulBuildDataset = False
            

    #Shuffle list to make for a better dataset
    random.shuffle(dataList)

    with open(os.path.join(appPath,filename + ".csv"), "w", newline='') as csvfile: #TODO
        writer = csv.writer(csvfile)
        for row in dataList:
            writer.writerow(row)
    
    return status, successfulBuildDataset