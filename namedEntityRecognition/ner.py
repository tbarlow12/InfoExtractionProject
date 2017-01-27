import sys

words = []
tags = []

def readFile(path):
    with open(path) as f:
        lines = f.readlines()
    tups = [x.strip().split() for x in lines]
    return tups

def test(testData):
    tups = readFile(testData)


def train(trainingData):
    tups = readFile(trainingData)
    for t in tups:
        if(len(t) > 0):
            other = t[0]
            tag = t[1]
            if (tag not in tags):
                tags.append(tag)
            word = t[2]
            if(word not in words):
                words.append(word)
    print len(words)
    print len(tags)


def main():
    trainingData = sys.argv[1]
    train(trainingData)
    testData = sys.argv[2]
    fType = sys.argv[3]

if __name__ == '__main__':
    main()
