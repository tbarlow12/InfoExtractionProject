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
        splitInstances.append(tups)
    return splitInstances

def test(testData):
    tups = readFile(testData)


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

def wordFeatureVector(instance):
    vector = []
    vector.append(instance[0])
    #return vector
def wordCapFeatureVector(instance):
    vector = []
    return vector
def posconFeatureVector(instance):
    vector = []
    return vector
def lexconFeatureVector(instance):
    vector = []
    return vector


def addToDictionary(d,s):
    if(s not in d):
        d[s] = len(d) + 1
        print s + ': ' + str(d[s])

def bothconFeatureVector(instance):
    featureIds = {}
    for line in instance:
        word = line[2]
        curr = 'curr-' + word
        prev = 'prev-' + word
        next = 'next-' + word
        addToDictionary(featureIds,curr)
        addToDictionary(featureIds,prev)
        addToDictionary(featureIds,next)


    vector = []



    return vector


def createFeatureVector(instance,fType):
    return {
        'word': wordFeatureVector(instance),
        'wordcap': wordCapFeatureVector(instance),
        'poscon': posconFeatureVector(instance),
        'lexcon': lexconFeatureVector(instance),
        'bothcon': bothconFeatureVector(instance)
    }[fType]


def processTrainingInstances(instances,fType):
    for instance in instances:
        v = createFeatureVector(instance,fType)



            #print t
            #print '\n'
            #bios.add(t[0])
            #tags.add(t[1])
            #words.add(t[2])

def createAllFeatureVectors(fType):
    for word in words:
        createFeatureVectors(word,fType)

def train(trainingData,fType):
    trainingInstances = readFile(trainingData)
    processTrainingInstances(trainingInstances,fType)
    createAllFeatureVectors(fType)

def main():
    trainingData = sys.argv[1].strip()
    testData = sys.argv[2].strip()
    fType = sys.argv[3].strip()
    train(trainingData,fType)

    trainOutput = trainingData + '.' + fType
    testOutput = testData + '.' + fType


if __name__ == '__main__':
    main()
