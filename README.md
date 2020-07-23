# SortStream
#### Grant Holtes 2020
### A GUI document classification tool

Sortstream allows non-technical users to train and distribute document classification models.

For product keys, please contact Grant at gwholtes@gmail.com

### Installation:

1) Download SortStream.py from this repository

2) Download and Install python 3.7. A simply method to accomplish this is to use install [anaconda](https://docs.anaconda.com/anaconda/install/) or by installing directly from [python.org](https://www.python.org/downloads/)

3) Once Python is installed and working, run Sortstream.py from your command line or anaconda terminal.
```
$ python Sortstream.py
```

### How to build a model:

In order to sort documents, the system needs to learn how to identify the category of each document. To do this, the user needs to provide a number of examples of each type of document the system would be expected to sort. 

1) Find a few examples of each category (between 10 and 100 is a good sample size)
2) For each category, make a folder that contains all of the examples. The name of this folder will be the name of the category.
3) Put all of these category example folders in a folder named **data** which is in the same file location as the program.
4) Open the program and click “build model”. The program will learn from the examples in the **data** folder, and build a model. This model is saved alongside the program file. Do not change the folder name of the saved model. 

### Classifying Documents:

1) Place the documents that need to be classified into **input_files_to_be_sorted** folder. This folder can either be created manually or will be automatically created the first time you press the **predict** button.
2) Open the program, use the slider to select a confidence value (see Confidence), and click **predict**

The files will be sorted from the input_files_to_be_sorted” folder into subfolders in the **predictions** folder.  Each subfolder contains the documents that belong to a specific category. 

If the system is not confident in a result, it will move the file to a specific subfolder named **NotClassified** in the predictions folder. These need to be sorted manually. 

Each time predict is used, a log file is saved to the **logs** folder. This CSV file lists every file classified and includes confidence levels for all categories alongside other logs. 

### Sharing Models:

This model can then be shared between users if required. 

### Confidence: 

When classifying documents, the user can select the desired confidence level. This is the probability that the classification made by the program is correct, based on the data that the model was trained on. 

The below heuristic can be used:

#### High confidence:
It is highly unlikely that the program will classify a document incorrectly. However, it is likely that only a few documents will be classified, with the remaining requiring manual sorting.

#### Low confidence:
It is more likely that the program will classify a document incorrectly, but very few documents will require manual sorting.
Ultimately the best confidence level to use will change based on the use case, so it is worth inspecting the logs files to see what confidence levels the program is producing on your data. 
It is also worth considering the cost of misclassification relative to the cost of manually sorting documents when choosing the confidence level. 
