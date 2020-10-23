from distutils.core import setup

setup(
    name='SortStream',
    version='1.2.0',
	author = "Grant Holtes",
	author_email = "gwholes@gmail.com",
	url = "https://github.com/Gholtes/SortStream",
	keywords = ["nlp", "classification", "document", "pdf"]
    packages=['sortstream'],
	install_requires=[
		"nltk",
		"numpy",
		"PyPDF2",
		"sklearn"
	],
    license="MIT",
	description='NLP Document Classification Tool.',
    long_description=open('README.txt').read()
)
