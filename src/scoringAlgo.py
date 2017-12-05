from __future__ import division  # Python 2 users only
import nltk, re, pprint
from nltk import word_tokenize

from collections import Counter
import math

import codecs

from nltk.stem.snowball import SnowballStemmer
ps = SnowballStemmer("english")

answerCheck = codecs.open('answerCheck.txt') #Answer check file from ALgo
answers = codecs.open('answers.txt') #Answers file
answersDebug = open('answersDebug.txt','w') #output file

totalAllInstances = 0.0
totalCorrectAnswers = 0.0
totalCorrectInAnswerKey = 0.0
totalSystemMarkCorrect = 0.0

answerCheckDic = {}
answersDic = {}

#Get all the information from answerCheck
currentProblem = ''
problemOrSol = 0
for line in answerCheck.read().split('\n'):
    line = line.decode('utf-8').strip()
    if line != '':
        if line == '[P]':
            problemOrSol = 1.0
            continue
        elif line == '[S]':
            problemOrSol = -1.0
            continue

        if problemOrSol == 1.0:
            currentProblem = line
            answerCheckDic[currentProblem] = []
            problemOrSol == 0
        elif problemOrSol == -1.0:
            answerCheckDic[currentProblem].append(line)
            problemOrSol = 0
    elif line == '':
        currentProblem = ''

#Get all the answers from answers.txt
currentProblem = ''
problemOrSol = 0
for line in answers.read().split('\n'):
    line = line.decode('utf-8').strip()
    if line != '':
        if line == '[P]':
            problemOrSol = 1.0
            continue
        elif line == '[S]':
            problemOrSol = -1.0
            continue

        if problemOrSol == 1.0:
            currentProblem = line
            answersDic[currentProblem] = []
            problemOrSol == 0
        elif problemOrSol == -1.0:
            answersDic[currentProblem].append(line)
            problemOrSol = 0
    elif line == '':
        currentProblem = ''

#Calculate the scores
for problem, solutions in answerCheckDic.iteritems():
    #get the solutions in the real answer key
    realSolutions = answersDic[problem]

    #update correct answer key
    totalCorrectInAnswerKey += len(realSolutions)
    #update total answer instances
    totalAllInstances += len(solutions)
    #update system mark correct
    totalSystemMarkCorrect += len(solutions)
    for ans in solutions:
        if ans in realSolutions:
            totalCorrectAnswers += 1

#Final score calcuation
precision = totalCorrectAnswers/totalSystemMarkCorrect
recall = totalCorrectAnswers/totalCorrectInAnswerKey
fmeasure = 2.0/( (1.0/precision) + (1.0/recall))

print 'System Evaluation: '
print 'Precision: ' + str(precision)
print 'Recall: ' + str(recall)
print 'F-Measure: ' + str(fmeasure)


answersDebug.close()
