import helpers as h
class answerer(object):
    @classmethod
    def answerQuestion(self,question):
        print('hello')
        return 'yes'
    def __init__(self,docRoot):
        self.docs = {}
        h.addDocsToDictionary(self.docs,docRoot)