from helpers import helpers as h
import sys
import spacy

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


PAST_TENSE = 0
PAST_PARTICIPLE = 1
PRESENT_TENSE = 2
INFINITIVE = 3


yes_no_words = {'do','does','did','was','can','will','has',
               'is','have','had','could','have','should'}
date_words = {'when'}
person_words = {'who'}
location_words = {'where'}
reason_words = {'why'}
how_words = {'how'}

q_type_words = [yes_no_words,date_words,person_words,location_words,reason_words,how_words]


def contained_in_document(rest_of_sentence,text):
    statement = h.append_spaced_words([w[0] for w in rest_of_sentence])
    if statement in text:
        return True
    return False


def parse_match(question, sentence):
    question_parse = h.get_dependency_parse(question)
    sentence_parse = h.get_dependency_parse(sentence)

    question_root = question_parse[0]
    sentence_root = sentence_parse[0]
    if question_root._label.lower() == sentence_root._label.lower():
        return True

    return False

#root = result[0]
#root_verb = root._label
#left = root[0]
#right = root[1]




def classify_question(question):
    if len(question) > 0:
        first_word = question[0].lower_
        for i in range(0,len(q_type_words)):
            word_set = q_type_words[i]
            if first_word in word_set:
                return i + 1
    return 0


def answer_yes_no(question,sentences):

    for sentence in sentences:
        #if parse_match(question,sentence):
        #   return 'yes'
        if h.jaccard_similarity(question,sentence) > .25:
            return 'yes'
    return 'no'


def answer_date(question, sentences):
    return 'DATE NOT IMPLEMENTED'
    #return h.first_match_in_similar_sentences(question,sentences,'\d{4}')


def answer_person(question, sentences):
    return 'PERSON NOT IMPLEMENTED'
    #return h.first_named_entity_in_similar_sentences(question,sentences)


def answer_location(question, sentences):
    return 'LOCATION NOT IMPLEMENTED'
    #return h.first_named_entity_in_similar_sentences(question,sentences)


def answer_reason(question, sentences):
    return 'REASON NOT IMPLEMENTED'
    #return h.first_named_entity_in_similar_sentences(question,sentences)


def answer_how(question, sentences):
    return 'HOW NOT IMPLEMENTED'
    #return h.first_named_entity_in_similar_sentences(question,sentences)


def find_answer(question, sentences):
    q_type = classify_question(question)

    similar = h.get_ranked_similar(question,sentences,5)

    print question

    sentence_match = h.get_sentence_match(question, sentences)

    return 'NULL'
    if q_type == no_type:
        return 'NULL'
    if q_type == yes_no_type:
        return answer_yes_no(question,sentences)
    if q_type == date_type:
        return answer_date(question,sentences)
    if q_type == person_type:
        return answer_person(question,sentences)
    if q_type == location_type:
        return answer_location(question,sentences)
    if q_type == reason_type:
        return answer_reason(question,sentences)
    if q_type == how_type:
        return answer_how(question,sentences)
    return ''

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
