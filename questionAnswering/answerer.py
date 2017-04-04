from helpers import helpers as h
import sys
import spacy
import pdb
import special_cases

nlp = spacy.load('en')

debug = False

if len(sys.argv) > 2 and sys.argv[2] == '-d':
    debug = True

def longest_match_sentence(question, sentences, answer_type):
    top = h.get_sentences_with_longest_match(question, sentences, 4)
    if len(top) > 0:
        if answer_type[0] == 1:
            sentence = h.get_first_entity_with_label(top,answer_type[1])
            if sentence is None:
                return top[0][0]
        else:
            return top[0][0]

def most_similar_sentence(question, transformed, sentences, answer_type):
    top = h.get_top_similar(question,transformed,sentences,10)
    if len(top) > 0:
        if answer_type[0] == 1:
            sentence = h.get_first_entity_with_label(top,answer_type[1])
            if sentence is None:
                return top[0][0]
        else:
            return top[0][0]


def find_answer(question, sentences):
    answer_type = h.get_answer_type(question)
    transformed = h.transform_question(question)

    sentence = h.find_exact_match(transformed, sentences)

    if sentence is not None:
        if answer_type[0] == 0:
            return 'yes'
    else:
        sentence = most_similar_sentence(question, transformed, sentences, answer_type)
        if answer_type[0] == 0:
            if h.jaccard_doc(question,sentence) > 0:
                return 'yes'
            return 'no'

    if answer_type[0] == 1:
        entities = []
        for ent in sentence.ents:
            entities.append([ent.text, ent.label_])

        return str(entities) + '\n' + sentence.text

    return sentence.text


class answerer(object):
    docs = {}

    @classmethod
    def answerQuestion(self,question,path):
        #chunks = h.get_chunks(question.lower())
        if path in self.docs:

            return find_answer(nlp(question),self.docs[path])
        else:
            return 'I don\'t have the file: ' + path

    def __init__(self,docRoot):
        print 'Indexing documents into database'
        h.addDocsToDictionary(self.docs,docRoot)
        print 'Finished indexing documents'
