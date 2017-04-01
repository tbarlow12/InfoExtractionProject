import io
from nltk.corpus import PlaintextCorpusReader
import sys
import re
import itertools
import spacy
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

def contains_verb(doc,verb):
    tokens = list(doc)
    for token in tokens:
        if token.pos_ == 'VERB' and token.lemma_ == verb:
            return True

def most_similar(word):
    word = nlp.vocab[word]
    queries = [w for w in word.vocab if w.is_lower == word.is_lower and w.prob >= -15]
    by_similarity = sorted(queries, key=lambda w: word.similarity(w), reverse=True)
    return by_similarity[:10]

def longest_match(doc1, doc2):
    tokens1 = list(doc1)
    tokens2 = list(doc2)
    longest_match = 0
    for i in range(0,len(tokens1)):
        t1 = tokens1[i]
        for j in range(0,len(tokens2)):
            t2 = tokens2[j]
            match_length = 0
            while t1.lemma_ == t2.lemma_ and i < len(tokens1) and j < len(tokens2):
                match_length += 1
                i += 1
                j += 1
            if match_length > longest_match:
                longest_match = match_length
    return longest_match

def get_root_verb(doc):
    for np in doc.noun_chunks:
        if np.root.head.pos_ == 'VERB':
            return np.root.head.lemma_
    return None

def get_top_similar(question, sentences, top):
    pairs = []
    verb = get_root_verb(question)
    for sentence in sentences:
        if contains_verb(sentence, verb):
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
    return [t.lemma_ for t in tokens]


def exact_match(left, question_phrase, right, s_lemmas):
    for i in range(0,len(s_lemmas)):
        j = 0
        while right[j] == s_lemmas[i]:
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

def get_answer_type(transformed):
    question_phrase = transformed[1]

    if len(question_phrase) > 0:
        t1 = question_phrase[0]
    else:
        t1 = ''
    if len(question_phrase) > 1:
        t2 = question_phrase[1]
    else:
        t2 = ''
    if len(question_phrase) > 2:
        t3 = question_phrase[2]
    else:
        t3 = ''
    if len(question_phrase) > 3:
        t4 = question_phrase[3]
    else:
        t4 = ''

    if t1 == 'be':
        #true-false
        pass
    if t1 == 'do':
        #true-false
        pass
    if t1 == 'who':
        #person
        if t2 == 'do' or t2 == 'be':
            pass
    if t1 == 'what':
        #thing/event
        if t2 == 'do' or t2 == 'be':
            pass
    if t1 == 'where':
        #location
        if t2 == 'do' or t2 == 'be':
            pass
    if t1 == 'when':
        #date
        if t2 == 'do' or t2 == 'be':
            pass
    if t1 == 'why':
        #reason
        if t2 == 'do' or t2 == 'be':
            pass
    if t1 == 'how':
        if t2 == 'do':
            pass
        if t2 == 'be':
            pass
        if t2 == 'many':
            if t3 == 'long':
                pass

        if t2 == 'long':




def find_exact_match(transformed, sentences):
    result = []
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
    t1 = tokens[0].lemma_
    t2 = tokens[1].lemma_
    t3 = tokens[2].lemma_
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
    first_head_noun_index = get_head_noun_indices(question)[0]

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
        content = lines[1:]
        str_content = u''
        for line in content:
            str_content += line + u' '
        key = get_key(path)
        docs[key] = [nlp(sent.text) for sent in nlp(clean_content(str_content)).sents]


def addDocsToDictionary(docs,root):
    corpus = PlaintextCorpusReader(root,'.*.txt.clean')
    for path in corpus.fileids():
        add_doc_to_dictionary(docs, root + path)
