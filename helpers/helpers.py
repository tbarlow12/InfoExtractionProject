import io
from nltk.corpus import PlaintextCorpusReader
import sys
import re
import itertools
import spacy



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
    return s[:top]

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
    return float(len(intersection)) / float(len(union))


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
