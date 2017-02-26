from questionAnswering import answerer as qa
from helpers import helpers as h
root = 'datasets/'
trainRoot = root + 'train/'
testRoot = root + 'test/'
def testAnswerer(answerSet):
    correct = 0
    asked = 0
    for set in answerSet:
        for item in set:
            if len(item) == 6:
                asked += 1
                title = item[0]
                question = item[1]
                answer = item[2]
                questionDiff = item[3]
                answerDiff = item[4]
                articleFile = item[5]
                if a.answerQuestion(question).lower() == answer.lower():
                    correct += 1
    return float(correct) / float(asked)

a = qa.answerer(trainRoot)

trainAnswerSet = h.getAnswerSet(trainRoot)
testAnswerSet = h.getAnswerSet(testRoot)

print(testAnswerer(trainAnswerSet))
print(testAnswerer(testAnswerSet))

