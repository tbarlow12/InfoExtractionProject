import sys

POSCON = 1
LEXCON = 2
featureIds = {}


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







def getLineVector(featureIds,instance,index,mode):
    line = instance[index]
    vector = []
    bioLabel = getBioLabel(line[0])
    vector.append(bioLabel)
    features = []
    addWordFeature(featureIds,features,line[2])
    if(mode > 0):
        addWordCapFeature(featureIds,features,line[2])
    if(mode == 2 or mode == 4):
        addConFeature(featureIds,features,instance,index,POSCON)
    if(mode == 3 or mode == 4):
        addConFeature(featureIds,features,instance,index,LEXCON)
    addFeaturesToVector(vector,features)
    return vector
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

def addFeaturesToVector(vector,features):
    features.sort()
    for f in features:
        vector.append(str(f) + ':1')

def wordFeatureIds(instance):
    addWordsToFeatureIds(featureIds,instance,False)
    return featureIds

def wordFeatureVector(instance):
    featureIds = wordFeatureIds(instance)
    vector = []
    index = 0
    while(index < len(instance)):
        v = getLineVector(featureIds,instance,index,0)
        vector.append(v)
        index += 1
    return vector
def wordCapFeatureIds(instance):
    addWordsToFeatureIds(featureIds,instance,False)
    addToDictionarySizeValue(featureIds,'capitalized')
    return featureIds
def wordCapFeatureVector(instance):
    featureIds = wordCapFeatureIds(instance)
    vector = []
    index = 0
    while(index < len(instance)):
        v = getLineVector(featureIds,instance,index,1)
        vector.append(v)
        index += 1
    return vector
def posconFeatureVector(instance):
    featureIds = posconFeatureIds(instance)
    vector = []
    index = 0
    while(index < len(instance)):
        v = getLineVector(featureIds,instance,index,2)
        vector.append(v)
        index += 1
    return vector
def posconFeatureIds(instance):
    #True if you want prev and next
    addPosToFeatureIds(featureIds,instance)
    addToDictionarySizeValue(featureIds,'capitalized')
    return featureIds

def lexconFeatureIds(instance):
    #True if you want prev and next
    addWordsToFeatureIds(featureIds,instance,True)
    addToDictionarySizeValue(featureIds,'capitalized')
    return featureIds

def lexconFeatureVector(instance):
    featureIds = lexconFeatureIds(instance)
    vector = []
    index = 0
    while(index < len(instance)):
        v = getLineVector(featureIds,instance,index,3)
        vector.append(v)
        index += 1
    return vector

def bothconFeatureIds(instance):
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
    if(fType == 'word'):
        return wordFeatureVector(instance)
    elif(fType == 'wordcap'):
        return wordCapFeatureVector(instance)
    elif(fType == 'poscon'):
        return posconFeatureVector(instance)
    elif(fType == 'lexcon'):
        return lexconFeatureVector(instance)
    elif(fType == 'bothcon'):
        return bothconFeatureVector(instance)

def processInstances(instances,fType):
    results = []
    for instance in instances:
        v = createFeatureVector(instance,fType)
        results.append(v)
    return results

def process(data,fType):
    instances = readFile(data)
    return processInstances(instances,fType)

def getString(result):
    finalString = ''
    for i in result:
        for j in i:
            line = ''
            for k in j:
                line += str(k) + ' '
            line = line[:-1]
            finalString += line + '\n'
    return finalString

def main():
    trainingData = sys.argv[1].strip()
    testData = sys.argv[2].strip()
    fType = sys.argv[3].strip()
    trainResult = process(trainingData,fType)
    testResult = process(testData,fType)

    print
    print getString(testResult)


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
