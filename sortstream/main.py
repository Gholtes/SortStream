from sortstream.model import createAndTrainModel, loadModel, getPredictions
from sortstream.buildDataset import buildDataset
from sortstream.loadFiles import loadFile
from sortstream.predict import FindAndLoadModel, getTargetFileDirs
from sortstream.log import saveLogs

import numpy as np
import os, sys
import tkinter as tk
from datetime import datetime
import csv

'''
This file houses the workflow funcions and UI to call these functions.
Key workflows:
1) fit: Transform a dataset of files into a trained model in one step.
2) predict: Given a 'data' folder, predict the classes of the files in 'data' and move into their own 
folders by class. If class folders do not exist, create these first.

File Structure:
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

'''

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
		# applicationPath = os.path.abspath(os.path.dirname(__file__))
		applicationPath = os.path.abspath(os.getcwd())
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

class document_classifier():
	def __init__(self, verbose = False, confidenceValue = 75):
		self.applicationPath = GetAppPath()
		self.confidenceValue = confidenceValue
		self.name = "SortStream"
		self.v = verbose

	def fit(self, data_folder = None, preprocess = True):
		timestamp = YYYYMMDDHMS() #get unique timestamp
		
		#Build dataset
		self.update_status("Building dataset...")

		filename = self.name+"builtDataset_"+timestamp
		buildDatasetSatatus, successfulBuildDataset = buildDataset(preprocess = preprocess, 
																	filename = filename, 
																	appPath = self.applicationPath, 
																	data_folder = data_folder,
																	verbose = self.v)
		
		datasetLoc = os.path.join(self.applicationPath, filename+".csv")

		if successfulBuildDataset:
			#load dataset
			self.update_status("Loading dataset...")

			loadedDataset = []
			with open(datasetLoc, "r") as csvfile: #TODO
				reader = csv.reader(csvfile)
				for row in reader:
					loadedDataset.append(row)
			loadedDataset = np.array(loadedDataset[1:])
			
			#train model
			#ensure that new model folder is present
			self.update_status("Training Model...")

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
			self.update_status("Done")
		else:
			#Something is wrong with the dataset build
			self.update_status(buildDatasetSatatus)
			try:
				os.remove(datasetLoc)
			except FileNotFoundError:
				self.update_status("Failed to remove dataset")
		return True

	def predict(self, processingBatchSize = 5):
		self.update_status("Predicting classes")
		#1) find model directory and files:
		#2) Load model and status
		model, classes, status = FindAndLoadModel(self.name, 
													self.applicationPath,
													verbose=self.v)
		self.update_status(status)        
		
		#3 get unprocessed files
		targetFiles = getTargetFileDirs(acceptedFileTypes = [".pdf"], 
										appPath = self.applicationPath, 
										verbose=self.v)
		#catch case where there are no files
		if len(targetFiles) == 0:
			self.update_status("Please add files to the input_files_to_be_sorted folder")  
		
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
					self.update_status("File not classified as prediction probability of {1}% was below threshold: {0}".format(file_i, 100*round(predictionsProbability, 3)))
					os.replace(file_i, os.path.join(self.applicationPath,"predictions", "NotClassified", fileNameOnly))
					#Append logging file
					fileLog = [fileNameOnly, "NotClassified", predictionsProbability, "confidence below threshold, no classification"]
					# for prob in predictionsProbabilities_i[1:]: fileLog.append(prob)
					for prob in predictionsProbabilities_i: fileLog.append(prob)
					logArray.append(fileLog)
		
		#Save logs for this prediction run
		saveLogs(logArray, appPath = self.applicationPath, verbose = self.v)
		return True
	
	def update_status(self, message):
		if self.v:
			print(message)

class document_classifier_gui(tk.Frame, document_classifier):
	def __init__(self, master=None, verbose = True):
		self.applicationPath = GetAppPath()
		self.confidenceValue = 75
		self.name = "SortStream"
		self.v = verbose

		super().__init__(master)
		self.master = master
		self.pack()
		self.createUI()

	def createUI(self):
		#Text items
		self.AppName = tk.Label(self, text = "SortStream - Document Classification")
		self.AppName.grid(row = 1, column = 1, sticky=tk.W+tk.N, padx = 20, pady=10)

		self.Licence = tk.Label(self, text = "MIT License (2020)")
		self.Licence.grid(row = 2, column = 1, sticky=tk.W, padx = 20)

		self.statusValue = tk.StringVar() #init status
		self.update_status("-")
		self.status = tk.Label(self, textvariable = self.statusValue)
		self.status.grid(row = 3, column = 1, sticky=tk.W, padx = 20)
		#4) PREDICT
		self.PREDICT_Button = tk.Button(self, 
													text = "Predict Classes",
													command = self.predict,
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
													command = self.fit,
													width=26)
		self.BuildModelFromData_Button.grid(row=6, column=1, sticky=tk.W, padx = 20)
		#Quit
		self.quit = tk.Button(self, text="Quit", fg="red",
							  command=self.QuitPressed,
							  width=10)
		self.quit.grid(row=6, column=2, sticky=tk.E, padx = 20)

	def QuitPressed(self):
		self.update_status("quit_Button PRESSED")
		#quit the program with master.destroy()
		self.master.destroy()
	
	def update_status(self, message):
		self.statusValue.set(message)


if __name__ == "__main__":
	#1) Get path
	applicationPath = GetAppPath()
	#2) run main
	root = tk.Tk()
	root.title("SortStream")
	#set size constraits
	root.geometry("650x210") #set default size
	root.minsize(500, 160) #set min size
	app = document_classifier_gui(master=root)
	app.update()
	app.mainloop()
