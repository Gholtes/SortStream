from sortstream.pdf2txt import pdf2txt

def loadFile(path):
	'''
	Grant Holtes 24/11/20
	uses premade functions and file exctension to load file as text
	'''
	text = ""
	if path[-4:].lower() == ".pdf":
		text = pdf2txt(path)

	return text