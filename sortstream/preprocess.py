from nltk import WordPunctTokenizer
from nltk.stem import PorterStemmer
import re

# If we need to download corpus to use lemmatizer
# import nltk
# nltk.download('wordnet')
# lemmatizer = WordNetLemmatizer()  #NOT USED

def setupTextPreProcess():
    #import stopwords
    global stopWords
    global tokenizer
    global stemmer

    #save some space
    stopWords = ['wouldn', 'which', "it's", "didn't", 'her', 'she', "hasn't", "you've", 'some', 'more', 'is', 'couldn', 'hers', 'no', 'so', 'ours', 'd', "shouldn't", 'off', 'was', 'about', "mightn't", 'own', 'above', 'most', 'out', 'you', 'just', "hadn't", 'haven', 'o', 'once', 'shouldn', 'few', 'y', 've', 'your', 'ourselves', 'why', 'does', 'me', 'at', 'mustn', "you'd", 'then', 'weren', 're', 'below', 'should', 'doesn', 'when', "she's", 'can', 'of', 'that', "weren't", 'after', 'any', "should've", 'wasn', 't', 'very', 'these', 'yourself', 'nor', 'my', 'won', 'his', 'both', 'same', 'yours', 'only', 'but', 'our', 'it', 'has', 'be', "wasn't", 'herself', 'its', 'mightn', "needn't", 'as', 'am', 'are', 'they', 'their', 'doing', 'during', 'again', 'all', "doesn't", 'between', 'under', 'over', "that'll", "haven't", 'this', 'will', 'until', "couldn't", 'had', 'myself', 'because', 'than', "won't", 'he', 'have', 'with', 'don', 'hadn', 'who', 'up', "wouldn't", 'ain', 'them', 'i', 'through', 'aren', 'here', 'themselves', "shan't", 'if', 'what', 'ma', 'yourselves', 'theirs', 'a', 'against', 'being', 'to', 'where', 'on', 'having', 'himself', 'each', "you'll", "don't", 'further', "isn't", 'while', 'in', 'how', 'such', 'now', 'from', 'needn', 'there', 'hasn', 'too', 'm', 'or', 'not', 'didn', 'whom', 'down', 'shan', 'll', "you're", 's', "mustn't", 'him', 'were', 'an', 'we', "aren't", 'by', 'been', 'the', 'itself', 'before', 'did', 'into', 'and', 'for', 'do', 'other', 'those', 'isn']

    tokenizer = WordPunctTokenizer()
    stemmer = PorterStemmer()

def preprocessText(text, stem = True):
    '''
    Grant Holtes, 15/02/2020
    input: str, a string
    output: str, a normalised string

    requires setupTextPreProcess() is run before calling

    Time to run ~= 0.0150 secounds per page of text with stemming,
                ~= 0.0010 secounds per page of text with no stemming
    '''
    #Remove non A-z chars
    maxLength = 100 # regex seems to fail on very long strings, so pass as substrings then reassemble
    substrings = [text[i:i+maxLength] for i in range(0, len(text), maxLength)]
    regexProcessedText = ""
    for substring in substrings:
        regexProcessedText += re.sub(r'[^a-zA-Z\s]', '', substring, re.I|re.A)
    # text = re.sub(r'[^a-zA-Z\s]', '', text, re.I|re.A) #processess string as one
    text = regexProcessedText
    #Make all text lower case
    text = text.lower()
    #get word tokens / splir
    textTokens = tokenizer.tokenize(text)
    #remove stopwords
    textTokens = [token for token in textTokens if token not in stopWords]
    #perform any required stemming
    if stem:
        normalizedTokens = []
        for char in textTokens:
            normalizedTokens.append(stemmer.stem(char))
        return ' '.join(normalizedTokens)
    else:
        return ' '.join(textTokens)

# text = "test 1 2 _ - end test"
# setupTextPreProcess()
# print(preprocessText(text))

