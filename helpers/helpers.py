import io
from nltk.corpus import PlaintextCorpusReader
import sys
import re
import itertools
import spacy
from spacy.symbols import nsubj, dobj, conj, pobj, VERB
import pdb

nlp = spacy.load('en')

debug = False

if len(sys.argv) > 2 and sys.argv[2] == '-d':
    debug = True

#NLP Helpers


def append_spaced_words(word_list):
    result = ''
    for word in word_list:
        result += word + ' '
    return result[:-1]


#Text Helpers

def getAnswerSet(root):
    with io.open(root + '/question_answer_pairs.txt',encoding='latin-1') as f:
        return [(u''.join(line.strip())).split('\t') for line in f.readlines()[1:]]

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def get_key(path):
    slash_indxs = find(path,'/')
    return path[slash_indxs[1]+1:-10]


def clean_content(strContent):
    s = strContent.replace('[','')
    s = s.replace(']','')
    s = s.replace('  ',' ')
    return s


def get_encoded(string):
    return u''.join(string).encode('utf-8')


def get_decoded(string):
    return u''.join(string).decode('utf-8')


#Algorithm helpers

#Check for synonyms of verb????? https://github.com/explosion/spaCy/issues/276

def contains_verb(tokens,verb):
    for token in tokens:
        if token.pos_ == 'VERB' and token.lemma_ == verb:
            return True

def most_similar(word):
    word = nlp.vocab[word]
    queries = [w for w in word.vocab if w.is_lower == word.is_lower and w.prob >= -15]
    by_similarity = sorted(queries, key=lambda w: word.similarity(w), reverse=True)
    return by_similarity[:10]

def longest_match(lemmas1, lemmas2):
    longest_match = 0
    for i in range(0,len(lemmas1)):
        t1 = lemmas1[i]
        for j in range(0,len(lemmas2)):
            t2 = lemmas2[j]
            match_length = 0
            while t1 == t2 and i < len(lemmas1) and j < len(lemmas2):
                match_length += 1
                i += 1
                j += 1
            if match_length > longest_match:
                longest_match = match_length
    return longest_match

def get_root_verb(transformed):
    if transformed is None:
        return None
    right = transformed[2]
    for token in right:
        if token.pos == VERB:
            return token.lemma_


def get_sentences_with_longest_match(question, sentences, min_match):
    pairs = []
    q_lemmas = lemmatize(question)
    for sentence in sentences:
        s_lemmas = lemmatize(sentence)
        match = longest_match(q_lemmas,s_lemmas)
        if match >= min_match:
            pairs.append([sentence, min_match])
    pairs = sorted(pairs,key=lambda x:(-x[1]))
    return pairs

def index_of(tokens,lemmatized_word):
    for i in range(0,len(tokens)):
        if tokens[i].lemma_ == lemmatized_word:
            return i
    return -1


def get_subjects(doc):
    verbs = set()
    for possible_subject in doc:
        if possible_subject.dep == nsubj and possible_subject.head.pos == VERB:
            verbs.add(possible_subject.lemma_)
    return verbs


def get_subject_verbs(doc):
    subjects = set()
    for possible_subject in doc:
        if possible_subject.dep == nsubj and possible_subject.head.pos == VERB:
            subjects.add(possible_subject.head.lemma_)
    return subjects

def get_objects(doc):
    objects = set()
    for possible_object in doc:
        if (possible_object.dep == dobj or possible_object.dep == pobj) and possible_object.head.pos == VERB:
            objects.add(possible_object.lemma_)
    return objects

def is_semi_match(question,sentence):

    q_subs = get_subjects(question)
    q_verbs = get_subject_verbs(question)
    q_obs =  get_objects(question)

    s_subs = get_subjects(sentence)
    s_verbs = get_subject_verbs(sentence)
    s_obs = get_objects(sentence)

    if len(q_verbs & s_verbs) > 0:
        if len(q_subs & s_subs) > 0 or len(q_obs & s_obs) > 0:
            return True
    return False


def get_top_similar(question, transformed, sentences, top):
    pairs = []
    verb = get_root_verb(transformed)
    for sentence in sentences:
        if contains_verb(list(sentence),verb):
        #if is_semi_match(question,transformed,sentence):
            sim = jaccard_doc(question, sentence)
        else:
            sim = 0
        pairs.append([sentence,sim])
    pairs = sorted(pairs,key=lambda x:(-x[1]))
    return pairs[:top]

def get_noun_indices(tokens):
    result = get_pos_indices(tokens,{'NOUN','PROPN'})
    if 0 in result:
        return result[1:]
    return result

def get_first_sentence_ent_type(sentences,types):
    for sentence in sentences:
        for ent in sentence.ents:
            if ent.label_ in types:
                return sentence
    return None


def get_first_entity_with_label(items,label):
    for item in items:
        doc = item[0]
        for ent in doc.ents:
            if ent.label_ == label:
                return ent
    return None



def get_head_noun_indices(tokens):
    head_noun_indices = []
    indices = get_noun_indices(tokens)
    i = 0
    while i < len(indices):
        while (i < len(indices) - 1) and ((indices[i+1] - indices[i]) == 1):
            i += 1
        head_noun_indices.append(indices[i])
        i += 1
    return head_noun_indices


    for i in range(0,len(indices)-1):
        if (indices[i+1] - indices[i]) > 1:
            n1 = i
            n2 = i + 1
            while (n2 < len(indices)-1) and ((indices[n2+1] - indices[n2]) == 1):
                n2 += 1
            adjacent_nouns.append([tokens[indices[n1]],tokens[indices[n2]]])
            head_noun_indices.append([indices[n1],indices[n2]])
    return head_noun_indices

def get_pos_indices(tokens,tags):
    indices = []
    for i in range(0,len(tokens)):
        token = tokens[i]
        if token.pos_ in tags:
            indices.append(i)
    return indices

def lemmatize(tokens):
    return [t.lemma_ for t in tokens if t.lower_ not in stop_words]


def exact_match(left, question_phrase, right, s_lemmas):
    if len(right) == 0 or len(s_lemmas) == 0:
        return False
    for i in range(0,len(s_lemmas)):
        j = 0
        while j < len(right) and i < len(s_lemmas) and right[j] == s_lemmas[i]:
            if j == len(right) - 1:
                return True
            i += 1
            j += 1
    return False
'''
PERSON	People, including fictional.
NORP	Nationalities or religious or political groups.
FACILITY	Buildings, airports, highways, bridges, etc.
ORG	Companies, agencies, institutions, etc.
GPE	Countries, cities, states.
LOC	Non-GPE locations, mountain ranges, bodies of water.
PRODUCT	Objects, vehicles, foods, etc. (Not services.)
EVENT	Named hurricanes, battles, wars, sports events, etc.
WORK_OF_ART	Titles of books, songs, etc.
LANGUAGE	Any named language.

DATE	Absolute or relative dates or periods.
TIME	Times smaller than a day.
PERCENT	Percentage, including "%".
MONEY	Monetary values, including unit.
QUANTITY	Measurements, as of weight or distance.
ORDINAL	"first", "second", etc.
CARDINAL	Numerals that do not fall under another type.

'''

def get_answer_type(question):


    if len(question) > 0:
        t1 = question[0].lemma_
    else:
        t1 = ''
    if len(question) > 1:
        t2 = question[1].lemma_
    else:
        t2 = ''
    if len(question) > 2:
        t3 = question[2].lemma_
    else:
        t3 = ''
    if len(question) > 3:
        t4 = question[3].lemma_
    else:
        t4 = ''

    if t1 == 'be':
        #true-false
        return [0]
    if t1 == 'do':
        #true-false
        return [0]
    if t1 == 'who':
        #person
        if t2 == 'do':
            #want object
            return [1,{pobj,dobj},{'PERSON'}]
        else:
            #want subject
            return [1,{nsubj},{'PERSON'}]
    if t1 == 'what':
        #thing/event
        if t2 == 'year':
            return [1,{},{'DATE'}]
        if t2 == 'do':
            return [1,{pobj,dobj},{'NORP','FACILITY','ORG','GPE','PRODUCT','EVENT','WORK_OF_ART','LANGUAGE'}]
        else:
            return [1,{},{'NORP','FACILITY','ORG','GPE','PRODUCT','EVENT','WORK_OF_ART','LANGUAGE'}]

    if t1 == 'where':
        #location
        return [1,{},{'LOC'}]
    if t1 == 'when':
        #date
        return [1,{},{'DATE'}]
    if t1 == 'why':
        #reason
        return [2]
    if t1 == 'how':
        if t2 == 'many':
            return [1,{'QUANTITY'}]
            if t3 == 'long':
                return [1,{'CARDINAL'}]
        if t2 == 'much':
            return [1,{'QUANTITY','PERCENT','MONEY'}]

        if t2 == 'long':
            return [1,{'CARDINAL'}]
        return [2]
    return [3]




def find_exact_match(transformed, sentences):
    if transformed is None:
        return None
    left = lemmatize(transformed[0])
    question_phrase = lemmatize(transformed[1])
    right = lemmatize(transformed[2])

    for sentence in sentences:
        s_tokens = list(sentence)
        s_lemmas = lemmatize(s_tokens)

        if exact_match(left, question_phrase, right, s_lemmas):
            return sentence

    return None










def get_question_phrase_index(tokens):
    if len(tokens) > 0:
        t1 = tokens[0].lemma_
    else:
        t1 = ''
    if len(tokens) > 1:
        t2 = tokens[1].lemma_
    else:
        t2 = ''
    if len(tokens) > 2:
        t3 = tokens[2].lemma_
    else:
        t3 = ''

    if t1 == 'be':
        return 0
    if t1 == 'do':
        return 0
    if t1 == 'who':
        if t2 == 'do' or t2 == 'be':
            return 1
        return 0
    if t1 == 'what':
        if t2 == 'do' or t2 == 'be':
            return 1
        return 0
    if t1 == 'where':
        if t2 == 'do' or t2 == 'be':
            return 1
        return 0
    if t1 == 'when':
        if t2 == 'do' or t2 == 'be':
            return 1
        return 0
    if t1 == 'why':
        if t2 == 'do' or t2 == 'be':
            return 1
        return 0
    if t1 == 'how':
        if t2 == 'do' or t2 == 'be' or t2 == 'many' or t2 == 'long':
            if t3 == 'long':
                return 2
            return 1
        return 0
    return 0



def transform_question(question):
    tokens = list(question)
    question_phrase_index = get_question_phrase_index(question)
    head_noun_indices = get_head_noun_indices(question)
    if len(head_noun_indices) > 0:
        first_head_noun_index = head_noun_indices[0]
    else:
        return None

    if question_phrase_index > 0:
        question_phrase = tokens[0:question_phrase_index+1]
    else:
        question_phrase = [tokens[0]]

    left = tokens[question_phrase_index+1:first_head_noun_index+1]
    right = tokens[first_head_noun_index+1:-1]

    if len(right) > 0:
        if right[0].lower_ == '\'s':
            left.append(right[0])
            right = right[1:]

        if right[0].lower_ == 'ever':
            question_phrase.append(right[0])
            right = right[1:]

    result = [left,question_phrase,right]
    return result

def get_head_noun_set(doc):
    tokens = list(doc)
    noun_idx = get_head_noun_indices(tokens)
    nouns = set()
    for index in noun_idx:
        nouns.add(tokens[index].lower_)
    return nouns

def get_noun_set(doc):
    tokens = list(doc)
    noun_idx = get_noun_indices(tokens)
    nouns = set()
    for index in noun_idx:
        nouns.add(tokens[index].lower_)
    return nouns

def get_adjacent_nouns(doc):
    adjacent_nouns = []
    tokens = list(doc)
    indices = get_head_noun_indices(tokens)
    for i in range(0,len(indices)-1):
        adjacent_nouns.append([tokens[indices[i]],tokens[indices[i+1]]])
    return adjacent_nouns

stop_words = {u'and',u'or',u'the',u'as',u'but',u'a',u'of',u'by',u'to',u'in'}

def get_word_set(sentence):
    s = set([word.lower_ for word in sentence])
    r = s - stop_words
    return r


def jaccard_doc(doc1, doc2):
    set1 = get_word_set(doc1)
    set2 = get_word_set(doc2)
    return jaccard_set(set1,set2)


def jaccard_set(set1, set2):
    intersection = set1 & set2
    union = set1 | set2
    if len(intersection) == 0 or len(union) == 0:
        return 0
    return float(len(intersection)) / float(len(union))


def add_doc_to_dictionary(docs, path):
    with io.open(path,encoding='latin-1') as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    if len(lines) > 1:
        content = lines
        str_content = u''
        for line in content:
            str_content += line + u' '
        key = get_key(path)
        docs[key] = [nlp(sent.text) for sent in nlp(clean_content(str_content)).sents]


def addDocsToDictionary(docs,root):
    corpus = PlaintextCorpusReader(root,'.*.txt.clean')
    for path in corpus.fileids():
        add_doc_to_dictionary(docs, root + path)
