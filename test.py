import io
from questionAnswering import answerer as qa
from helpers import helpers as h

root = 'datasets/'
trainRoot = root + 'train/'
testRoot = root + 'test/'
answerer = qa.answerer(root)


def write_missed(missed_questions):
    with io.open('missed_questions.txt','wb') as f:
        for q in missed_questions:
            try:
                f.write(q[0] + '\n')
            except UnicodeDecodeError:
                print 'Could not decode'
            try:
                s = ('EXPECTED: ' + q[1] + '\t' + 'ACTUAL: ' + q[2] + '\n\n').encode('utf-8')
                f.write(s)
            except UnicodeEncodeError:
                print 'Could not encode'


def testAnswerer(setRoot):
    answerSet = h.getAnswerSet(setRoot)
    correct = 0
    asked = 0
    missed_questions = []
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
                missed_questions.append([question,expected_answer,actual_answer])
            write_missed(missed_questions)
    return float(correct) / float(asked)
print testAnswerer(trainRoot + 'S08')
print testAnswerer(trainRoot + 'S09')
#print testAnswerer(testRoot + 'S10')


