'''
This file houses the workflow funcions and UI to call these functions.
Key workflows:
1) BuildModelFromData: Transform a dataset of files into a trained model in one step.
2) BuildDatasetOnly: Transfrom structured files into a csv dataset, but dont train any model.
3) TrainModelOnly: Given a transfromed dataset exists from 1) or 2), train a model on this dataset.
4) PredictClasses: Given a 'data' folder, predict the classes of the files in 'data' and move into their own 
folders by class. If class folders do not exist, create these first.
5) PredictAPI: Given a 'data' folder, predict the classes of the files in 'data' and move into their own 
folders by class. If class folders do not exist, create these first. This should be callable without activating the GUI.


Structure:
PROGRAMFILE

data
    X1.pdf
    X2.pdf
    ...
builtDataset.csv

models
    Logit
    vectorizerX

predictions
    Class 1
        X1.pdf
        ...
    Class 2
        X2.pdf
        ...
    ...

UI:
__________________________________________________________
NAME OF PROGRAM                  Process Monitor
[Instruction Manual]             (Process text)
[Licencing]         

[PREDICT]
[Train a new classifier]                
[Build a dataset]
[Train a model from an existing dataset]    
                                            [QUIT]
__________________________________________________________       

To create an application, PyInstaller is used on a monolithic script
Call:
    pyinstaller --onefile --windowed workflow.py
        Mac uses .icns icon files while windows uses .ico
    pyinstaller --onefile --windowed --hidden-import="sklearn.utils._cython_blas" --icon=chrome.icns --name="SortStream" workflow.py
    pyinstaller --onefile --windowed --icon=SSIconBeta.icns --name="SortStream" workflow.py
    https://pyinstaller.readthedocs.io/en/stable/operating-mode.html#bundling-to-one-file 
'''

#import programs
from model import createAndTrainModel, loadModel, getPredictions
from buildDataset import buildDataset
from loadFiles import loadFile
from predict import FindAndLoadModel, getTargetFileDirs
from log import saveLogs
from checkLicence import *
#import packages
import numpy as np
import os, sys
import tkinter as tk
from datetime import datetime
import csv
#Hidden Imports
# import sklearn.utils._cython_blas
# import scipy.special.cython_special
# import pkg_resources.py2_warn

def defaultButton(self, text, command):
    ''' 
    Grant Holtes 10/5/20
    Structured default format button
    inputs: self, text (str), command in the form self.FUNCTION
    outputs: a tk button
    '''
    return tk.Button(self, text = text, command = command,
    background = "black",
    borderwidth = 4)

def YYYYMMDDHMS():
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def GetAppPath():
    if getattr(sys, 'frozen', False):
        applicationPath = os.path.abspath(os.path.dirname(sys.executable))
        #except for mac os:
        if "MacOS" in applicationPath:
            appPathList = splitall(applicationPath)
            newPath = ""
            for i in range(len(appPathList)-3):
                newPath = os.path.join(newPath, appPathList[i])
            applicationPath = newPath
    elif __file__:
        applicationPath = os.path.abspath(os.path.dirname(__file__))
    return applicationPath

def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts

class DocumentClassifierApp(tk.Frame):
    def __init__(self, master=None, globalPrivateKey=0):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createUI()
        self.name = "SortStream"
        #detect if the script is being run as a script or a frozen exe. Get the absoute path 
        self.applicationPath = GetAppPath()
        self.confidenceValue = 75
        self.privateKey = globalPrivateKey
        

    #__________________________________GUI_FUNCTIONS______________________________________
    def createUI(self):
        #Text items
        self.AppName = tk.Label(self, text = "Document Classification System")
        self.AppName.grid(row = 1, column = 1, sticky=tk.W+tk.N, padx = 20, pady=10)

        self.Licence = tk.Label(self, text = "Licence: XYZ Ltd, 2020")
        self.Licence.grid(row = 2, column = 1, sticky=tk.W, padx = 20)

        self.statusValue = tk.StringVar() #init status
        self.statusValue.set("-")
        self.status = tk.Label(self, textvariable = self.statusValue)
        self.status.grid(row = 3, column = 1, sticky=tk.W, padx = 20)
        #0) General Info
        self.INSTRUCTIONS_Button = tk.Button(self, 
                                                    text = "Instructions",
                                                    command = self.OpenInstructions,
                                                    width=10)
        self.INSTRUCTIONS_Button.grid(row=1, column=2, sticky=tk.E, padx = 20)
        #4) PREDICT
        self.PREDICT_Button = tk.Button(self, 
                                                    text = "Predict Classes",
                                                    command = self.PredictClasses,
                                                    width=26)
        self.PREDICT_Button.grid(row=5, column=1, sticky=tk.W, padx = 20)
        #4.2 Predict Confidence 
        self.confidence = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL)
        self.confidence.set(75)
        self.confidence.grid(row=5, column=2, sticky=tk.W, padx = 20)

        self.confidenceLab = tk.Label(self, text = "Confidence (%)")
        self.confidenceLab.grid(row = 4, column = 2, sticky=tk.W, padx = 20)
        #1) BuildModelFromData
        self.BuildModelFromData_Button = tk.Button(self, 
                                                    text = "Build Model from Data",
                                                    command = self.BuildModelFromData,
                                                    width=26)
        self.BuildModelFromData_Button.grid(row=6, column=1, sticky=tk.W, padx = 20)
        #Quit
        self.quit = tk.Button(self, text="Quit", fg="red",
                              command=self.QuitPressed,
                              width=10)
        self.quit.grid(row=6, column=2, sticky=tk.E, padx = 20)
    #_________________________________WORKFLOW_FUNCTIONS_________________________________
    def OpenInstructions(self):
        print("OpenInstructions_Button PRESSED")
        print(self.applicationPath)
        self.statusValue.set("Current application path:{0}".format(self.applicationPath))
        return True

    def BuildModelFromData(self):
        print("BuildModelFromData_Button PRESSED")
        timestamp = YYYYMMDDHMS() #get unique timestamp
        
        #Build dataset
        print("Building dataset")
        self.statusValue.set("Building dataset...")

        filename = self.name+"builtDataset_"+timestamp
        buildDatasetSatatus, successfulBuildDataset = buildDataset(preprocess = True, filename = filename, appPath = self.applicationPath)
        datasetLoc = os.path.join(self.applicationPath, filename+".csv")

        if successfulBuildDataset:
            #load dataset
            print("Loading dataset")
            self.statusValue.set("Loading dataset...")

            loadedDataset = []
            with open(datasetLoc, "r") as csvfile: #TODO
                reader = csv.reader(csvfile)
                for row in reader:
                    loadedDataset.append(row)
            loadedDataset = np.array(loadedDataset[1:])
            
            #train model
            #ensure that new model folder is present
            print("Training model")
            self.statusValue.set("Training Model...")

            #Concat strings to make model name
            modelLocation = self.name + "model" + timestamp
            os.mkdir(os.path.join(self.applicationPath, modelLocation))
            #call model
            createAndTrainModel(loadedDataset[:,1],
                            loadedDataset[:,0].reshape(-1, 1), 
                            loadedDataset[:50,1],
                            loadedDataset[:50,0].reshape(-1, 1),
                            saveloc = modelLocation, 
                            maxFeatures = 2000, 
                            batchSize = 15,
                            epochsTrain = 50,
                            appPath = self.applicationPath)
            os.remove(datasetLoc)
            print("Done")
            self.statusValue.set("Done")
        else:
            #Something is wrong with the dataset build
            self.statusValue.set(buildDatasetSatatus)
            try:
                os.remove(datasetLoc)
            except FileNotFoundError:
                print("Failed to remove dataset")
        return True

    def PredictClasses(self, processingBatchSize = 5, threshold = 0.7):
        print("PredictClasses_Button PRESSED")
        self.confidenceValue = self.confidence.get()
        #1) find model directory and files:
	    #2) Load model and status
        model, classes, status = FindAndLoadModel(self.name, self.applicationPath)
        self.statusValue.set(status)        
        
        #3 get unprocessed files
        targetFiles = getTargetFileDirs(acceptedFileTypes = [".pdf"], appPath = self.applicationPath)
        #catch case where there are no files
        if len(targetFiles) == 0:
            self.statusValue.set("Please add files to the input_files_to_be_sorted folder")  
        
        #Prepare for Logging, add header row
        logArray = [["filename", "classification", "confidence", "errors"]]
        # for class_ in classes[1:-1]: logArray[0].append("probability of class: " + str(class_)) #Exclude 'not classified'
        for class_ in classes: 
            if class_ != 'NotClassified': logArray[0].append("probability of class: " + str(class_)) #Exclude 'not classified'

        #Batch Up The files for effeciency:
        for i in range(0,len(targetFiles), processingBatchSize):
            textList, fileList = [], []
            for batch_i in range(processingBatchSize):
                try:
                    #get file locacton:
                    targetFile = targetFiles[i+batch_i]
                    #load file:
                    fileList.append(targetFile)
                    textList.append(loadFile(targetFile))
                except IndexError:
                    pass
            #get predictions
            predictionsLabel, predictionsProbabilities = getPredictions(textList, model)
            #move files to destinations based on predicions
            for i in range(len(fileList)):
                predictionsLabel_i, predictionsProbabilities_i, file_i = predictionsLabel[i], predictionsProbabilities[i], fileList[i]
                #Todo set min threshold predictionsProbability_i for sorting. set based on model metrics
                predictionsProbabilities_i = predictionsProbabilities_i.tolist()
                print(predictionsLabel_i, predictionsProbabilities_i, file_i)
                predictionsProbability = max(predictionsProbabilities_i)
                #Get file name
                fileNameOnly = os.path.split(file_i)[1]

                #Get threshold
                threshold = self.confidenceValue / 100
                #Move file to destination folder
                if predictionsProbability >= threshold:
                    newFileName = predictionsLabel_i + "_" + YYYYMMDDHMS() + "_" + fileNameOnly
                    os.replace(file_i, os.path.join(self.applicationPath, "predictions", predictionsLabel_i, newFileName)) #TODO
                    #Append logging file
                    fileLog = [newFileName, predictionsLabel_i, predictionsProbability, "No errors"]
                    # for prob in predictionsProbabilities_i[1:]: fileLog.append(prob) #TODO
                    for prob in predictionsProbabilities_i: fileLog.append(prob)
                    logArray.append(fileLog)
                else:
                    print("File not classified as prediction probability of {1}% was below threshold: {0}".format(file_i, 100*round(predictionsProbability, 3)))
                    os.replace(file_i, os.path.join(self.applicationPath,"predictions", "NotClassified", fileNameOnly))
                    #Append logging file
                    fileLog = [fileNameOnly, "NotClassified", predictionsProbability, "confidence below threshold, no classification"]
                    # for prob in predictionsProbabilities_i[1:]: fileLog.append(prob)
                    for prob in predictionsProbabilities_i: fileLog.append(prob)
                    logArray.append(fileLog)
        
        #Save logs for this prediction run
        saveLogs(logArray, appPath = self.applicationPath)
        return True

    def PredictAPI():
        return True

    def QuitPressed(self):
        print("quit_Button PRESSED")
        #quit the program with master.destroy()
        self.master.destroy()

class Licencing(tk.Frame):
    def __init__(self, master=None, globalPrivateKey=0):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createUI()
        self.name = "SortStream"
        #detect if the script is being run as a script or a frozen exe. Get the absoute path 
        self.applicationPath = GetAppPath()
        self.confidenceValue = 75
        self.privateKey = globalPrivateKey
        

    #__________________________________GUI_FUNCTIONS______________________________________
    def createUI(self):
        #Text items
        self.AppName = tk.Label(self, text = "SortStream")
        self.AppName.grid(row = 1, column = 1, sticky=tk.W+tk.N, padx = 20, pady=10)

        self.Licence = tk.Label(self, text = "Licence: XYZ Ltd, 2020")
        self.Licence.grid(row = 2, column = 1, sticky=tk.W, padx = 20)

        self.info = tk.Label(self, text = "Please enter a valid product code below:")
        self.info.grid(row = 3, column = 1, sticky=tk.W, padx = 20)

        self.statusValue = tk.StringVar() #init status
        self.statusValue.set("-")
        self.status = tk.Label(self, textvariable = self.statusValue)
        self.status.grid(row = 4, column = 1, sticky=tk.W, padx = 20)

        #1) Product Key
        self.prodKey = tk.Entry(self)
        self.prodKey.grid(row=5, column=1, sticky=tk.W, padx = 20)

        #2) submit
        self.submit = tk.Button(self, 
                                text = "Enter",
                                command = self.checkProductKey,
                                width = 10)
        self.submit.grid(row=6, column=2, sticky=tk.W, padx = 20)
        
        #Quit
        self.quit = tk.Button(self, text="Quit", fg="red",
                              command=self.QuitPressed,
                              width=10)
        self.quit.grid(row=7, column=2, sticky=tk.E, padx = 20)
    #_________________________________WORKFLOW_FUNCTIONS_________________________________
 
    def QuitPressed(self):
        print("quit_Button PRESSED")
        #quit the program with master.destroy()
        self.master.destroy()
    
    def checkProductKey(self):
        print("checkProductKey PRESSED")
        productKeyUser = self.prodKey.get()
        print("Product key entered: {0}".format(productKeyUser))
        #3) check product key
        validProductKey, returnMessage = checkProductKey(productKey = productKeyUser)
        self.statusValue.set(returnMessage)
        #4) write licence file if key is valid
        if validProductKey:
            writeLicenceFile(licenceFilename = "sortstream.licence", 
                        X = self.privateKey, 
                        productKey = productKeyUser, 
                        appPath = self.applicationPath)
        return True

#MAIN
print(tk.TkVersion)
#1) Check licence
applicationPath = GetAppPath()
globalPrivateKey = 1234
validLicence = AuthenticateLicence(appPath = applicationPath, licenceFilename = "sortstream.licence", X = globalPrivateKey)
# validLicence = False
if validLicence:
    #1.1) run main
    root = tk.Tk()
    root.title("SortStream")
    #set size constraits
    root.geometry("650x210") #set default size
    root.minsize(500, 160) #set min size
    app = DocumentClassifierApp(master=root)
    app.update()
    app.mainloop()
else:
    #2) ask for product key
    #3) check product key
    #4) write licence file if key is valid
    root = tk.Tk()
    root.title("SortStream")
    #set size constraits
    root.geometry("550x210") #set default size
    root.minsize(500, 160) #set min size
    app = Licencing(master=root, globalPrivateKey=globalPrivateKey)
    app.update()
    app.mainloop()