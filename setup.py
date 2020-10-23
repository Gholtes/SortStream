from distutils.core import setup

setup(
    name='SortStream',
    version='1.0.0',
	author = "Grant Holtes",
	author_email = "gwholes@gmail.com",
    packages=['sortstream'],
	install_requires=[
		"nltk",
		"numpy",
		"PyPDF2",
		"sklearn"
	],
    license='LICENSE.txt',
	description='NLP Document Classification Tool.',
    long_description=open('README.txt').read()
)
