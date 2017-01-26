import re

class trainedModel(object):
    @classmethod
    def train(self,path):
        model = 'test'
        return model

    def __init__(self,path):
        self.model = self.train(path)
class answerer(object):

    @classmethod
    def answerQuestion(self,question):
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
