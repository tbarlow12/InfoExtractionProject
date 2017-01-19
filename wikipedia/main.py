#chcp 65001
#set PYTHONIOENCODING=utf-8
#run these commands in windows console to get utf-8 encoding
import wikipedia
import unicodedata
import fileinput
import datetime
#from datetime import timedelta
from dateutil.relativedelta import relativedelta #pip install python-dateutil==1.5
import sys
import re #https://docs.python.org/2/howto/regex.html

summaryRegex = 'who is (.*)\??'
ageRegex = 'how old is (.*)\??'
ageRegex2 = 'what is the age of (.*)\??'
questionList = [summaryRegex,ageRegex,ageRegex2];

def answerType(qType,person):
    if (qType == 1):
        return person.summary
    if(qType >= 2 and qType <= 3):
        if(person.birth is None):
            return None
        if(person.death is not None):
            return str(person.age) + ' (at time of death)'
        return person.age

sectionRegex = '===? (.*) ===?\\n((?:[^(?:===? .* ===)]|\\s|\.|\(|\)|\:)*)'
yearRegex = '(\d{4})'
monthRegex = '([a-zA-Z]{3,})'
dayRegex = '(\\d{1,2})(?:th|nd|rd)?'
#December 23, 1991
dateRegex = monthRegex + ' ' + dayRegex + ', ' + yearRegex
#23 December 1991
dateRegex2 = dayRegex + ' ' + monthRegex + ' ' + yearRegex
dateRange = '\\((?:.*; )?' + dateRegex + ' .* ' + dateRegex + '\\)'
dateRange2 = '\\((?:.*; )?' + dateRegex2 + ' .* ' + dateRegex2 + '\\)'

def difYears(start,finish):
    if finish is None:
        finish = datetime.datetime.now()
    return relativedelta(finish,start)

def make_date(year,month,day):
    d = datetime.datetime(year,month,day,0,0,0)
    return d

class Person(object):

    def __init__(self,name,birth,death,summary):
        self.name = name
        self.birth = birth
        self.death = death
        self.age = difYears(birth,death).years
        self.summary = summary

def make_person(name,birth,death,summary):
    person = Person(name,birth,death,summary)
    return person

def learnPerson(subject,summary,sections):
    birth = getBirthday(summary)
    death = getDeathday(summary)
    if(birth is None and death is None):
        lifeRange = getLifeRange(summary,dateRange)
        if(lifeRange is None):
            lifeRange = getLifeRange(summary,dateRange2)
        if(lifeRange is not None):
            birth = lifeRange[0]
            death = lifeRange[1]
    p = make_person(subject,birth,death,summary)
    return p

#Returns list of tuples where first is section title and second is section content
def getSections(content):
    p = re.compile(sectionRegex,re.I)
    matches = re.findall(p,content)
    return matches

def getMonthNum(m):
    return {
        'january': 1,
        'jan': 1,
        'february': 2,
        'feb': 2,
        'march': 3,
        'mar': 3,
        'april': 4,
        'apr': 4,
        'may': 5,
        'june': 6,
        'jun': 6,
        'july': 7,
        'jul': 7,
        'august': 8,
        'aug': 8,
        'september': 9,
        'sep': 9,
        'october': 10,
        'oct': 10,
        'november': 11,
        'nov': 11,
        'december': 12,
        'dec': 12
    }[m]

def getDate(tup,regex):
    if(regex == 0):
        month = getMonthNum(tup[0].lower())
        day = int(tup[1])
        year = int(tup[2])
        return make_date(year,month,day)
    elif(regex == 1):
        month = getMonthNum(tup[1].lower())
        day = int(tup[0])
        year = int(tup[2])
        return make_date(year,month,day)

def getBirthday(summary):
    p = re.compile('born ' + dateRegex,re.I)
    l = re.findall(p,summary)
    if(len(l) > 0):
        return getDate(l[0],0)
    return None

def getDeathday(summary):
    '''p = re.compile('died ' + dateRegex,re.I)
    l = re.findall(p,summary)
    if(len(l) > 0):
        return getDate(l[len(l)-1])'''
    return None

def getLifeRange(summary,regex):
    regexFlag = 0
    if(regex == dateRange2):
        regexFlag = 1
    p = re.compile(regex,re.I)
    l = re.findall(p,summary)
    if(len(l) > 0):
        result = (getDate(l[0][0:3],regexFlag),getDate(l[0][3:6],regexFlag));
        return result
    return None

def getSubjectFromRegex(regex,question):
    subject = ''
    p = re.compile(regex,re.I)
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
    p = re.compile(sectionRegex,re.I)
    matches = re.findall(p,content)
    return matches

def getAnswer(question):
    questionResult = getSubject(question)
    questionType = questionResult[0]
    subject = questionResult[1]
    if (len(subject) > 0):
        page = wikipedia.page(subject)
        summary = page.summary.encode('utf-8')
        content = page.content.encode('utf-8')
        sections = getSections(content)
        p = learnPerson(subject,summary,sections)
        answer = answerType(questionType,p)
        if(answer is not None):
            return answer
    return 'I couldn\'t find an answer to that question'

def main():

    while True:
        question = sys.stdin.readline()
        if(len(question) == 0):
            return
        print question
        question = question.lower()
        print getAnswer(question)


if __name__ == '__main__':
    main()
