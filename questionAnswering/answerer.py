from helpers import helpers as h
import en


no_type = 0
yes_no_type = 1
date_type = 2

PAST_TENSE = 0
PAST_PARTICIPLE = 1
PRESENT_TENSE = 2
INFINITIVE = 3

yes_no_words = {'do','does','did','was','can','will','has',
               'is','have','had','could','have','should'}

def answer_date(question,text):
    return 'yes'

def get_conjugation(word,tense):
    try:
        return {
            PAST_TENSE: en.verb.past(word),
            PAST_PARTICIPLE: en.verb.past_participle(word),
            PRESENT_TENSE: en.verb.present(word),
            INFINITIVE: en.verb.infinitive(word)
        }[tense]
    except KeyError:
        return None


def contained_in_document(rest_of_sentence,text):
    statement = h.append_spaced_words([w[0] for w in rest_of_sentence])
    if statement in text:
        return True
    return False


def answer_yes_no(question,text):
    tagged_string = h.getTaggedString(question)
    index = 1
    while index < len(tagged_string) and tagged_string[index][1] == 'NNP':
        index += 1
    rest_of_sentence = [list(w) for w in tagged_string[index:-1]]
    if contained_in_document(rest_of_sentence,text):
        return 'yes'
    else:
        for item in rest_of_sentence:
            if item[1] == 'VB':
                past = get_conjugation(item[0],PAST_TENSE)
                if past is not None:
                    item[0] = past
                    if contained_in_document(rest_of_sentence,text):
                        return 'yes'
    return 'no'

def classify_question(question):
    words = question.lower().split()
    if len(words) > 0:
        first_word = words[0]
        if first_word in yes_no_words:
            return yes_no_type
        return date_type
    else:
        return no_type

def find_answer(question,text):
    qType = classify_question(question)
    answer = {
        no_type: '',
        yes_no_type: answer_yes_no(question,text),
        date_type: answer_date(question,text)
    }[qType]
    return answer

class answerer(object):
    docs = {}

    @classmethod
    def answerQuestion(self,question,path):
        chunks = h.getChunks(question)
        if path in self.docs:
            return find_answer(question,self.docs[path])
        else:
            return 'I don\'t have the file: ' + path

    def __init__(self,docRoot):
        h.addDocsToDictionary(self.docs,docRoot)