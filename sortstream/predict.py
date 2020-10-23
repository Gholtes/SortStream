from sortstream.model import loadModel
import os

def FindAndLoadModel(name, appPath = ".", verbose = False):
	#1) find model directory and files:
	#return model directory
	home = os.listdir(appPath)
	cnt = sum([1 if x[:len(name + "model")]==name + "model" else 0 for x in home])
	status = ""
	if cnt == 1:
		for i in home:
			if i[:len(name + "model")]==name + "model":
				modelDir = i
		status = "Using model {0}".format(modelDir)
		if verbose:
			print(status)

	elif cnt > 1:
		print("There are {0} model folders. Remove extras?".format(cnt))
		for i in home:
			if i[:len(name + "model")]==name + "model":
				modelDir = i
		status = "{0} model folders found. \n Using {1}".format(cnt, modelDir)
		if verbose:
			print(status)

	elif cnt == 0:
		status = "0 model folders found. Train a model before using predict"
		print(status)
		model = None
		return model, None, status

	#check if destination folder exists
	if not "predictions" in home:
		# self.statusValue.set("Making new output folder as 'predictions' folder missing")
		if verbose:
			print("Making new output folder as \n 'predictions' folder missing")
		os.mkdir("predictions")
	
	#2) load model
	if verbose:
		print("Load Model files")
	model = loadModel(folder = os.path.join(appPath, modelDir)) #TODO

	#check if destination subfolders exists
	classes = model[1].classes_
	classes = [str(c) for c in classes]
	classes.append("NotClassified")
	classesDir = os.listdir(os.path.join(appPath, "predictions"))

	for class_ in classes:
		if (not class_ in classesDir) and (not str(class_) == "Category"):
			os.mkdir(os.path.join(appPath, "predictions", class_))

	return model, classes, status

def getTargetFileDirs(acceptedFileTypes = [".pdf"], appPath = ".", verbose = False):
	'''
	Grant Holtes 24/5/20
	returns a list of acceptable input file locations 
	full path is used eg "input_files_to_be_sorted/FILENAME.pdf"
	'''
	home = os.listdir(appPath)
	#check if source folder exists
	if not "input_files_to_be_sorted" in home:
		# self.statusValue.set("Making new output folder as 'predictions' folder missing")
		if verbose:
			print("Making new output folder as \n 'input_files_to_be_sorted' folder missing")
		os.mkdir("input_files_to_be_sorted")
	
	files = os.listdir(os.path.join(appPath, "input_files_to_be_sorted"))
	filesToBeSorted = []
	for file_ in files:
		for fileType in acceptedFileTypes:
			if fileType == file_[-len(fileType):]:
				filesToBeSorted.append(os.path.join(appPath, "input_files_to_be_sorted", file_))
				break

	return filesToBeSorted


