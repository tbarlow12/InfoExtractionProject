from helpers import helpers as h
import re
import pdb

def regex_matches(text,regex):
    r = re.compile(regex, re.IGNORECASE)
    return [m.groupdict() for m in r.finditer(text)]


def match(regex, text):
    return re.search(regex,text,re.IGNORECASE)


def check_special(question,sentences):
    if match(question.text, 'How old was .*\?'):
        pdb.set_trace()
        print 'age'
