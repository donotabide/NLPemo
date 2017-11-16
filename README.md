# Information Retrieval/Extraction in Emotional-Solution Entries 

This project intends to perform information extraction of emotional entries and matching them with potential solution paragraphs. Our goal is to perform an assessment of users emotional states, giving them a platform to post, relate to others and receive potential solutions anonymously. 

## Overview
Using past emotional entries the program suggests a potential solution for a user’s current emotional state. The program assigns emotional “weights” and draws from a database of potential solution based on these emotional weightages.

##  Data
Emotional Word Bank
Text.txt document containing a list of words and their associated emotions each entry in a new line
afraid \t fear \t sadness \n
### Emotional Tag’s
1) Happiness 2) Sadness 3) Fear/Surprise 4) Anger/Disgust
### Gathering Data
Entries from Students about their current “status” on NYU Secrets and other colleges Secret pages - A Facebook page that posts thoughts from anonymous university students.
These entries are used to create our emotional word bank. Key words from each entry are manually selected and emotional tags assigned.
Words are selected manually due to the use of “slang” in common speech e.g “Going nuts”

### Other potential data sources
Extract - Twitter API and other web scraping API
### Potential Solutions
Text.txt document containing a list of potential solutions each entry in a new line. Each potential solution has emotional weights attached.
E.g Slow down your breathing and read a book \t happiness 0 sadness 30 fear/surprise 70 anger/disgust 0
Potential solutions taken from the comments section of the facebook posts. We also aim to create our own potential solutions.


## Data Sources:
*“Secrets” pages on Twitter and Facebook
	* Entries as paragraph problem
	* Use comments as possible solutions
* Medical Subject Headings thesaurus (MeSH) to promote sentiment analysis of whether the entry is emotional or not 

## Input and Output Data Format
### Input
User enters an input in the command line console. 
e.g “I spilled my coffee on my shirt, almost lost my phone, had a pop quiz that went terribly but was able to pet two adorable golden retriever puppies on the subway today”.
Output
The program outputs a suggested solution or comment
E.g “Take a deep breath. You’ll be fine”

### Process
SenPy, NLTK using Sentiment Analysis and Information retrieval, give weights to pre-defined emotions and solutions. 

### Alternative 1: The Algorithm (Input as problem paragraph)
* Summarization of paragraph
* Detect “key words”
* Match “key words” with the emotional word bank 
* Assign emotional score based on 4 categories of emotional words 
* Based on the score match 2 - 5 closest solutions 
* Provide one of the possible best solution to the users

### Alternative 2: as Queries (input)
* Summarize problem paragraph
* Sentiment analysis:  is it an emotional entry or not?
* Make it into a query vector
* Run search in database to see correlation in database
* Number of documents with the vector words
* Run vector through database to see which solution paragraph has best match
* Return best match


### Responsibilities

#### Arjun Madgavkar:
* Data scraping & formatting
* Assigning weights based on input and emotional bank
* iPhone application (designs and development, if we want to create one)
#### Han Zhang:
* Building emotional words bank 
* Matching input to an existing bank of solutions vectors
#### Jaeduk Choi: 
* assigning weights based on input and emotional bank
* building emotional words bank
#### Nicholas Ang:
* Data scraping & formatting
* Building solutions word bank and assigning attributes to solutions
#### Ricardo Nunes:
* Data scraping and formating 
* Emotional words bank
* Data processing using vectors
	

## Possible Paid Algorithms
* https://algorithmia.com/algorithms/nlp/Summarizer Summarizes text  
* https://algorithmia.com/algorithms/nlp/SocialSentimentAnalysis Assign sentiment analysis 

### URL sources: 
* https://www.facebook.com/NYUSecrets/
* https://www.facebook.com/BruinSecrets/
* https://www.facebook.com/BerkeleySecrets/
* https://meshb.nlm.nih.gov/record/ui?ui=D004644 

