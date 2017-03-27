print 'Importing modules'
import io
from questionAnswering import answerer as qa
from helpers import helpers as h

root = 'datasets/'
trainRoot = root + 'train/'
first_train = trainRoot + 'S08/'
second_train = trainRoot + 'S09/'
testRoot = root + 'test/'

def write_answer_set(name, question_set, list_type):
    with io.open('{}_{}.txt'.format(name,list_type),'w',encoding='utf-8') as f:
        for q in question_set:
            try:
                s = u''.join(q[0] + u'\n')
                f.write(s)
            except UnicodeDecodeError:
                print 'Could not decode'
            try:
                s = (u'EXPECTED: ' + u''.join(q[1]) + u'\t' + u'ACTUAL: ' + u''.join(q[2]) + u'\n\n')
                f.write(s)
            except UnicodeEncodeError:
                print 'Could not encode'


def testAnswerer(answerer, setRoot, debug):
    answerSet = h.getAnswerSet(setRoot)
    correct = 0
    asked = 0
    missed_questions = []
    right_questions = []
    for item in answerSet:
        if len(item) == 6:
            asked += 1
            title = item[0]
            question = u''.join(item[1])
            expected_answer = u''.join(item[2])
            questionDiff = u''.join(item[3])
            answerDiff = u''.join(item[4])
            articleFile = u''.join(setRoot[-3:]) + u'/' + u''.join(item[5])
            actual_answer = answerer.answerQuestion(question,articleFile)
            if actual_answer.lower() == expected_answer.lower():
                correct += 1
                right_questions.append([question,expected_answer,actual_answer])
            else:
                missed_questions.append([question,expected_answer,actual_answer])
    if debug:
        write_answer_set(setRoot[-3:], missed_questions,'missed')
        write_answer_set(setRoot[-3:], right_questions, 'correct')
    return float(correct) / float(asked)


def test_training_data():
    print 'Initializing Answerer'
    answerer = qa.answerer(trainRoot)
    print 'Answerer Initialized'
    print testAnswerer(answerer,trainRoot + 'S08',True)
    print testAnswerer(answerer,trainRoot + 'S09',True)

def test_data():
    print 'Initializing Answerer'
    answerer = qa.answerer(testRoot)
    print 'Answerer Initialized'
    print testAnswerer(answerer,testRoot + 'S10',False)

def main():
    
    test_training_data()
    #test_data()


if __name__ == '__main__':
    main()
