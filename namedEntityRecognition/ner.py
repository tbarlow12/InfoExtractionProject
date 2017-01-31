import sys

bios = set()
words = set()
tags = set()

POSCON = 1
LEXCON = 2

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

def getIsCap(word):
    return word[0].isupper()

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


def addToDictionarySizeValue(d,s):
    if(s not in d):
        d[s] = len(d) + 1

def addAllThreeToDictionary(d,s):
    curr = 'curr-' + s
    prev = 'prev-' + s
    next = 'next-' + s
    addToDictionarySizeValue(d,curr)
    addToDictionarySizeValue(d,prev)
    addToDictionarySizeValue(d,next)

def addTwoToDictionary(d,s):
    prev = 'prev-' + s
    next = 'next-' + s
    addToDictionarySizeValue(d,prev)
    addToDictionarySizeValue(d,next)

def bothconFeatureIds(instance):
    featureIds = {}
    for line in instance:
        addAllThreeToDictionary(featureIds,line[2])

    addAllThreeToDictionary(featureIds,'PHI')
    addAllThreeToDictionary(featureIds,'OMEGA')
    addAllThreeToDictionary(featureIds,'UNKWORD')

    for line in instance:
        addTwoToDictionary(featureIds,line[1])

    addTwoToDictionary(featureIds,'PHIPOS')
    addTwoToDictionary(featureIds,'OMEGAPOS')
    addTwoToDictionary(featureIds,'UNKPOS')

    addToDictionarySizeValue(featureIds,'capitalized')

    return featureIds

def addWordFeature(featureIds,features,word):
    key = 'curr-' + word
    if(key in featureIds):
        features.append(featureIds[key])

def addCapFeature(featureIds,features,word):
    if(getIsCap(word)):
        capFeatureId = featureIds['capitalized']
        features.append(capFeatureId)

def addFeature(featureIds,features,posLex,prefix,word):
    key = prefix + word
    if key in featureIds:
        featureId = featureIds[key]
    elif (posLex == POSCON):
        featureId = featureIds[prefix + 'UNKPOS']
    else:
        featureId = featureIds[prefix + 'UNKWORD']
    if(featureId not in features):
        features.append(featureId)

def addNext(featureIds,features,instance,index,posLex):

        if(index < len(instance) - 1):
            next = instance[index+1][posLex]
        elif (posLex == POSCON):
            next = 'OMEGAPOS'
        else:
            next = 'OMEGA'

        addFeature(featureIds,features,posLex,'next-',next)

def addPrevious(featureIds,features,instance,index,posLex):
    line = instance[index]

    if(index > 0):
        prev = instance[index-1][posLex]
    elif (posLex == POSCON):
        prev = 'PHIPOS'
    else:
        prev = 'PHI'

    addFeature(featureIds,features,posLex,'prev-',prev)


def addConFeature(featureIds,features,instance,index,posLex):
    addPrevious(featureIds,features,instance,index,posLex)
    addNext(featureIds,features,instance,index,posLex)


def bothconLineVector(featureIds,instance,index):
    line = instance[index]

    vector = []
    tag = line[1]
    word = line[2]

    bioLabel = getBioLabel(line[0])
    vector.append(bioLabel)

    features = []
    addWordFeature(featureIds,features,word)
    addCapFeature(featureIds,features,word)
    addConFeature(featureIds,features,instance,index,POSCON)
    addConFeature(featureIds,features,instance,index,LEXCON)

    features.sort()
    vector.extend(features)





    return vector



def bothconFeatureVector(instance):
    featureIds = bothconFeatureIds(instance)
    vector = []
    index = 0
    while(index < len(instance)):
        v = bothconLineVector(featureIds,instance,index)
        print v
        vector.append(v)

        index += 1

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
