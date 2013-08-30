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

def analyzeTextAlphaNum(text):
    textSpl = text.split()

    maxSenLen = 500
    maxWordLen = 100
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

    minAnalyzedSenCharSize = 300
    currentSentence = "";

    # save data
    saveDir = "./Result/"

    for word in textSpl:
        word.lower()
        currentSentence += word
        #sentence length data
        if isSentenceEnd(word):
            if ( (lastSenLen > 0) and ((wordIndex -lastWordIndex) < maxSenLen) and (lastSenLen < maxSenLen) ):
                #print "last senLen| ",lastSenLen,"    curr| ",(wordIndex -lastWordIndex),"    word| ",word
                senLen1Freq[lastSenLen+maxSenLen*((wordIndex -lastWordIndex))] += 1
                if len(currentSentence) > minAnalyzedSenCharSize:
                    #print "sen ",currentSentence
                    # sentence level character frequency
                    # useful to get standard deviation in probability of char frequency
                    # given a sentence length range
                    [senChar, senChar2] = analyzeLineCharLowered2Gram(currentSentence)
                    saveListAppend(senChar,saveDir+"sentenceCharFreq.txt")
                    saveListAppend(senChar2,saveDir+"sentenceChar2Freq.txt")
                    currentSentence = ""
            if ((wordIndex -lastWordIndex) < maxSenLen):
                senLenFreq[(wordIndex -lastWordIndex)] += 1
            lastSenLen = (wordIndex -lastWordIndex)
            lastWordIndex = wordIndex

        wordIndex += 1
        # characters in word data
        analyzeWordAlphaNum(word,charFreq,charInitFreq,charInit2Freq,charLowFreq,char1Freq,char2Freq,wordFreq,wordLenFreq)
        # word length data
        if ( lastWordLen > 0 and maxWordLen > len(re.sub('[\W_]+', '', word)) and lastWordLen < maxWordLen ):
            wordLen1Freq[lastWordLen+maxWordLen*(len(re.sub('[\W_]+', '', word)))] += 1
        lastWordLen = len(re.sub('[\W_]+', '', word))

    #normalize
    normalizeList(charFreq)
    normalizeList(charInitFreq)
    normalizeList(charInit2Freq)
    normalizeList(char1Freq)
    normalizeList(char2Freq)
    normalizeList(charLowFreq)

    # save whole text data
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

def analyzeLineCharLowered2Gram(text):
    textSpl = text.split()
    global alphabetSize

    # initialize list of frequencies
    charFreq = [0 for x in range(alphabetSize+alphabetSize+10)]
    char1Freq = [0 for x in range(alphabetSize*alphabetSize)]

    for word in textSpl:
        # characters in word data
        analyzeWord2GramAlphaNum(word.lower(),charFreq,char1Freq)

    normalizeList(charFreq)
    normalizeList(char1Freq)
    return [charFreq,char1Freq]


def normalizeList(lin):
    sum = 0.0
    for x in lin:
        sum += float(x)
    ind = 0
    for x in lin:
        val = (x/sum)
        lin[ind] = float(val)
        ind += 1
    return lin

def saveList(newList, fileName):
    thefile = open(fileName, 'w')
    for item in newList:
        thefile.write("%s\n" % item)
    thefile.close()

def saveListAppend(newList, fileName):
    try:
        with open(fileName): pass
    except IOError:
        print 'Need to make new file.'
        file = open(fileName, 'w')
        file.write('')
        file.close()

    thefile = open(fileName, 'a+')

    for item in newList:
        thefile.write("%s  " % item)
    thefile.write("\n")
    thefile.close()

def saveListChar(newList, fileName):
    thefile = open(fileName, 'w')
    indexIn = 0
    for item in newList:
        if item is not 0:
            thefile.write("%s , %s \n" % (item, getNewCharFromIndex(indexIn)) )
        indexIn += 1
    thefile.close()

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
def loadAndAnalyzeAlphaNum(fileName):
	f = open(fileName, 'r')
	fileStr = f.read()
	return analyzeTextAlphaNum(fileStr)

# load a file and process it
def loadAndAnalyzeAscii(fileName):
	f = open(fileName, 'r')
	fileStr = f.read()
	return analyzeTextAsciiNoSpaces(fileStr)

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
def analyzeWordAlphaNum(wordIn, charFreq,charInitFreq,charInit2Freq,charLowFreq, char1Freq, char2Freq, wordFreq, wordLenFreq):
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
    if len(word) < 100:
        wordLenFreq[len(word)] += 1
    lastWord = word

def getRemappedAscii( charMapping, charIn ):
    ind = 0
    pos = 0
    for charMapped in charMapping:
        if charIn is charMapped:
           pos = ind
        ind += 1
    return pos

def makeAsciiMap( text ):
    present = [0 for x in range(255)]
    map = []
    for charIn in text:
        if( (ord(charIn) is not ord("\n"))  ):
            present[ord(charIn)] += 1
    ind = 0
    for count in present:
        if count is not 0:
            map.append(chr(ind))
        ind += 1
    return map

# analyze a word for data to be taken
def analyzeWordAscii(wordIn, charFreq,char1Freq, mapAscii):
    last1Char = None
    # character frequency analysis
    for charec in wordIn:
        #print type(charec)
        charFreq[getRemappedAscii(mapAscii,charec)] += 1
        if last1Char is not None:
            char1Freq[getRemappedAscii(mapAscii,charec)+len(mapAscii)*getRemappedAscii(mapAscii,last1Char)] += 1
        last1Char = charec

# analyze a word for data to be taken
def analyzeWord2GramAlphaNum(wordIn, charFreq, char1Freq):
    # strip the word to alphanum
    word  = re.sub('[\W_]+', '', wordIn)
    last1Char = None
    # character frequency analysis
    for charec in word:
        #print type(charec)
        if charec.isalpha():
            #print "char | ",charec
            charFreq[getNewCharIndex(charec.lower())] += 1
            if last1Char is not None :
                if (last1Char.isalpha()):
                    char1Freq[getCharTransfInd(charec,last1Char)] += 1
            last1Char = charec


def analyzeTextAsciiNoSpaces(text):
    textSpl = text.split()

    #determine found ascii
    alphabetSize = 26

    # initialize list of frequencies
    charFreq = [0 for x in range(alphabetSize)]
    char1Freq = [0 for x in range(alphabetSize*alphabetSize)]

    # save data
    saveDir = "./ResultAscii/"
    map = makeAsciiMap(text)
    print len(map)

    charFreq = [0 for x in range(len(map))]
    char1Freq = [0 for x in range(len(map)*len(map))]
    for word in textSpl:
        analyzeWordAscii(word,charFreq,char1Freq,map)
    #normalize
    normalizeList(charFreq)
    normalizeList(char1Freq)

    prefix= "AllTrain-"
    # save whole text data
    saveList(charFreq,saveDir+prefix+"charFreqSumAscii.txt")
    saveList(char1Freq,saveDir+prefix+"char1FreqSumAscii.txt")
    saveList(map,saveDir+prefix+"mapAscii.txt")
    return [charFreq,char1Freq]


# Mark Twain - Huck Finn / Tom Sawyer is what I used. Not exactly english.
loadAndAnalyzeAlphaNum("./trainBasic.txt")
