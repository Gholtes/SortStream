from PyPDF2 import PdfFileReader

def pdf2txt(path):
    '''
    Grant Holtes, 10/02/2020
    Opens a pdf file, extracts text data

    inputs: str, a path to a PDF file
    outputs: str, a string of all the text in the pdf that could be extracted.

    runtime ~= 0.05sec per pdf
    '''
    textDump = ""
    with open(path, "rb") as f:
        reader = PdfFileReader(f, strict=False) #strict = False; suppress warnings as some can be fatal
        for page in reader.pages:
            textDumpPage = page.extractText()
            textDump += textDumpPage
    return textDump



