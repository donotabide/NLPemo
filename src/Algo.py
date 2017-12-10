from __future__ import division  # Python 2 users only
import nltk, re, pprint
from nltk import word_tokenize

from collections import Counter
import math

import codecs

from nltk.stem.snowball import SnowballStemmer
ps = SnowballStemmer("english")

qry1 = codecs.open('entries.txt', 'a') #Problem file
abst1 = codecs.open('response.txt') #Soltions file

#Sentiments
positiveFile = codecs.open('positive.txt') #Positive words file
negitiveFile = codecs.open('negative.txt') #Negative words file

#outputCheck = open('outputCheck.txt','w') #output file
finalAnswersDoc = open('finalAnswers.txt', 'w') #Finals Answers
answerCheckDoc = open('answerCheck.txt', 'w') #Answer check

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
                line = line.decode('utf-8').strip()
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
                    tokens.append(ps.stem(item[0].lower()))
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
            #print line
            if line != '':
                line = line.decode('utf-8').strip()
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
                    abstTokens.append(ps.stem(item[0].lower()))
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
            solutions = solutions[:3]
            solutionsWithIndex = solutionsWithIndex[:3]
            finalSolutionsWithIndex.append({queryNumber:solutionsWithIndex})
            finalSolutions.append({issue:solutions})
            queryNumber += 1
            abstractNumber = 0
        #End of query for loop for score
        #outputCheck.write(str(stringOutput))

        #WriteOut the Top 5 solutions answerCheckFile.txt
        outputStringForAnswerCheck = ''
        for solSet in finalSolutions:
            issuetxt = ''
            soltuionstxt = ''
            for issue, solutions in solSet.iteritems():
                issue = issue.encode('utf-8').strip()
                issuetxt = str(issue)
                for sol in solutions:
                    sol = sol.encode('utf-8').strip()
                    soltuionstxt = soltuionstxt + '[S]\n' + str(sol) + '\n'
            outputStringForAnswerCheck += '[P]\n' + issuetxt + '\n' + soltuionstxt + '\n\n'
        answerCheckDoc.write(outputStringForAnswerCheck)

        #Handle Sentiments
        finalAnswers = []
        positiveWords = []
        for line in positiveFile.read().split('\n'):
            line = line.decode('utf-8').strip()
            positiveWords.append(ps.stem(line))
        negitiveWords = []
        for line in negitiveFile.read().split('\n'):
            line = line.decode('utf-8').strip()
            negitiveWords.append(ps.stem(line))
        for solSet in finalSolutionsWithIndex:
            #Each problem
            #print 'FOR'
            for issue, solutions in solSet.iteritems():
                #print issue
                #print solutions
                #handle the issue and get the set weights
                issuePosCount = 0.0
                issueNegCount = 0.0
                totalCount = 0.0
                issueWeight = {'Positive':0.0,'Negative':0.0}
                theIssue = listOfQuery[issue]
                noOfWordsInIssue = len(theIssue)
                for word in theIssue:
                    if word in positiveWords:
                        issuePosCount += 1.0
                    elif word in negitiveWords:
                        issueNegCount += 1.0
                if issueNegCount != 0.0 or issuePosCount != 0.0:
                    totalCount = issuePosCount + issueNegCount
                    issueWeight['Positive'] = issuePosCount/noOfWordsInIssue
                    issueWeight['Negative'] = issueNegCount/noOfWordsInIssue
                    negWeightIssue = issueNegCount/noOfWordsInIssue
                #print issueWeight
                #print theIssue

                #handle the solution and get the set weights
                #Reset count
                posCount = 0.0
                negCount = 0.0
                solWeight = 0.0
                scoreArray = []
                solWeightHash = {'Positive':0.0,'Negative':0.0}
                for sol in solutions:
                    #Check if it has a solution if not. No solution
                    if sol != -1:                       
                        theSolution = listOfAbs[sol]
                        #noOfWordsInSolution = len(theSolution)
                        for word in theSolution:
                            if word in positiveWords:
                                posCount += 1.0
                            elif word in negitiveWords:
                                negCount += 1.0
                        if posCount != 0.0 and issueNegCount!= 0.0:
                            solWeight = posCount/issueNegCount #divide by itself or the issue count?
                            scoreArray.append(solWeight)
                            solWeightHash['Positive'] = solWeight
                            solWeightHash['Negative'] = 1.0 - solWeight
                        else:
                            scoreArray.append(-101)
                    else:
                        scoreArray.append(-100)
                #print scoreArray
                #Get closest score to the neg issue weight
                if any(i >= 0 for i in scoreArray):
                    score = min(scoreArray, key=lambda x:abs(x-negWeightIssue))
                    indexOfClosestScore = scoreArray.index(score)
                    #Add the final answers to final array
                    finalAnswers.append({'[PROBLEM]':originalListOfProblems[issue],'[SOLUTION]':originalListOfSolutions[solutions[indexOfClosestScore]],'[SENTIMENT:P]':issueWeight,'[SENTIMENT:S]':solWeightHash})
                else:
                    #There is no sentiment score or no solution.
                    if all(k == -100 for k in scoreArray):
                        #no solution
                        finalAnswers.append({'[PROBLEM]':originalListOfProblems[issue],'[SOLUTION]':'We are sorry. Kindly seek help somewhere else!','[SENTIMENT:P]':issueWeight,'[SENTIMENT:S]':solWeightHash})
                    elif any(k == -101 for k in scoreArray):
                        #no sentiment score - So we take the highest COS score
                        finalAnswers.append({'[PROBLEM]':originalListOfProblems[issue],'[SOLUTION]':originalListOfSolutions[solutions[0]],'[SENTIMENT:P]':issueWeight,'[SENTIMENT:S]':solWeightHash})
                scoreArray=[]
            #Break for each problem
            #break
            
        #Output the finals answers to txt
        finalAnswerOutputString = ''
        for has in finalAnswers:
            problem = ''
            sol = ''
            sentp = ''
            sents = ''
            for key, value in has.iteritems():
                if str(key) == '[PROBLEM]':
                    value = value.encode('utf-8').strip()
                    problem = str(value)
                elif str(key) == '[SOLUTION]':
                    value = value.encode('utf-8').strip()
                    sol = str(value)
                elif str(key) == '[SENTIMENT:P]':
                    sentp = str(value)
                elif str(key) == '[SENTIMENT:S]':
                    sents = str(value)
            finalAnswerOutputString = finalAnswerOutputString + '[PROBLEM]' + ':\n' + problem + '\n' + '[SENTIMENT:P]' + ':\n' + sentp + '\n' + '[SOLUTION]' + ':\n' + sol + '\n' +'[SENTIMENT:S]' + ':\n' + sents + '\n\n\n'
        finalAnswersDoc.write(finalAnswerOutputString)
        #End handle sentiments

        #Print Users Output
        usersProblem = finalAnswers[len(finalAnswers)-1]
        problem = ''
        sol = ''
        sentp = ''
        sents = ''
        for key, value in usersProblem.iteritems():
            if str(key) == '[PROBLEM]':
                value = value.encode('utf-8').strip()
                problem = str(value)
            elif str(key) == '[SOLUTION]':
                value = value.encode('utf-8').strip()
                sol = str(value)
            elif str(key) == '[SENTIMENT:P]':
                sentp = str(value)
            elif str(key) == '[SENTIMENT:S]':
                sents = str(value)
        userOutputString = '\n' + '[PROBLEM]' + ':\n' + problem + '\n' + '[SENTIMENT:P]' + ':\n' + sentp + '\n' + '[SOLUTION]' + ':\n' + sol + '\n' +'[SENTIMENT:S]' + ':\n' + sents + '\n'
        print userOutputString
        
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
#outputCheck.close()
finalAnswersDoc.close()
answerCheckDoc.close()
