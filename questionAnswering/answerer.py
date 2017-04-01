from helpers import helpers as h
import sys
import spacy
import pdb
import special_cases


nlp = spacy.load('en')

debug = False

if len(sys.argv) > 2 and sys.argv[2] == '-d':
    debug = True

no_type = 0
yes_no_type = 1
date_type = 2
person_type = 3
location_type = 4
reason_type = 5
how_type = 6
thing_type = 8


yes_no_words = {'do','does','did','was','can','will','has',
               'is','have','had','could','have','should'}
date_words = {'when'}
person_words = {'who'}
location_words = {'where'}
reason_words = {'why'}
how_words = {'how'}
thing_words = {'what'}


q_type_words = [yes_no_words,date_words,person_words,location_words,reason_words,how_words,thing_words]


def classify_question(question):
    if len(question) > 0:
        first_word = question[0].lower_
        for i in range(0,len(q_type_words)):
            word_set = q_type_words[i]
            if first_word in word_set:
                return i + 1
    return 0

#TODO Identify longest sentence match

def get_sentence_match(question, sentences):
    top = h.get_top_similar(question,sentences,20)
    sequence_length = 0
    for sentence in top:
        length = h.longest_match(question, sentence)

def answer_yes_no(question,sentences):
    adjacent_nouns = h.get_adjacent_nouns(question)
    result = h.get_top_similar(question,sentences,5)
    if result[0][1] > .25:
        return 'yes'
    else:
        return 'no'

def answer_date(question, sentences):
    top = h.get_top_similar(question,sentences,5)
    answer = h.get_first_entity_with_label(top,'DATE')
    if answer is None:
        return 'NULL'
    return answer.text


#TODO Filter on contains data type(date, quantity, etc.)

def answer_person(question, sentences):
    top = h.get_top_similar(question,sentences,5)
    answer = h.get_first_entity_with_label(top,'PERSON')
    if answer is None:
        return 'NULL'
    return answer.text


def answer_location(question, sentences):
    top = h.get_top_similar(question,sentences,5)
    answer = h.get_first_entity_with_label(top,'GPE')
    if answer is None:
        return 'NULL'
    return answer.text


def answer_reason(question, sentences):
    return 'REASON: ' + h.get_top_similar(question,sentences,1)[0][0].text


def answer_how(question, sentences):
    return 'HOW: ' + h.get_top_similar(question,sentences,1)[0][0].text


def answer_what(question, sentences):
    #transformed = h.transform_question(question)
    pass


def find_sentence(question,sentences):

    transformed = h.transform_question(question)
    exact = h.find_exact_match(transformed, sentences)

    if exact is not None:
        return exact

    answer_type = h.get_answer_type(transformed)


def find_answer(question, sentences):

    sentence = find_sentence(question, sentences)




    q_type = classify_question(question)
    answer = 'NULL'
    if q_type == no_type:
        return 'NULL'
    if q_type == yes_no_type:
        answer = answer_yes_no(question,sentences)
    if q_type == date_type:
        answer = answer_date(question,sentences)
    if q_type == person_type:
        answer = answer_person(question,sentences)
    if q_type == location_type:
        answer = answer_location(question,sentences)
    if q_type == reason_type:
        answer = answer_reason(question,sentences)
    if q_type == how_type:
        answer = answer_how(question,sentences)
    if q_type == thing_type:
        answer = answer_what(question,sentences)
    return answer

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
