import os
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import PlaintextCorpusReader
import hashlib
def getNamedEntities(text):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
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
def getSentences(content):
    return sent_tokenize(content)
def getTaggedString(text):
    return nltk.pos_tag(nltk.word_tokenize(text))
def addDocToDictionary(docs, path):
    with open(path,encoding='latin-1') as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    if(len(lines) > 1):
        title = lines[0].replace('_',' ')
        content = lines[1:]
        strContent = ''
        for line in content:
            strContent += line
        if title in docs:
            docs[title].append(strContent)
        else:
            docs[title] = [strContent]
def addDocsToDictionary(docs,root):
    corpus = PlaintextCorpusReader(root,'.*.txt.clean')
    for path in corpus.fileids():
        addDocToDictionary(docs,root + '/' + path)


def getAnswerSet(root):
    directories = os.listdir(root)
    answerSet = []
    for d in directories:
        with open(root + d + '/question_answer_pairs.txt',encoding='latin-1') as f:
            answerSet.append([line.strip().split('\t') for line in f.readlines()])
    return answerSet