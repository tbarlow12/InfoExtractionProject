from helpers import helpers as h
import sys
import spacy
import pdb
from spacy.symbols import nsubj, dobj, conj, pobj, VERB
import re
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
    substitution = h.find_substitution(question, sentences)
    if substitution is not None:
        return substitution.text
    answer_type = h.get_answer_type(question)
    transformed = h.transform_question(question)

    #if 'theory of molarity' in question.text.lower():
    #    pdb.set_trace()
    sentence = h.find_exact_match(transformed, sentences)

    if sentence is not None:
        if answer_type[0] == 0:
            return 'yes'
    else:
        sentence = most_similar_sentence(question, transformed, sentences, answer_type)
        if answer_type[0] == 0:
            j = h.jaccard_doc(question,sentence)
            if j > 0.05:
                return 'yes'
            return 'no'

    if answer_type[0] == 1:
        search_phrase = question[1:-1]
        search_phrase_index = h.index_of_range(sentence,search_phrase)
        if search_phrase_index[0] > 0:
            candidate = sentence[0:search_phrase_index[0]]
            if len(candidate) == 1 and candidate[0].lemma_ == '-PRON-':
                sentence_index = h.index_of_sentence(sentences, sentence)
                while sentence_index > 1:
                    prev = sentences[sentence_index-1]
                    person = h.get_first_entity_with_label_in_sentence(prev,'PERSON')
                    if person is not None:
                        return person.text
                    sentence_index -= 1
            else:
                return candidate.text
        entities = h.get_entities(sentence)
        #print entities
        return 'ENTITY QUESTION: ' + str(entities) + '\n' + sentence.text
    elif answer_type[0] == 2:
        search = answer_type[1]
        tokens = list(sentence)
        s_index = h.index_of_range(sentence,search)
        if s_index[0] > 0:
            pass
            #print sentence
            #print question
            #pdb.set_trace()


    elif answer_type[0] == 3:
        text = sentence.text
        search = answer_type[1].text
        r = re.compile('([^,.;:!?]+)' + search,re.IGNORECASE)
        answers = r.findall(text)
        if len(answers) > 0:
            r2 = re.compile('(the [^,.;:!?]+)' + search,re.IGNORECASE)
            answers2 = r2.findall(text)
            if len(answers2) > 0:
                return answers[0].strip()
            return answers[0].strip()
    else:
        return 'QUESTION TYPE: ' + str(answer_type[0]) + '\n' + sentence.text

    #return sentence.text
    return 'NULL'

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
