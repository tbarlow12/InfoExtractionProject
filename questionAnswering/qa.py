import re
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import PlaintextCorpusReader
import hashlib
import os
from os import listdir
from os.path import isfile, join
import glob
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('latin-1')

class document(object):

    @classmethod
    def hashWords(self,allWords):
        allHashes = []
        for sentence in allWords:
            hashes = []
            for word in sentence:
                hash_object = hashlib.md5(word.encode())
                hashes.append(hash_object)
            allHashes.append(hashes)
        return allHashes

    @classmethod
    def getWords(self,sentences):
        allWords = []
        for sentence in sentences:
            words = word_tokenize(sentence)
            #words = tokenizer.tokenize(sentence.split())
            allWords.append(words)
        return allWords

    @classmethod
    def getSentences(self,content):
        return sent_tokenize(content.decode())

    def __init__(self,title,content):
        self.title = title
        self.content = content
        self.sentences = self.getSentences(self.content)
        self.words = self.getWords(self.sentences)
        #self.hashes = self.hashWords(self.words)
        #self.hashSentences(self.sentences)

class trainedModel(object):
    documents = {}

    @classmethod
    def normalizeTitle(self,title):
        return title.replace('_',' ')

    @classmethod
    def addDocToDictionary(self,path):
        with open(path) as f:
            lines = f.readlines()
        lines = [x.strip() for x in lines]
        if(len(lines) > 1):
            title = self.normalizeTitle(lines[0].decode())
            content = lines[1:len(lines)]
            strContent = ''
            for line in content:
                strContent += line
            doc = document(title,strContent)
            if (title in self.documents):
                self.documents[title].append(doc)
            else:
                docList = []
                docList.append(doc)
                self.documents[title] = docList
            print title
            print len(self.documents[title])


    @classmethod
    def train(self,path):
        corpus_root = '.'
        corpus = PlaintextCorpusReader(corpus_root, '.*.txt.clean')
        for path in corpus.fileids():
            self.addDocToDictionary(path)

        return 'model'

    def __init__(self,path):
        self.model = self.train(path)
class answerer(object):
    @classmethod
    def get_continuous_chunks(self,text):
         chunked = ne_chunk(pos_tag(word_tokenize(text)))
         prev = None
         current_chunk = []
         continuous_chunk = []
         for i in chunked:
             if type(i) == Tree:
                 current_chunk.append(" ".join([token for token, pos in i.leaves()]))
             elif current_chunk:
                 named_entity = " ".join(current_chunk)
                 if named_entity not in continuous_chunk:
                         continuous_chunk.append(named_entity)
                         current_chunk = []
             else:
                 continue
         return continuous_chunk

    @classmethod
    def getTaggedString(self,text):
        return nltk.pos_tag(nltk.word_tokenize(text))

    @classmethod
    def classifyQuestion(self,question):
        return 0
        #Answers for 4W1H questions may classified into
        #two groups. First group is the answers for how and
        #consists of numerical expressions like distance, time,
        #and so on. Second group corresponds to the answers
        #for 4W, and consists of proper names like person name
        #and time expressions like date.

        #TODO analyze sentence similarity. Hash each word and use Jaccard


    @classmethod
    def answerQuestion(self,question):
        qType = self.classifyQuestion(question)


        #print str(self.get_continuous_chunks(question)) + '\t' + question + '\t' + str(self.getTaggedString(question))
        yesNoWords = '(?:is|did|was|do|are|were|has|have|had|would|will|can)?'
        yesNoRegex = '(?:' + yesNoWords + ')|(?:' + '.*, ' + yesNoWords + ') ' + '.*\?'
        p = re.compile(yesNoRegex,re.I)
        if(p.match(question)):
            #print question
            return 'yes'
        return ''

    def __init__(self,trainingData):
        self.model = trainedModel(trainingData)
class testAnswerPair(object):
    def __init__(self,tup):
        self.title = tup[0].strip()
        self.question = tup[1].strip()
        self.answer = tup[2].strip()
        self.questDiff = tup[3].strip()
        self.ansDiff = tup[4].strip()
        self.file = tup[5].strip()
class testAnswerSet(object):
    def getByAnsDiff(answerSet,level):
        return [x for x in answerSet.content if x.ansDiff == level]
    def getByQuestDiff(answerSet,level):
        return [x for x in answerSet.content if x.questDiff == level]
    def getByQuestAnsDiff(answerSet,questLevel,ansLevel):
        return [x for x in answerSet.content if x.questDiff == questLevel and x.ansDiff == ansLevel]
    def getContent(answerSet,path):
        with open(path) as f:
            content = f.readlines()
        tups = [x.strip().split('\t') for x in content]
        answerPairs = []
        for tup in tups:
            a = testAnswerPair(tup)
            answerPairs.append(a)
        return answerPairs
    def __init__(self,path):
        self.content = self.getContent(path)
class tester(object):

    path1 = 'Question_Answer_Dataset_v1.2/S08/question_answer_pairs.txt'
    path2 = 'Question_Answer_Dataset_v1.2/S09/question_answer_pairs.txt'
    path3 = 'Question_Answer_Dataset_v1.2/S10/question_answer_pairs.txt'

    @classmethod
    def testList(tester,answerList,a):
        correct = 0
        yesNo = 0
        for x in answerList:
            if(x.answer.lower() == 'yes' or x.answer.lower() == 'no'):
                yesNo += 1
            if x.question != 'Question':
                actual = a.answerQuestion(x.question)
                if(actual.lower() == x.answer.lower()):
                    correct += 1
                elif(x.answer.lower() == 'yes'):
                    print x.question
        print 'yes no ratio: ' + str(float(yesNo) / float(len(answerList)))
        if(len(answerList) == 0):
            return 0
        return (float(correct) / float(len(answerList)) * 100)

    @classmethod
    def testBothDifficulty(tester):
        levels = ['easy','medium','hard','too hard']

        for level1 in levels:
            for level2 in levels:
                print level1 + ' questions and ' + level2 + ' answers'
                set1 = tester.testAnswerSet1.getByQuestAnsDiff(level1,level2)
                set2 = tester.testAnswerSet2.getByQuestAnsDiff(level1,level2)
                set3 = tester.testAnswerSet3.getByQuestAnsDiff(level1,level2)

                score1 = tester.testList(set1,answerer)
                print 'list 1: ' + str(score1)

                score2 = tester.testList(set2,answerer)
                print 'list 2: ' + str(score2)

                score3 = tester.testList(set3,answerer)
                print 'list 3: ' + str(score3) + '\n'

                print 'Average score: ' + str(float(score1 + score2 + score3) / 3.0) + '\n'

    @classmethod
    def testDifficultySet(tester,level):

        set1 = tester.testAnswerSet1.getByAnsDiff(level)
        set2 = tester.testAnswerSet2.getByAnsDiff(level)
        set3 = tester.testAnswerSet3.getByAnsDiff(level)

        set1 = tester.testAnswerSet1.getByQuestDiff(level)
        set2 = tester.testAnswerSet2.getByQuestDiff(level)
        set3 = tester.testAnswerSet3.getByQuestDiff(level)

        score1 = tester.testList(set1,answerer)
        print level + ' list 1: ' + str(score1)

        score2 = tester.testList(set2,answerer)
        print level + ' list 2: ' + str(score2)

        score3 = tester.testList(set3,answerer)
        print level + ' list 3: ' + str(score3) + '\n'

        return float(score1 + score2 + score3) / 3.0

    @classmethod
    def testAnswerer(self,answerer,verbose):

        self.testAnswerSet1 = testAnswerSet(self.path1)
        self.testAnswerSet2 = testAnswerSet(self.path2)
        self.testAnswerSet3 = testAnswerSet(self.path3)

        print ''

        if(verbose > 0):

            if(verbose > 1):

                self.testBothDifficulty()

            easyScore = self.testDifficultySet('easy')
            print 'Average easy score: ' + str(easyScore) + '\n'

            mediumScore = self.testDifficultySet('medium')
            print 'Average medium score: ' + str(mediumScore) + '\n'

            hardScore = self.testDifficultySet('hard')
            print 'Average hard score: ' + str(hardScore) + '\n'

            tooHardScore = self.testDifficultySet('too hard')
            print 'Average \'too hard\' score: ' + str(tooHardScore) + '\n'

        list1Score = self.testList(self.testAnswerSet1.content,answerer)
        list2Score = self.testList(self.testAnswerSet2.content,answerer)
        list3Score = self.testList(self.testAnswerSet3.content,answerer)

        overallScore = float(list1Score + list2Score + list3Score) / 3.0

        print 'Total overall score: ' + str(overallScore) + '\n'

def main():
    a = answerer('test')
    tester.testAnswerer(a,0)

if __name__ == '__main__':
    main()
