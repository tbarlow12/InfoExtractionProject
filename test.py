from questionAnswering import answerer as qa
from helpers import helpers as h

root = 'datasets/'
trainRoot = root + 'train/'
testRoot = root + 'test/'
answerer = qa.answerer(root)

def testAnswerer(setRoot):
    answerSet = h.getAnswerSet(setRoot)
    correct = 0
    asked = 0
    for item in answerSet:
        if len(item) == 6:
            asked += 1
            title = item[0]
            question = h.get_encoded(item[1])
            expected_answer = item[2]
            questionDiff = item[3]
            answerDiff = item[4]
            articleFile = setRoot[-3:] + '/' + item[5]
            actual_answer = answerer.answerQuestion(question,articleFile)
            if actual_answer.lower() == expected_answer.lower():
                correct += 1
            else:
                print(question)
    return float(correct) / float(asked)
print testAnswerer(trainRoot + 'S08')
print testAnswerer(trainRoot + 'S09')
#print testAnswerer(testRoot + 'S10')


