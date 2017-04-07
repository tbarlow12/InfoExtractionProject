print 'Importing modules'
import io
import sys
import string
from questionAnswering import answerer as qa
from helpers import helpers as h
import pdb

debug = False

if len(sys.argv) > 2 and sys.argv[2] == '-d':
    debug = True

root = 'datasets/'
trainRoot = root + 'train/'
first_train = trainRoot + 'S08/'
second_train = trainRoot + 'S09/'
testRoot = root + 'test/'

def write_answer_set(name, question_set, list_type):
    with io.open('debug/{}_{}.txt'.format(name,list_type),'w',encoding='utf-8') as f:
        for q in question_set:
            try:
                s = u''.join(q[0] + u'\t' + q[1] + u'\t' + q[2] + u'\n\n' + q[3] + u'\n\n')
                f.write(s)
            except UnicodeDecodeError:
                print 'Could not decode'
exclude = set(string.punctuation)
def normalize(s):
    s = s.lower()
    s = ''.join(ch for ch in s if ch not in exclude)
    return s


def testAnswerer(answerer, setRoot, debug, non_null):
    if non_null:
        answerSet = h.getAnswerSet_non_null(setRoot)
        correct = 0
        asked = 0
        missed_questions = []
        right_questions = []
        for question in answerSet:
            asked += 1
            expected_answer = answerSet[question][0]
            articleFile = answerSet[question][1]
            actual_answer = answerer.answerQuestion(question,articleFile)
            if normalize(actual_answer) == normalize(expected_answer):
                correct += 1
                right_questions.append([question,expected_answer,articleFile,actual_answer])
            else:
                missed_questions.append([question,expected_answer,articleFile,actual_answer])
        if debug:
            write_answer_set(setRoot[-3:], missed_questions,'missed-non-null')
            write_answer_set(setRoot[-3:], right_questions, 'correct-non-null')
        return float(correct) / float(asked)
    else:
        answerSet = h.getAnswerSet_all(setRoot)
        correct = 0
        asked = 0
        missed_questions = []
        right_questions = []
        for item in answerSet:
            asked += 1
            question = item[0]
            expected_answer = item[1]
            articleFile = item[2]
            actual_answer = answerer.answerQuestion(question,articleFile)
            if normalize(actual_answer) == normalize(expected_answer):
                correct += 1
                right_questions.append([question,expected_answer,articleFile,actual_answer])
            else:
                missed_questions.append([question,expected_answer,articleFile,actual_answer])
        if debug:
            write_answer_set(setRoot[-3:], missed_questions,'missed-all')
            write_answer_set(setRoot[-3:], right_questions, 'correct-all')
        return float(correct) / float(asked)



def test_missed():
    correct = 0
    asked = 0
    print 'Testing Missed Questions'
    print 'Initializing Answerer'
    answerer = qa.answerer(trainRoot)
    print 'Answerer Initialized'
    missed_questions = []
    right_questions = []
    missed_files = ['S08_missed.txt','S09_missed.txt']
    for missed_file in missed_files:
        with io.open(missed_file,encoding='latin-1') as f:
            lines = f.readlines()
            for line in lines:
                asked += 1
                line = u''.join(line)
                parts = line.split('\t')
                question = parts[0]
                expected = parts[1]
                path = parts[2]
                previous_answer = parts[3]
                new_answer = answerer.answerQuestion(question,path)
                if new_answer.lower() == expected.lower():
                    correct += 1
                    right_questions.append([question,expected,path,new_answer])
                else:
                    missed_questions.append([question,expected,path,new_answer])
                if debug:
                    raw_input('\nPress Enter to continue')
            write_answer_set(missed_file[:3], missed_questions,'missed')
            write_answer_set(missed_file[:3], right_questions, 'correct')
    return float(correct) / float(asked)


def test_training_data():
    print 'Testing Training Data'
    print 'Initializing Answerer'
    answerer = qa.answerer(trainRoot)
    print 'Answerer Initialized'
    print testAnswerer(answerer,trainRoot + 'S08',True,True)
    print testAnswerer(answerer,trainRoot + 'S09',True,True)

def test_data():
    print 'Testing Final Data'
    print 'Initializing Answerer'
    answerer = qa.answerer(testRoot)
    print 'Answerer Initialized'
    print testAnswerer(answerer,testRoot + 'S10',False,True)

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == '-m':
            test_missed()
        elif sys.argv[1] == '-t':
            test_training_data()
        elif sys.argv[1] == '-f':
            test_data()

if __name__ == '__main__':
    main()
