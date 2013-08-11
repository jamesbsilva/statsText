#!/usr/bin/env python
##########################################################
#
#            statsText
#
#       This takes text and calculates the frequency
#   of characters/words/sentences in a piece of text
#   including the length.
#
#   @author : jbsilva
#
##########################################################

import re
from math import floor

lastWord = ""
alphabetSize = 26

def analyzeText(text):
    textSpl = text.split()

    maxSenLen = 80
    maxWordLen = 40
    global alphabetSize

    # initialize list of frequencies
    wordLenFreq = [0 for x in range(maxWordLen)]
    senLenFreq = [0 for x in range(maxSenLen)]
    wordLen1Freq = [0 for x in range(maxWordLen*maxWordLen)]
    senLen1Freq = [0 for x in range(maxSenLen*maxSenLen)]
    wordFreq = {}
    charFreq = [0 for x in range(alphabetSize+alphabetSize+10)]
    char1Freq = [0 for x in range(alphabetSize*alphabetSize)]
    char2Freq = [0 for x in range(alphabetSize*alphabetSize)]
    charLowFreq = [0 for x in range(alphabetSize)]
    charInitFreq = [0 for x in range(alphabetSize)]
    charInit2Freq = [0 for x in range(alphabetSize)]

    # indices to calculate sentence length and relationship between lengths
    lastWordIndex = 0
    lastSenLen = 0
    lastWordLen = 0
    wordIndex = 0

    for word in textSpl:
        #sentence length data
        if isSentenceEnd(word):
            if lastSenLen > 0:
                #print "last senLen| ",lastSenLen,"    curr| ",(wordIndex -lastWordIndex),"    word| ",word
                senLen1Freq[lastSenLen+maxSenLen*((wordIndex -lastWordIndex))] += 1
            senLenFreq[(wordIndex -lastWordIndex)] += 1
            lastSenLen = (wordIndex -lastWordIndex)
            lastWordIndex = wordIndex
        wordIndex += 1
        # characters in word data
        analyzeWord(word,charFreq,charInitFreq,charInit2Freq,charLowFreq,char1Freq,char2Freq,wordFreq,wordLenFreq)
        # word length data
        if lastWordLen > 0:
            wordLen1Freq[lastWordLen+maxWordLen*(len(re.sub('[\W_]+', '', word)))] += 1
        lastWordLen = len(re.sub('[\W_]+', '', word))


    # save data
    saveDir = "./"
    saveListChar(charFreq,saveDir+"charFreqSum.txt")
    saveList(charInitFreq,saveDir+"charInitFreqSum.txt")
    saveList(charInit2Freq,saveDir+"charInit2FreqSum.txt")
    saveListChar(charLowFreq,saveDir+"charFreqLowSum.txt")
    saveListCharTransf(char1Freq,saveDir+"char1FreqSum.txt")
    saveListCharTransf(char2Freq,saveDir+"char2FreqSum.txt")
    saveList(charFreq,saveDir+"charFreqRawSum.txt")
    saveList(charLowFreq,saveDir+"charFreqLowRawSum.txt")
    saveList(char1Freq,saveDir+"char1FreqRawSum.txt")
    saveList(char2Freq,saveDir+"char2FreqRawSum.txt")
    saveList(wordLenFreq,saveDir+"wordLenFreqSum.txt")
    saveList(senLenFreq,saveDir+"senLenFreqSum.txt")
    saveList(wordLen1Freq,saveDir+"wordLen1FreqSum.txt")
    saveList(senLen1Freq,saveDir+"senLen1FreqSum.txt")
    saveDict(wordFreq,saveDir+"wordFreqSum.txt")
    return [charFreq,wordLenFreq,senLenFreq,wordFreq]

def saveList(newList, fileName):
	thefile = open(fileName, 'w')
	for item in newList:
  		thefile.write("%s\n" % item)

def saveListChar(newList, fileName):
	charOffset = 0
	thefile = open(fileName, 'w')
	indexIn = 0
	for item in newList:
		if item is not 0:
	  		thefile.write("%s , %s \n" % (item, getNewCharFromIndex(indexIn)) )
		indexIn += 1

def saveListCharTransf(newList, fileName):
    global alphabetSize
    thefile = open(fileName, 'w')
    indexIn = 0
    for item in newList:
        if item is not 0:
            thefile.write("%s , %s , % s\n" % (item, getNewCharFromIndex(int(floor(indexIn/alphabetSize))),getNewCharFromIndex(int(indexIn%alphabetSize))) )
        indexIn += 1

def saveDict(newDict, fileName):
    thefile = open(fileName, 'w')
    for key in newDict.keys():
        if newDict[key] is not " ":
            thefile.write("%s , %s \n" % (key, newDict[key]))

# load a file and process it
def loadAndAnalyze(fileName):
	f = open(fileName, 'r')
	fileStr = f.read()
	return analyzeText(fileStr)

# map characters to 0-26 lowercase and 26-52 uppercase and rest numerical
def getNewCharIndex(charIn):
    if ord(charIn) < 64:
        return ord(charIn)+4
    if charIn.isalpha():
        # lower case
        if ord(charIn) > 96:
            return ord(charIn)-97
        #uppercase
        else:
            return ord(charIn)-39
    return 63

# rule for what is a word in end of statement
def isSentenceEnd(wordIn):
    if "." in wordIn :
        return True
    if "," in wordIn :
        return True
    if chr(34) in wordIn :
        return True
    if "?" in wordIn :
        return True
    if ";" in wordIn :
        return True
    if "!" in wordIn :
        return True
    return False

# map back from characters to 0-26 lowercase and 26-52 uppercase and rest numerical
def getNewCharFromIndex(charIn):
    # numerical
    if charIn > (2*alphabetSize-1):
        return chr(charIn-4)
    # upper case alphabet
    elif charIn > (alphabetSize-1):
        return chr(charIn+39)
    else:
        return chr(charIn+97)

# get indice for character sequence data
def getCharTransfInd(charIn, charLast):
    if charIn.isalpha() and charLast.isalpha():
        return (getNewCharIndex(charIn.lower())+26*getNewCharIndex(charLast.lower()))

# analyze a word for data to be taken
def analyzeWord(wordIn, charFreq,charInitFreq,charInit2Freq,charLowFreq, char1Freq, char2Freq, wordFreq, wordLenFreq):
    global lastWord
    global last1Char
    global last2Char
    # strip the word to alphanum
    word  = re.sub('[\W_]+', '', wordIn)
    initWord = False
    initWord2 = False
    # character frequency analysis
    for charec in word:
        #print type(charec)
        charFreq[getNewCharIndex(charec)] += 1
        if charec.isalpha():
            #print "char | ",charec
            charLowFreq[getNewCharIndex(charec.lower())] += 1
            if initWord2:
                if last1Char.isalpha():
                    char1Freq[getCharTransfInd(charec,last1Char)] += 1
                if last2Char.isalpha():
                    char2Freq[getCharTransfInd(charec,last2Char)] += 1
                    last2Char = last1Char
                    last1Char = charec
            if not initWord:
                charInitFreq[getNewCharIndex(charec.lower())] += 1
                initWord = True
                last1Char = charec
            if not initWord2 and initWord:
                charInit2Freq[getNewCharIndex(charec.lower())] += 1
                initWord2 = True
                last2Char = last1Char
                last1Char = charec

    # word frequency data
    if word not in wordFreq:
        wordFreq[word.lower()] = 0
    else:
        wordFreq[word.lower()] += 1
    # word length frequency data
    wordLenFreq[len(word)] += 1
    lastWord = word

# Mark Twain - Huck Finn / Tom Sawyer
loadAndAnalyze("./trainBasic.txt")