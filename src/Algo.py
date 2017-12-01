from __future__ import division  # Python 2 users only
import nltk, re, pprint
from nltk import word_tokenize

from collections import Counter
import math

qry1 = open('entries.txt')#Qry file
abst1 = open('response.txt') #abst file

output = open('output.txt','w') #output file

closed_class_stop_words = ['a','the','an','and','or','but','about','above','after','along','amid','among',\
                           'as','at','by','for','from','in','into','like','minus','near','of','off','on',\
                           'onto','out','over','past','per','plus','since','till','to','under','until','up',\
                           'via','vs','with','that','can','cannot','could','may','might','must',\
                           'need','ought','shall','should','will','would','have','had','has','having','be',\
                           'is','am','are','was','were','being','been','get','gets','got','gotten',\
                           'getting','seem','seeming','seems','seemed',\
                           'enough', 'both', 'all', 'your' 'those', 'this', 'these', \
                           'their', 'the', 'that', 'some', 'our', 'no', 'neither', 'my',\
                           'its', 'his' 'her', 'every', 'either', 'each', 'any', 'another',\
                           'an', 'a', 'just', 'mere', 'such', 'merely' 'right', 'no', 'not',\
                           'only', 'sheer', 'even', 'especially', 'namely', 'as', 'more',\
                           'most', 'less' 'least', 'so', 'enough', 'too', 'pretty', 'quite',\
                           'rather', 'somewhat', 'sufficiently' 'same', 'different', 'such',\
                           'when', 'why', 'where', 'how', 'what', 'who', 'whom', 'which',\
                           'whether', 'why', 'whose', 'if', 'anybody', 'anyone', 'anyplace', \
                           'anything', 'anytime' 'anywhere', 'everybody', 'everyday',\
                           'everyone', 'everyplace', 'everything' 'everywhere', 'whatever',\
                           'whenever', 'whereever', 'whichever', 'whoever', 'whomever' 'he',\
                           'him', 'his', 'her', 'she', 'it', 'they', 'them', 'its', 'their','theirs',\
                           'you','your','yours','me','my','mine','I','we','us','much','and', 'or', \
                           ]
symbolSet = ['!','"','#','$','%','&','(',')','*','+',',','-','.','/',':',';','?','@','[',']','^','_','`','{','|','}','~']


#Get info from response.txt and clean it up
listOfQuery = []
tokens = []
for line in qry1.read().split('\n'):
    text = word_tokenize(line)
    tagged = nltk.pos_tag(text)
    
    for item in list(tagged):
        #check if has stop words to remove, numbers or punctuation
        if item[0] in closed_class_stop_words:
            #remove that from the original
            tagged.remove(item)
        if item[1] == 'NUM':
            tagged.remove(item)
        if item[1] == 'CD':
            tagged.remove(item)
        if item[0] in symbolSet:
            tagged.remove(item)
    
    #Extract all the tokens from tagged
    for item in tagged:
        tokens.append(item[0])
    #Update the QRY list
    listOfQuery.append(tokens)
    tokens = []

    print listOfQuery
    break



#close fliles
qry1.close()
abst1.close()
output.close()
