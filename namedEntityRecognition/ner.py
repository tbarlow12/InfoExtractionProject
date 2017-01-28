import sys

bios = set()
words = set()
tags = set()

def readFile(path):
    with open(path) as f:
        lines = f.readlines()
    tups = [x.strip().split() for x in lines]
    return tups

def test(testData):
    tups = readFile(testData)

def findWordsAndTags(tups):
    for t in tups:
        if(len(t) > 0):
            bios.add(t[0])
            tags.add(t[1])
            words.add(t[2])


def wordFeatureType(word):
    return 0
def wordCapFeatureType(word):
    return 0
def posconFeatureType(word):
    return 0
def lexconFeatureType(word):
    return 0
def bothconFeatureType(word):
    return 0


def createFeatureTypes(word,fType):
    return {
        'word': wordFeatureType(word),
        'wordcap': wordCapFeatureType(word),
        'poscon': posconFeatureType(word),
        'lexcon': lexconFeatureType(word),
        'bothcon': bothconFeatureType(word)
    }[fType]

def createAllFeatureTypes(fType):
    for word in words:
        createFeatureTypes(word,fType)

def train(trainingData,fType):
    tups = readFile(trainingData)
    findWordsAndTags(tups)
    createAllFeatureTypes(fType)
    print bios
    print len(words)

def main():
    trainingData = sys.argv[1]
    testData = sys.argv[2]
    fType = sys.argv[3]

    train(trainingData,fType)


if __name__ == '__main__':
    main()
