import os
import io
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import PlaintextCorpusReader
import hashlib
import sys
import en
reload(sys)


def get_chunks(text):
    chunked = ne_chunk(pos_tag(word_tokenize(text.encode('utf-8'))))
    prev = None
    current_chunk = []
    continuous_chunk = []
    for i in chunked:
        if type(i) == Tree:
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue
    return continuous_chunk
def get_sentences(content):
    result = []
    sentences = [s.strip() for s in nltk.sent_tokenize(content.decode('utf-8'))]
    for s in sentences:
        if len(s) > 0:
            result.append(s)
    return result


def get_head_verb(tagged_sentence):
    for item in tagged_sentence:
        tag = item[1]
        word = item[0]
        if 'VB' in tag:
            return en.verb.infinitive(word.lower())
    try:
        return en.verb.infinitive(tagged_sentence[0][0].lower())
    except:
        return None

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


def getTaggedString(text):
    return nltk.pos_tag(nltk.word_tokenize(text))

def append_spaced_words(word_list):
    result = ''
    for word in word_list:
        result += word + ' '
    return result[:-1]

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


def get_key(path):
    slash_indxs = find(path,'/')
    return path[slash_indxs[1]+1:-10]


def clean_content(strContent):
    s = strContent.replace('[','')
    s = s.replace(']','')
    return get_encoded(s)


def get_encoded(string):
    return u''.join(string).encode('utf-8')

def get_decoded(string):
    return u''.join(string).decode('utf-8')

def addDocToDictionary(docs, path):
    with io.open(path,encoding='latin-1') as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    if(len(lines) > 1):
        title = lines[0].replace('_',' ')
        content = lines[1:]
        strContent = ''
        for line in content:
            strContent += line
        key = get_key(path)
        docs[key] = get_sentences(clean_content(strContent))
def addDocsToDictionary(docs,root):
    corpus = PlaintextCorpusReader(root,'.*.txt.clean')
    for path in corpus.fileids():
        addDocToDictionary(docs,root + path)
def getAnswerSet(root):
    with io.open(root + '/question_answer_pairs.txt',encoding='latin-1') as f:
        return [line.strip().split('\t') for line in f.readlines()[1:]]

#        with open(root + d + '/question_answer_pairs.txt',encoding='latin-1') as f:
#            answerSet.append([line.strip().split('\t') for line in f.readlines()[1:]])
