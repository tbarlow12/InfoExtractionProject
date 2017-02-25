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

