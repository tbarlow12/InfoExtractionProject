import sys

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

def addPosToFeatureIds(featureIds,instance):
    for line in instance:
        addTwoToDictionary(featureIds,line[1])
    addTwoToDictionary(featureIds,'PHIPOS')
    addTwoToDictionary(featureIds,'OMEGAPOS')
    addTwoToDictionary(featureIds,'UNKPOS')

def addWordsToFeatureIds(featureIds,instance,includeBorders):
    for line in instance:
        if(includeBorders):
            addAllThreeToDictionary(featureIds,line[2])
        else:
            addToDictionarySizeValue(featureIds,'curr-' + line[2])
    if(includeBorders):
        addAllThreeToDictionary(featureIds,'PHI')
        addAllThreeToDictionary(featureIds,'OMEGA')
        addAllThreeToDictionary(featureIds,'UNKWORD')
    else:
        addToDictionarySizeValue(featureIds,'curr-PHI')
        addToDictionarySizeValue(featureIds,'curr-OMEGA')
        addToDictionarySizeValue(featureIds,'curr-UNKWORD')


def addWordFeature(featureIds,features,word):
    key = 'curr-' + word
    if(key in featureIds):
        features.append(featureIds[key])

def addWordCapFeature(featureIds,features,word):
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

def getLineVector(featureIds,instance,index,mode):
    line = instance[index]

    vector = []
    bioLabel = getBioLabel(line[0])
    vector.append(bioLabel)

    features = []
    addWordFeature(featureIds,features,line[2])
    if(mode > 1):
        addWordCapFeature(featureIds,features,line[2])
    if(mode == 2 or mode == 4):
        addConFeature(featureIds,features,instance,index,POSCON)
    if(mode == 3 or mode == 4):
        addConFeature(featureIds,features,instance,index,LEXCON)

    addFeaturesToVector(vector,features)

def addConFeature(featureIds,features,instance,index,posLex):
    addPrevious(featureIds,features,instance,index,posLex)
    addNext(featureIds,features,instance,index,posLex)

def addFeaturesToVector(vector,features):
    features.sort()
    for f in features:
        vector.append(str(f) + ':1')

def wordFeatureIds(instance):
    featureIds = {}
    addWordsToFeatureIds(featureIds,instance,True)
def wordFeatureVector(instance):
    featureIds = wordFeatureIds(instance)
    vector = []
    index = 0
    while(index < len(instance)):
        v = getLineVector(featureIds,instance,index,0)
        vector.append(v)
        index += 1
    return vector

def wordCapFeatureVector(instance):
    vector = []
    return vector
def posconFeatureVector(instance):
    vector = []
    return vector
def lexconLineVector(featureIds,instance,index):
    line = instance[index]

    vector = []
    bioLabel = getBioLabel(line[0])
    vector.append(bioLabel)

    features = []

    addWordFeature(featureIds,features,line[2])
    addWordCapFeature(featureIds,features,line[2])
    addConFeature(featureIds,features,instance,index,LEXCON)

    addFeaturesToVector(vector,features)

    return vector
def lexconFeatureVector(instance):
    vector = []
    return vector
def bothconLineVector(featureIds,instance,index):
    line = instance[index]

    vector = []
    bioLabel = getBioLabel(line[0])
    vector.append(bioLabel)

    features = []

    addWordFeature(featureIds,features,line[2])
    addWordCapFeature(featureIds,features,line[2])
    addConFeature(featureIds,features,instance,index,POSCON)
    addConFeature(featureIds,features,instance,index,LEXCON)

    addFeaturesToVector(vector,features)

    return vector
def bothconFeatureIds(instance):
    featureIds = {}
    #True if you want prev and next
    addWordsToFeatureIds(featureIds,instance,True)
    addPosToFeatureIds(featureIds,instance)
    addToDictionarySizeValue(featureIds,'capitalized')

    return featureIds
def bothconFeatureVector(instance):
    featureIds = bothconFeatureIds(instance)
    vector = []
    index = 0
    while(index < len(instance)):
        v = getLineVector(featureIds,instance,index,4)
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

def train(trainingData,fType):
    trainingInstances = readFile(trainingData)
    processTrainingInstances(trainingInstances,fType)

def main():
    trainingData = sys.argv[1].strip()
    testData = sys.argv[2].strip()
    fType = sys.argv[3].strip()
    train(trainingData,fType)

    trainOutput = trainingData + '.' + fType
    testOutput = testData + '.' + fType


if __name__ == '__main__':
    main()
