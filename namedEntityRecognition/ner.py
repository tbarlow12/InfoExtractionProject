import sys

bios = set()
words = set()
tags = set()

def readFile(path):
    with open(path) as f:
        text = f.read()
    sentences = text.strip().split("\n\n")
    instances = [s.strip().split("\n") for s in sentences]
    splitInstances = []
    for i in instances:
        tups = [x.strip().split() for x in i]
        if(len(tups) > 0):
            splitInstances.append(tups)
    for s in splitInstances:
        print 'split instance:'
        print s
    return splitInstances

def test(testData):
    tups = readFile(testData)

def findWordsAndTags(tups):
    for t in tups:
        if(len(t) > 0):
            bios.add(t[0])
            tags.add(t[1])
            words.add(t[2])


def wordFeatureVector(word):
    return 0
def wordCapFeatureVector(word):
    return 0
def posconFeatureVector(word):
    return 0
def lexconFeatureVector(word):
    return 0
def bothconFeatureVector(word):
    return 0


def createFeatureVectors(word,fType):
    return {
        'word': wordFeatureVector(word),
        'wordcap': wordCapFeatureVector(word),
        'poscon': posconFeatureVector(word),
        'lexcon': lexconFeatureVector(word),
        'bothcon': bothconFeatureVector(word)
    }[fType]

def createAllFeatureVectors(fType):
    for word in words:
        createFeatureVectors(word,fType)

def train(trainingData,fType):
    trainingInstances = readFile(trainingData)
    findWordsAndTags(trainingInstances)
    createAllFeatureVectors(fType)
    print bios
    print len(words)

def main():
    trainingData = sys.argv[1].strip()
    testData = sys.argv[2].strip()
    fType = sys.argv[3].strip()
    train(trainingData,fType)

    trainOutput = trainingData + '.' + fType
    testOutput = testData + '.' + fType


if __name__ == '__main__':
    main()
