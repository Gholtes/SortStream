# SortStream
### A GUI document classification tool

Sortstream allows non-technical users to train and distribute document classification models.

For product keys, please contact Grant at gwholtes@gmail.com

### Installation 

1) Download SortStream.py from this repository

2) Download and Install python 3.7. A simply method to accomplish this is to use install [anaconda](https://docs.anaconda.com/anaconda/install/) or by installing directly from [python.org](https://www.python.org/downloads/)

3) Once Python is installed and working, run Sortstream.py from your command line or anaconda terminal.

### How to build a model

In order to sort documents, the system needs to learn how to identify the category of each document. To do this, the user needs to provide a number of examples of each type of document the system would be expected to sort. 

1) Find a few examples of each category (between 10 and 100 is a good sample size)
2) For each category, make a folder that contains all of the examples. The name of this folder will be the name of the category.
3) Put all of these category example folders in a folder named “data” which is in the same file location as the program.
4) Open the program and click “build model”. The program will learn from the examples in the “data” folder, and build a model. This model is saved alongside the program file. Do not change the folder name of the saved model. 
