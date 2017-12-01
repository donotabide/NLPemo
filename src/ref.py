from __future__ import division  # Python 2 users only
import nltk, re, pprint
from nltk import word_tokenize

from collections import Counter
import math

qry1 = open('cran.qry') #Qry file
abst1 = open('cran.all.1400') #abst file

output = open('naz224_HW5_Output.txt','w') #output file

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
                           'you','your','yours','me','my','mine','I','we','us','much','and', 'or'
                           ]
symbolSet = ['!','"','#','$','%','&','(',')','*','+',',','-','.','/',':',';','?','@','[',']','^','_','`','{','|','}','~']

#Get info from cran.qry
isQry = 0
sentTemp = []
listOfQuery = []
for line in qry1.read().split('\r'):
    curr = line.split()
    #check if the following will be a query string
    if len(curr) > 0:
        if curr[0] == '.W':
            isQry = 1
        elif curr[0] == '.I':
            isQry = 0
            if len(sentTemp) > 0:
                listOfQuery.append(' '.join(sentTemp))
                sentTemp = []
        if isQry == 1 and curr[0] != '.W':
            sentTemp += curr
    #Handle the last sentence in the file
    if len(curr) == 0:
        listOfQuery.append(' '.join(sentTemp))

#Clean up the query removing stop words etc
tokens = []
index = 0
for sent in list(listOfQuery):
    text = word_tokenize(sent)
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
    listOfQuery[index] = tokens
    index += 1
    tokens = []

#Create vectors for each query
totalNumberOfQueries = len(listOfQuery)
queryListVector =[]
for query in list(listOfQuery):
    #go through each token in the query
    TFIDFScore = []
    for token in list(query):
        IDFScore = 0
        tokenAppear = 0
        tokenNumberInCurrQuery = 0
        #for the token check how many number of documents which it appears
        for i in list(listOfQuery):
            if token in i:
                tokenAppear += 1
        #IDF Score for the current token
        IDFScore = math.log(totalNumberOfQueries/tokenAppear)
        #Counter number of instances of each token in each query
        tokenNumberInCurrQuery = Counter(query)[token]
        #for i in list(listOfQuery):
            #if token in i:
 #               tokenNumberInCurrQuery += Counter(i)[token]
        #Final TF-IDF score
        TFIDF = IDFScore * tokenNumberInCurrQuery
        TFIDFScore.append(TFIDF)
    #Update the ListOfQuery Array with scores to make vector
    update = []
    index1 = 0
    for item in query:
        #check if the item is already in the score
        #We do not repeat the terms because it is taken into account in the scores via TF
        if not any(d.get(item, None) == TFIDFScore[index1] for d in update):
            update.append({item:TFIDFScore[index1]})
        index1 += 1
    queryListVector.append(update)

#output.write(str(queryListVector))

#Get info from cran.all
isAbs = 0
absTemp = []
listOfAbs = []
index = 0
for line in abst1.read().split('\n'):
    curr = line.split()
    if len(curr) > 0:
        if curr[0] == '.I':
            index += 1
            isAbs = 0
            if len(absTemp) > 0:
                listOfAbs.append(' '.join(absTemp))
                absTemp = []
            #Handle empty lines
            if curr[1] == '472' or curr[1] == '996':
                listOfAbs.append(' '.join(absTemp))
                absTemp = []
        elif curr[0] == '.W':
            isAbs = 1
        if isAbs == 1 and curr[0] != '.W':
            absTemp += curr
        #Handle the last sentence in the file
    if len(curr) == 0:
        listOfAbs.append(' '.join(absTemp))
#output.write(str(listOfAbs))

#Clean up the abst removing stop words etc
abstTokens = []
index = 0
for absrt in list(listOfAbs):
    text = word_tokenize(absrt)
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
        abstTokens.append(item[0])
    #Update the QRY list
    listOfAbs[index] = abstTokens
    index += 1
    abstTokens = []

#output.write(str(listOfAbs))
#print len (listOfAbs)
#print listOfAbs[470]
#print listOfAbs[994]

#IDF scores for each word in collection of abst
totalNumberOfAbst = 1400
IDFScoresWordAbst = {}
for abt in list(listOfAbs):
    for word in abt:
        if word not in IDFScoresWordAbst:
            #check if the IDF scores has been calculated. If so - cal IDF Score
            tokenAppear = 0
            for i in list(listOfAbs):
                if word in i:
                    tokenAppear += 1
            #IDF Score for the current token
            IDFScore = math.log(totalNumberOfAbst/tokenAppear)
            #add to the scores
            IDFScoresWordAbst[word] = IDFScore

#output.write(str(IDFScoresWordAbst))

#Number of instances of each non-stop word in each abstract
abstWordCount = []
wordCount = {}
for abt in list(listOfAbs):
    for word in abt:
        if word not in wordCount:
            #count the number of times it appears in current abst
            wordCount[word] =  Counter(abt)[word]
    abstWordCount.append(wordCount)
    wordCount = {}

#Calucate the scores
queryNumber = 1
abstractNumber = 1
stringOutput = ''
for query in list(queryListVector):
    COSScoresCurrentQuery = []
    COSScoresWithAbst = {}
    abstTracker = 0
    for abst in list(listOfAbs):
        #print query
        finalQueryVector = []
        finalAbstVector = []
        #print abst
        #check if abst is not empty
        if len(abst) > 0:
            #check which words are both in query and abst
            for token in query:
                for t, tokenTFIDF in token.iteritems():
                    #print t
                    #check if token from query also exists in the abst
                    if t in abst:
                        #token in query also exists in abst
                        #Add the token and its TFIDFS score to finalQueryVector
                        finalQueryVector.append(token)
                        #Calculate scores for the AbstVector
                        IDFScoreForWord = IDFScoresWordAbst[t] #get the IDF Abst score
                        wordCountInAbst = abstWordCount[abstTracker][t] #get word count in Abst
                        #Append the final TFIDF score of abst to finalAbtVector
                        finalAbstVector.append({t:IDFScoreForWord*wordCountInAbst})
        #Cal COS scores
        numerator = 0
        queryDemScore = 0
        abstDemScore = 0
        for index in range(0,len(finalQueryVector)):
            for word, score in finalQueryVector[index].iteritems():
                numerator += score * finalAbstVector[index][word]
                abstDemScore += math.pow(finalAbstVector[index][word],2)
        for token in query:
            for t, tokenTFIDF in token.iteritems():
                queryDemScore += math.pow(tokenTFIDF, 2)

        #check if scores are zero
        if numerator != 0 and queryDemScore != 0 and abstDemScore != 0:
            totalCosScore = numerator/math.sqrt(queryDemScore*abstDemScore)
            #Add the scores
            #check if  same score exists
            if totalCosScore not in COSScoresCurrentQuery:
                COSScoresCurrentQuery.append(totalCosScore)
            #Check if the same score exists
            if totalCosScore in COSScoresWithAbst:
                #Same score exists
                COSScoresWithAbst[totalCosScore].append(abstractNumber)
            else:
                #does not exist
                COSScoresWithAbst[totalCosScore] = [abstractNumber]
        else:
            #There is a zero score. Hence there is no relation at all
            totalCosScore = 0.0
            #Add the scores
            #check if  same score exists
            if totalCosScore not in COSScoresCurrentQuery:
                COSScoresCurrentQuery.append(totalCosScore)
            #Check if the same score exists
            if totalCosScore in COSScoresWithAbst:
                #Same score exists
                COSScoresWithAbst[totalCosScore].append(abstractNumber)
            else:
                #does not exist
                COSScoresWithAbst[totalCosScore] = [abstractNumber]            

        abstractNumber += 1                               
        abstTracker += 1
    #End of abst for loop
    #Sort all the scores
    COSScoresCurrentQuery.sort(reverse=True)
    #output the scores ranked order
    for finalScore in COSScoresCurrentQuery:
        #find the score's Abst number
        arrayOfScoreAbst = COSScoresWithAbst[finalScore]
        for abstNumber in arrayOfScoreAbst:
            stringOutput += str(queryNumber) + ' ' + str(abstNumber) + ' ' + str(finalScore) + '\n'
    queryNumber += 1
    abstractNumber = 1
#End of query for loop

#Save output
output.write(stringOutput)

#close fliles
qry1.close()
abst1.close()
output.close()
