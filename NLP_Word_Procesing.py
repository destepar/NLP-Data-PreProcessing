# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 09:38:25 2021

@author: Daniel Estepa
"""
import PyPDF2
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
# nltk.download()
# nltk.download('punkt')

from nltk.stem import PorterStemmer

import sys
import glob, os
import pickle
import numpy as np

# base=r'D:\USUARIS\GEUGYFH\Desktop\Documents Processing'
base=os.getcwd()
files=os.listdir(base)

try:
    with open("data.pickle","rb") as f:
        String, Nr_Pages, name=pickle.load(f)
        
except:
    
    for root, directories, files in os.walk(base, topdown=False):
        for name in files:
            if name.endswith('.pdf'):
                pdfFileObj = open(os.path.join(root, name), 'rb')
                pdfReader  = PyPDF2.PdfFileReader(pdfFileObj)
                Nr_Pages=pdfReader.getNumPages()
                
                String=[]
                
                for J in range(0,Nr_Pages):
                        # 0,Nr_Pages
                        pageObj = pdfReader.getPage(J)
                        Extract=pageObj.extractText()
                
                        String.append(Extract.split('\n')[0])
                
                        # String =list(filter(lambda x: 'Page' not in x , String))
                        # String =list(filter(lambda x: 'd...' not in x , String))
    
    with open("data.pickle","wb") as f:
           pickle.dump((String,Nr_Pages,name),f)

paragraph=String[230:236]

# paragraph_Flat = [item for sublist in paragraph for item in sublist]

paragraph_Flat='_'.join(paragraph)

# Tokenizing sentences
sentences=nltk.sent_tokenize(paragraph_Flat)
sentences_Ste=nltk.sent_tokenize(paragraph_Flat)
sentences_Lem=nltk.sent_tokenize(paragraph_Flat)


# Tokenizing words
words=nltk.word_tokenize(paragraph_Flat)

# Stemming No sense words
stemmer=PorterStemmer()
for i in range(len(sentences)):
    words_Ste= nltk.word_tokenize(sentences[i])
    words_Ste=[stemmer.stem(word) for word in words_Ste if word not in set(stopwords.words('english'))]
    sentences_Ste[i]=' ' .join(words_Ste)


# Lemming Sense words
lemmatizer= WordNetLemmatizer()
for i in range(len(sentences)):
    words_Lem= nltk.word_tokenize(sentences[i])
    words_Lem=[lemmatizer.lemmatize(word) for word in words_Lem if word not in set(stopwords.words('english'))]
    sentences_Lem[i]=' ' .join(words_Lem)
    

#Bag of words Approach

# Cleaning the text

import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

ps=PorterStemmer()
wordnet=WordNetLemmatizer()
sentences=nltk.sent_tokenize(paragraph_Flat)
corpus=[]

for i in range(len(sentences)):
    review=re.sub('[^a-zA-Z]', ' ', sentences[i])
    review=review.lower()
    review=review.split()
    review=[wordnet.lemmatize(word) for word in review if not word in set(stopwords.words('english'))]
    review=' '.join(review)
    corpus.append(review)

corpus2 = [x for x in corpus if x!='']


    
# Xreating the Bag of Words Model
from sklearn.feature_extraction.text import CountVectorizer

cv=CountVectorizer(max_features=1500)

X=cv.fit_transform(corpus2).toarray()

wrds=cv.get_feature_names_out()

Wrds_Hist=np.sum(X,axis=0)

import matplotlib.pyplot as plt

Wrds_Hist.sort()

plt.bar(np.arange(0,len(Wrds_Hist),1),Wrds_Hist[::-1])





