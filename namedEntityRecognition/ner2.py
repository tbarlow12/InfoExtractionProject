import sys
import operator
words = []
tags = []
featureIds = {}
WORD = 0
WORDCAP = 1
POSCON = 2
LEXCON = 3
BOTHCON = 4
def getBioLabel(bio):
    return {
        'O': 0,
        'B-PER': 1,
        'I-PER': 2,
        'B-LOC': 3,
        'I-LOC': 4,
        'B-ORG': 5,
        'I-ORG': 6
    }[bio]
def getMode(fType):
    return {
        'word': WORD,
        'wordcap': WORDCAP,
        'poscon': POSCON,
        'lexcon': LEXCON,
        'bothcon': BOTHCON
    }[fType]
def readFile(path):
    with open(path) as f:
        text = f.read()
    sentences = text.strip().split("\n\n")
    instances = [s.strip().split("\n") for s in sentences]
    splitInstances = []
    for i in instances:
        tups = [x.strip().split() for x in i]
        splitInstances.append(tups)
    return splitInstances
def printSortedFeatureIds():
    sorted_x = sorted(featureIds.items(), key=operator.itemgetter(1))
    for i in sorted_x:
        print str(i[1]) + '\t' + i[0]
def getUniqueWordsTags(sentences,mode,training):
    for sentence in sentences:
        for line in sentence:
            if line[2] not in words:
                words.append(line[2])
            if line[1] not in tags:
                tags.append(line[1])
    if(training):
        print 'Found ' + str(len(sentences)) + ' training instances with ' + str(len(words)) + ' distinct words and ' + str(len(tags)) + ' distinct POS tags'
    else:
        print 'Found ' + str(len(sentences)) + ' test instances'

    for word in words:
        addToDictionarySizeValue('curr-' + word)
        if(mode > POSCON):
            addToDictionarySizeValue('prev-' + word)
            addToDictionarySizeValue('next-' + word)
    addToDictionarySizeValue('curr-PHI')
    if(mode > POSCON):
        addToDictionarySizeValue('prev-PHI')
        addToDictionarySizeValue('next-PHI')
    addToDictionarySizeValue('curr-OMEGA')
    if(mode > POSCON):
        addToDictionarySizeValue('prev-OMEGA')
        addToDictionarySizeValue('next-OMEGA')
    addToDictionarySizeValue('curr-UNKWORD')
    if(mode > POSCON):
        addToDictionarySizeValue('prev-UNKWORD')
        addToDictionarySizeValue('next-UNKWORD')
    if(mode == POSCON or mode == BOTHCON):
        for tag in tags:
            addToDictionarySizeValue('prev-' + tag)
            addToDictionarySizeValue('next-' + tag)
        addToDictionarySizeValue('prev-PHIPOS')
        addToDictionarySizeValue('next-PHIPOS')
        addToDictionarySizeValue('prev-OMEGAPOS')
        addToDictionarySizeValue('next-OMEGAPOS')
        addToDictionarySizeValue('prev-UNKPOS')
        addToDictionarySizeValue('next-UNKPOS')
    if(mode > WORD):
        addToDictionarySizeValue('capitalized')

def addToDictionarySizeValue(s):
    if(s not in featureIds):
        featureIds[s] = len(featureIds) + 1
def process(data,fType,training):
    sentences = readFile(data)
    mode = getMode(fType)
    getUniqueWordsTags(sentences,mode,training)
    allFeatureVectors = []
    for sentence in sentences:
        allFeatureVectors.append(processSentence(sentence,mode))
    return allFeatureVectors

def addFeature(features,key,default):
    if key in featureIds:
        features.append(featureIds[key])
    else:
        features.append(featureIds[default])

def processSentence(sentence,mode):
    i = 0
    featureVector = []
    while i < len(sentence):
        line = sentence[i]
        word = line[2]
        tag = line[1]
        bio = getBioLabel(line[0])
        lineVector = []
        lineVector.append(bio)
        features = []
        key = 'curr-' + word
        if key in featureIds:
            wordId = featureIds[key]
        else:
            wordId = featureIds['curr-UNKWORD']
        features.append(wordId)
        if(mode > WORD):
            if word[0].isupper():
                features.append(featureIds['capitalized'])
        if(mode > WORDCAP):
            if(i > 0):
                prevLine = sentence[i-1]
                prevWord = prevLine[2]
                prevPos = prevLine[1]
            else:
                prevWord = 'PHI'
                prevPos = 'PHIPOS'
            if(i < (len(sentence) - 1)):
                nextLine = sentence[i+1]
                nextWord = nextLine[2]
                nextPos = nextLine[1]
            else:
                nextWord = 'OMEGA'
                nextPos = 'OMEGAPOS'
            if mode == POSCON or mode == BOTHCON:
                addFeature(features,'prev-'+prevPos,'prev-UNKPOS')
                addFeature(features,'next-'+nextPos,'next-UNKPOS')
            if mode == LEXCON or mode == BOTHCON:
                addFeature(features,'prev-'+prevWord,'prev-UNKWORD')
                addFeature(features,'next-'+nextWord,'next-UNKWORD')
        features.sort()
        for feature in features:
            lineVector.append(str(feature) + ':1')
        featureVector.append(lineVector)
        i += 1
    return featureVector
def getString(result):
    finalString = ''
    for i in result:
        for j in i:
            line = ''
            for k in j:
                line += str(k) + ' '
            line = line[:-1]
            finalString += line + '\n'
    return finalString[:-1]
def main():
    trainingData = sys.argv[1].strip()
    testData = sys.argv[2].strip()
    fType = sys.argv[3].strip()
    trainResult = process(trainingData,fType,True)
    testResult = process(testData,fType,False)
    trainOutputFile = trainingData + '.' + fType
    testOutputFile = testData + '.' + fType

    text_file = open(trainOutputFile, "w")
    text_file.write(getString(trainResult))
    text_file.close()

    text_file = open(testOutputFile, "w")
    text_file.write(getString(testResult))
    text_file.close()
if __name__ == '__main__':
    main()
