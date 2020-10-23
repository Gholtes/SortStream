# SortStream
#### Grant Holtes 2020
### A GUI Document Classification Tool

Sortstream allows non-technical users to train and distribute AI document sorting models.

### Benefits

#### 1. Your data never leaves your system
SortStream never sends your data via the internet with all processing happening on your computer, including model training. 
SortStream doesn’t even require an internet connection to run, with the only internet connection required used to verify the product code.
This allows you to retain full ownership of your sensitive data and abide by local sovereignty laws

#### 2. Simple to use and incorporate into existing automation solutions
SortStream uses a simple directory based approach to allow non-technical users to easily adapt their workflows to use SortStream. This allows allows existing automation or RPA tools to use with SortStream without complex APIs.

#### 3. Reliable results
Sortstream provides a confidence when it predicts a document’s type, allowing the user to filter out predictions where the model is uncertain of the results. This confidence level is statistically interpretable as the probability of the document being a certain type, based on the training data used.

## Usage

#### GUI Usage

```python
from sortstream import document_classifier_gui

document_classifier_gui() #opens a user interface.
```

#### Usual Usage

```python
from sortstream import document_classifier

sorter = document_classifier()
sorter.fit(data_folder = "/PATH/TO/ROOT/DATA/FOLDER")
sorter.predict()

```

## Installation:

Use pip to install SortStream and its dependancies.

```bash
$ pip install -e git+https://github.com/Gholtes/SortStream.git#egg=sortstream
```

### Requirements

Python 3.7+. A simply method to install Python is to use install [anaconda](https://docs.anaconda.com/anaconda/install/) or by installing directly from [python.org](https://www.python.org/downloads/)

Python packages: `numpy, sklearn, nltk, requests, tkinter, PyPDF2`

### How to Build a Model:

In order to sort documents, the system needs to learn how to identify the category of each document. To do this, the user needs to provide a number of examples of each type of document the system would be expected to sort. 

1) Find a few examples of each category (between 10 and 100 is a good sample size)
2) For each category, make a folder that contains all of the examples. The name of this folder will be the name of the category.
3) Put all of these category example folders in a folder named **data** which is in the same file location as the program.
4) Open the program and click **build model** The program will learn from the examples in the **data** folder, and build a model. This model is saved alongside the program file. Do not change the folder name of the saved model. 

Each time **build model** is used, a new model is created. If multiple models are present in the folder, the program will use the first one it finds.

### Classifying Documents:

1) Place the documents that need to be classified into **input_files_to_be_sorted** folder. This folder can either be created manually or will be automatically created the first time you press the **predict** button.
2) Open the program, use the slider to select a confidence value (see Confidence), and click **predict**

The files will be sorted from the **input_files_to_be_sorted** folder into subfolders in the **predictions** folder.  Each subfolder contains the documents that belong to a specific category. 

If the system is not confident in a result, it will move the file to a specific subfolder named **NotClassified** in the predictions folder. These need to be sorted manually. 

Each time predict is used, a log file is saved to the **logs** folder. This CSV file lists every file classified and includes confidence levels for all categories alongside other logs. 

### Sharing Models:

The model files, which are named **SortStreammodelXXXXX** can be shared between users, and will be used if in the same folder as the **SortStream.py** program file. 

Each time **build model** is used, a new model is created. If multiple models are present in the folder, the program will use the first one it finds.

### Confidence: 

When classifying documents, the user can select the desired confidence level. This is the probability that the classification made by the program is correct, based on the data that the model was trained on. 

The below heuristic can be used:

#### High confidence:
It is highly unlikely that the program will classify a document incorrectly. However, it is likely that only a few documents will be classified, with the remaining requiring manual sorting.

#### Low confidence:
It is more likely that the program will classify a document incorrectly, but very few documents will require manual sorting.

Ultimately the best confidence level to use will change based on the use case, so it is worth inspecting the logs files to see what confidence levels the program is producing on your data. 
It is also worth considering the cost of misclassification relative to the cost of manually sorting documents when choosing the confidence level. 

### Product Pipeline

We are excited to be working on a number of additional pieces of functionality to make SortStream even more useful. These include:
1. Support for MS Office documents
2. Command line interface (CLI) for easy integration into automation solutions
3. Advanced user settings to customise and evaluate the model
4. Automatic dataset balancing
