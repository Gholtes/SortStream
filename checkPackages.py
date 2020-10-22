'''Grant Holtes 2020
check of requiredPackages are installed, and if no calls Pip to install the packages
'''

import os

#numpy
try:
	import numpy as np
except ModuleNotFoundError:
	os.system("pip install numpy")
	os.system("pip3 install numpy")

#tkinter
try:
	import tkinter 
except ModuleNotFoundError:
	os.system("pip install tkinter")
	os.system("pip3 install tkinter")

#requests
try:
	import requests
except ModuleNotFoundError:
	os.system("pip install requests")
	os.system("pip3 install requests")

#sklearn
try:
	import sklearn
except ModuleNotFoundError:
	os.system("pip install sklearn")
	os.system("pip3 install sklearn")

#PyPDF2
try:
	import PyPDF2
except ModuleNotFoundError:
	os.system("pip install PyPDF2")
	os.system("pip3 install PyPDF2")

#PyPDF2
try:
	import nltk
except ModuleNotFoundError:
	os.system("pip install nltk")
	os.system("pip3 install nltk")

#pkg_resources.py2_warn
# try:
# 	import pkg_resources.py2_warn
# except ModuleNotFoundError:
# 	os.system("pip install pkg_resources.py2_warn")
# 	os.system("pip3 install pkg_resources.py2_warn")