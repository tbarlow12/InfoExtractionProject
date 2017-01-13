#chcp 65001
#set PYTHONIOENCODING=utf-8
#run these commands in windows console to get utf-8 encoding
import wikipedia
import fileinput
import datetime
from datetime import timedelta
import sys
import re #https://docs.python.org/2/howto/regex.html

summaryRegex = 'Who is (.*)\?'
ageRegex = 'How old is (.*)\?'

questionList = [summaryRegex,ageRegex];

sectionRegex = '===? (.*) ===?\\n((?:[^(?:===? .* ===)]|\\s|\.|\(|\)|\:)*)'
dateRegex = '([a-zA-Z]{3,}) (\d){1,2}(?:th|nd|rd)?, (\d{4})'

class Person(object):
    name = ""
    birth = datetime.MINYEAR
    death = datetime.MINYEAR

    def __init__(self,name,birth,death):
        self.name = name
        self.birth = birth
        self.death = death

def make_person(name,birth,death):
    person = Person(name,birth,death)
    return person

#Returns list of tuples where first is section title and second is section content
def getSections(content):
    p = re.compile(sectionRegex)
    matches = re.findall(p,content)
    return matches

def getMonthNum(m):
    return {
        'january': 1,
        'february': 2,
        'march': 3,
        'april': 4,
        'may': 5,
        'june': 6,
        'july': 7,
        'august': 8,
        'september': 9,
        'october': 10,
        'november': 11,
        'december': 12,
    }[m]

def getDate(dateString):
    p = re.compile(dateRegex)
    m = p.match(dateString)
    monthString = m.group(1)
    day = m.group(2)
    year = m.group(3)
    month = getMonthNum(monthString.lower())
    print month
    print day
    print year

def getBirthday(summary):
    print 'date'
    getDate(summary)
    return datetime.date(2015,3,12)

def getDeathday(summary):
    return datetime.date(2015,3,12)

def getSubjectFromRegex(regex,question):
    subject = ''
    p = re.compile(regex)
    m = p.match(question)
    if m is not None:
        subject = m.group(1)
    return subject

def getSubject(question):
    result = (0,'');
    i = 1
    while (i <= len(questionList)):
        regex = questionList[i-1]
        subject = getSubjectFromRegex(regex,question)
        if(len(subject) > 0):
            result = (i,subject);
        i += 1
    return result



def getSections(content):
    p = re.compile(sectionRegex)
    matches = re.findall(p,content)
    return matches

def getAnswer(question):
    questionResult = getSubject(question)
    questionType = questionResult[0]
    print questionType
    subject = questionResult[1]
    if (len(subject) > 0):
        page = wikipedia.page(subject)
        summary = page.summary
        content = page.content.encode('utf-8')
        sections = getSections(content)
        return page.title
    return 'I couldn\'t find an answer to that question'

def main():
    while True:
        question = sys.stdin.readline()
        if(len(question) == 0):
            return
        print 'Question: ' + question
        print getAnswer(question)


if __name__ == '__main__':
    main()
