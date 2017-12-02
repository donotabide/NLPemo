from __future__ import division  # Python 2 users only
import nltk, re, pprint
from nltk import word_tokenize

from collections import Counter
import math

qry1 = open('entries.txt', 'a') #Problem file
abst1 = open('response.txt') #Soltions file

#Sentiments
positiveFile = open('positive.txt') #Positive words file
negitiveFile = open('negative.txt') #Negative words file

outputCheck = open('outputCheck.txt','w') #output file
finalAnswersDoc = open('finalAnswers.txt', 'w') #Finals Answers

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

while True:
    print 'Type \'entry\' to enter your problem'
    print 'or'
    print 'Type \'update\' to add a new problem and solution to the database'
    userinput = raw_input("Enter your option: ")
    if userinput == 'entry':
        userinput = raw_input("Enter your problem: ")
        #Write to the database the users new problem
        qry1.write('\n')
        qry1.write('\n')
        qry1.write(userinput)
        qry1.close()
        
        qry1 = open('entries.txt') #Problem file
        #Get info from response.txt and clean it up
        originalListOfProblems = []
        listOfQuery = []
        tokens = []
        for line in qry1.read().split('\n'):
            if line != '':
                originalListOfProblems.append(line)
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
                    tokens.append(item[0].lower())
                #Update the QRY list
                listOfQuery.append(tokens)
                tokens = []
        #end of for loop
    
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
        #End of score TFIDF for qurey

        #get information from the solutions set'
        originalListOfSolutions = []
        listOfAbs = []
        abstTokens = []
        for line in abst1.read().split('\n'):
            if line != '':
                originalListOfSolutions.append(line)
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
                    abstTokens.append(item[0].lower())
                #Update the problems list
                listOfAbs.append(abstTokens)
                abstTokens = []
        #end of for loop               

        #IDF scores for each word in collection of problems
        totalNumberOfAbst = len(listOfAbs)
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
        #End of IDF scores for each word in collection of problem
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
        #End of TF for words in problem
        
        #Calucate the scores
        queryNumber = 0
        abstractNumber = 0
        stringOutput = ''
        finalSolutions = []
        finalSolutionsWithIndex = []
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
            issue = originalListOfProblems[queryNumber]
            solutions = []
            solutionsWithIndex = []
            for finalScore in COSScoresCurrentQuery:
                #find the score's Abst number
                arrayOfScoreAbst = COSScoresWithAbst[finalScore]
                for abstNumber in arrayOfScoreAbst:
                    stringOutput += str(queryNumber) + ' ' + str(abstNumber) + ' ' + str(finalScore) + '\n'
                    #Add the top 10 solutions for each problem

                    #check if able to find solution
                    solution = originalListOfSolutions[abstNumber]
                    solutionIndex = abstNumber
                    if finalScore == 0.0:
                        solution = 'We are sorry. Kindly seek help somewhere else!'
                        solutionIndex = -1
                    solutions.append(solution)
                    solutionsWithIndex.append(solutionIndex)
            solutions = solutions[:5]
            solutionsWithIndex = solutionsWithIndex[:5]
            finalSolutionsWithIndex.append({queryNumber:solutionsWithIndex})
            finalSolutions.append({issue:solutions})
            queryNumber += 1
            abstractNumber = 0
        #End of query for loop for score
        outputCheck.write(str(stringOutput))

        #WriteOut the Top 5 solutions answerCheckFile.txt
            #TODO

        #Handle Sentiments
        finalAnswers = []
        positiveWords = []
        for line in positiveFile.read().split('\n'):
            positiveWords.append(line)
        negitiveWords = []
        for line in negitiveFile.read().split('\n'):
            negitiveWords.append(line)
        for solSet in finalSolutionsWithIndex:
            #Each problem
            for issue, solutions in solSet.iteritems():
                #handle the issue and get the set weights
                issuePosCount = 0.0
                issueNegCount = 0.0
                totalCount = 0.0
                issueWeight = {'pos':0.0,'neg':0.0}
                theIssue = listOfQuery[issue]
                noOfWordsInIssue = len(theIssue)
                for word in theIssue:
                    if word in positiveWords:
                        issuePosCount += 1.0
                    elif word in negitiveWords:
                        issueNegCount += 1.0
                if issueNegCount != 0.0 or issuePosCount != 0.0:
                    totalCount = issuePosCount + issueNegCount
                    issueWeight['pos'] = issuePosCount/noOfWordsInIssue
                    issueWeight['neg'] = issueNegCount/noOfWordsInIssue
                    negWeightIssue = issueNegCount/noOfWordsInIssue
                #print issueWeight
                #print theIssue

                #handle the solution and get the set weights
                #Reset count
                posCount = 0.0
                negCount = 0.0
                solWeight = 0.0
                scoreArray = []
                for sol in solutions:
                    #Check if it has a solution if not. No solution
                    if sol != -1:                       
                        theSolution = listOfAbs[sol]
                        #noOfWordsInSolution = len(theSolution)
                        for word in theSolution:
                            if word in positiveWords:
                                posCount += 1.0
                        if posCount != 0.0 and totalCount != 0.0:
                            solWeight = posCount/totalCount #divide by itself or the issue count?
                            scoreArray.append(solWeight)
                        else:
                            scoreArray.append(-101)
                    else:
                        scoreArray.append(-100)
                #Get closest score to the neg issue weight
                if any(i >= 0 for i in scoreArray):
                    score = min(scoreArray, key=lambda x:abs(x-negWeightIssue))
                    indexOfClosestScore = scoreArray.index(score)
                    #Add the final answers to final array
                    finalAnswers.append({'problem':originalListOfProblems[issue],'solution':originalListOfSolutions[solutions[indexOfClosestScore]],'sent':issueWeight})
                else:
                    #There is no sentiment score or no solution.
                    if all(k == -100 for k in scoreArray):
                        #no solution
                        finalAnswers.append({'problem':originalListOfProblems[issue],'solution':'We are sorry. Kindly seek help somewhere else!','sent':issueWeight})
                    elif any(k == -101 for k in scoreArray):
                        #no sentiment score - So we take the highest COS score
                        finalAnswers.append({'problem':originalListOfProblems[issue],'solution':originalListOfSolutions[solutions[0]],'sent':issueWeight})
                scoreArray=[]
                #Output the finals answers to txt
                finalAnswersDoc.write(str(finalAnswers))
            #End handle sentiments
            
            
            #Break for each problem
            #break
        #while loop break
        break
    elif userinput == 'update': #User decided to enter a new problem soltuion pair to the program
        problem = raw_input("Enter a new problem: ")
        problem += str(problem) + '\n'
        qry1.write(problem)
        solution = raw_input("Enter a new solution: ")
        solution += str(solution) + '\n'
        abst1.write(solution)
        break

#close fliles
qry1.close()
abst1.close()
positiveFile.close()
negitiveFile.close()
outputCheck.close()
