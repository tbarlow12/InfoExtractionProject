import io
from nltk.corpus import PlaintextCorpusReader
import en
import sys
import re
import itertools
import spacy



nlp = spacy.load('en')

debug = False

if len(sys.argv) > 2 and sys.argv[2] == '-d':
    debug = True

#NLP Helpers

PAST_TENSE = 0
PAST_PARTICIPLE = 1
PRESENT_TENSE = 2
INFINITIVE = 3


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


def append_spaced_words(word_list):
    result = ''
    for word in word_list:
        result += word + ' '
    return result[:-1]


#Text Helpers

def getAnswerSet(root):
    with io.open(root + '/question_answer_pairs.txt',encoding='latin-1') as f:
        return [line.strip().split('\t') for line in f.readlines()[1:]]

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def get_key(path):
    slash_indxs = find(path,'/')
    return path[slash_indxs[1]+1:-10]


def clean_content(strContent):
    s = strContent.replace('[','')
    s = s.replace(']','')
    return s


def get_encoded(string):
    return u''.join(string).encode('utf-8')


def get_decoded(string):
    return u''.join(string).decode('utf-8')


#Algorithm helpers

def get_ranked_similar(question, sentences, top):
    pairs = []
    for i in range(0,len(sentences)):
        sentence = sentences[i]
        sim = jaccard_similarity(question, sentence)
        pairs.append([sentence,sim])
    s = sorted(pairs,key=lambda x:(-x[1]))
    return s[top:]

def get_noun_indices(tokens):
    indices = []
    for i in range(0,len(tokens)):
        token = tokens[i]
        if token.pos_ == 'NOUN' or token.pos_ == 'PROPN':
            indices.append(i)
    return indices

def get_adjacent_nouns(doc):
    adjacent_nouns = []
    tokens = list(doc)
    indices = get_noun_indices(doc)
    for i in range(0,len(indices)-1):
        if (indices[i+1] - indices[i]) > 1:
            n1 = i
            n2 = i + 1
            while (n2 < len(indices)-1) and ((indices[n2+1] - indices[n2]) == 1):
                n2 += 1
            adjacent_nouns.append([tokens[indices[n1]],tokens[indices[n2]]])
    return adjacent_nouns





            

'''
def first_named_entity_in_similar_sentences(question,sentences):
    ranked_similar = get_ranked_similar(question,sentences,20)
    for tuple in ranked_similar:
        sentence = tuple[0]
        chunks = sentence.ents
        if len(chunks) > 0:
            return chunks[0].text

    return 'NULL'


def first_match_in_similar_sentences(question,sentences,regex_str):
    ranked_similar = get_ranked_similar(question,sentences)

    regex = re.compile(regex_str)

    for tuple in ranked_similar:
        sentence = tuple[0]
        match_list = regex.findall(sentence.text)
        if len(match_list) > 0:
            return match_list[0]

    return 'NULL'

'''

stop_words = {u'and',u'or',u'the',u'as',u'but',u'a',u'of',u'by',u'to',u'in'}

def get_word_set(sentence):

    s = set([word.lower_ for word in sentence])
    r = s - stop_words
    return r


def jaccard_similarity(question, sentence):
    q_word_set = get_word_set(question)
    s_word_set = get_word_set(sentence)

    intersection = q_word_set & s_word_set

    union = q_word_set | s_word_set
    sim = float(len(intersection)) / float(len(union))
    return sim

def add_doc_to_dictionary(docs, path):
    with io.open(path,encoding='latin-1') as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    if len(lines) > 1:
        content = lines[1:]
        str_content = u''
        for line in content:
            str_content += line
        key = get_key(path)
        docs[key] = [nlp(sent.text) for sent in nlp(clean_content(str_content)).sents]


def addDocsToDictionary(docs,root):
    corpus = PlaintextCorpusReader(root,'.*.txt.clean')
    for path in corpus.fileids():
        add_doc_to_dictionary(docs, root + path)
