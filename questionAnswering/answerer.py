from helpers import helpers as h


no_type = 0
yes_no_type = 1
date_type = 2
person_type = 3
location_type = 5
reason_type = 6
how_type = 7


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




def answer_date(question,text):
    return 'yes'




def contained_in_document(rest_of_sentence,text):
    statement = h.append_spaced_words([w[0] for w in rest_of_sentence])
    if statement in text:
        return True
    return False







def answer_yes_no(question,sentences):
    tagged_question = h.getTaggedString(question)
    q_head_verb = h.get_head_verb(tagged_question)

    for sentence in sentences:
        tagged_sentence = h.getTaggedString(sentence)
        s_head_verb = h.get_head_verb(tagged_sentence)
        chunks = h.get_chunks(sentence)
        print sentence
        print tagged_sentence
        print s_head_verb

    return 'yes'




def classify_question(question):
    words = question.lower().split()
    if len(words) > 0:
        first_word = words[0]
        for i in range(0,len(q_type_words)):
            word_set = q_type_words[i]
            if first_word in word_set:
                return i + 1
    return 0

def find_answer(question,text):
    q_type = classify_question(question)
    print q_type
    answer = {
        no_type: 'NULL',
        yes_no_type: answer_yes_no(question,text),
        date_type: answer_date(question,text)
    }[q_type]
    return answer

class answerer(object):
    docs = {}

    @classmethod
    def answerQuestion(self,question,path):
        chunks = h.get_chunks(question.lower())
        if path in self.docs:
            return find_answer(question,self.docs[path])
        else:
            return 'I don\'t have the file: ' + path

    def __init__(self,docRoot):
        print 'Indexing documents into database'
        h.addDocsToDictionary(self.docs,docRoot)
        print 'Finished indexing documents'