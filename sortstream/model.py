from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
import pickle
from sortstream.preprocess import setupTextPreProcess, preprocessText
from numpy import ndarray as ndarray
import os

def createAndTrainModel(xTrain, yTrain, xTest, yTest, saveloc = "model",
                        maxFeatures = 1000, 
                        batchSize=100,
                        epochsTrain = 10,
                        appPath = "."
                        ):
    '''
    Grant Holtes, 15/02/2020
    input:  xTrain, xTest; input training and test data, as preprocessed text in a list of strings,
            yTrain, yTest; target training and test data, as a finite set of text or numeric labels in a list.
    output: 3 sklearn models are saved to disk
    '''

    #preprocesses data
    vectorizer = TfidfVectorizer(strip_accents='ascii',
                                    analyzer = "word",
                                    max_df=1.0, 
                                    min_df=0.0,
                                    max_features = 1000,
                                    )

    #Train vectorizer on the training set
    xTrainVectorised = vectorizer.fit_transform(xTrain).toarray()
    #vectorize test set
    # xTestVectorised = vectorizer.transform(xTest).toarray()

    #The max features may not be used, so check how many features were created
    featuresCount = xTrainVectorised.shape[1]

    #Define and train multinomial logistic regression
    model = LogisticRegression(solver='lbfgs',
                                multi_class='multinomial',
                                max_iter = 2000
                                )
    #Fit
    model.fit(xTrainVectorised, yTrain.transpose()[0])
 
    #Save models
    with open(os.path.join(appPath, saveloc, "vectorizerX"), "wb") as pickleFile: #TODO
        pickle.dump(vectorizer, pickleFile)
    with open(os.path.join(appPath, saveloc, "logistic"), "wb") as pickleFile: #TODO
        pickle.dump(model, pickleFile)

    return True

def loadModel(folder = "model",
                vectorizerX = "vectorizerX",
                model = "logistic",
                appPath = "."):
    '''
    Grant Holtes, 15/02/2020
    input: locations of the 2 sklearn models and 1 tf model are saved to disk that are created when createAndTrainModel() is run
    output: a tuple of the loaded models

    Requires createAndTrainModel() has been run
    '''
    #load models
    vectorizer = pickle.load(open(os.path.join(folder, vectorizerX), "rb" ))
    Model = pickle.load(open(os.path.join(folder, model), "rb"))
    return (vectorizer, Model)

def getPredictions(x, modelTuple, preprocess = True):
    '''
    Grant Holtes, 15/02/2020
    input:  x, a string or list of strings that have not been preporcessed yet
            modelTuple, a tuple of the loaded models output by loadModel
    output: a list of predictions of the category that the input string(s) belong to

    Requires createAndTrainModel() and loadModel() has been run
    '''
    (vectorizer, model) = modelTuple

    if preprocess:
        #preprocess input
        setupTextPreProcess()
        if isinstance(x, list) and isinstance(x[0], str): #check that the input is a LIST of STRINGS
            xPreProcessed = []
            for item in x:
                xPreProcessed.append(preprocessText(item)) #do initial text processing

        elif isinstance(x, str):
            xPreProcessed = [preprocessText(x)] #do initial text processing
        
        else:
            print("ERROR: unsupported data type passed as x")
            exit()

    else: #if no preprocessing
        if isinstance(x, list) and isinstance(x[0], str): # check if the input is a LIST of STRINGS 
            xPreProcessed = x
        
        elif isinstance(x, ndarray): #if no preprocessing, allow for numpy data for testing purposes
            xPreProcessed = x
        
        else:
            print("ERROR: unsupported data type passed as x")
            exit()
    #feed data through model
    #vectorise text
    xVectorised = vectorizer.transform(xPreProcessed).toarray() #vectorise input
    #predict class
    predictionsLabel = model.predict(xVectorised)
    predictionsProbabilities = model.predict_proba(xVectorised)
    #transform back to label

    return predictionsLabel, predictionsProbabilities
