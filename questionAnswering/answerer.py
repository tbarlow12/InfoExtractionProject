from helpers import helpers as h
class answerer(object):

    @classmethod
    def answerQuestion(self,question):
        print(question)
        print(h.getNamedEntities(question))
        return 'yes'
    def __init__(self,docRoot):
        self.docs = {}
        h.addDocsToDictionary(self.docs,docRoot)