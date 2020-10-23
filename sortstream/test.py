import os

def path():
	applicationPath = os.path.abspath(os.getcwd())
	print(applicationPath)