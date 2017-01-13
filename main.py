#chcp 65001
#set PYTHONIOENCODING=utf-8
#run these commands in windows console to get utf-8 encoding
import wikipedia
import fileinput
import sys
import re #https://docs.python.org/2/howto/regex.html

summaryRegex = 'Who is (.*)\?'
ageRegex = 'How old is (.*)\?'

def getSubjectFromRegex(regex,question):
    p = re.compile(regex)
    m = p.match(question)
    print regex
    print question
    if m is not None:
        subject = m.group(1)
        return subject
    return ''

def getSubject(question):
    subject = getSubjectFromRegex(summaryRegex,question)
    if(len(subject) == 0):
        subject = getSubjectFromRegex(ageRegex,question)
    '''
    if subject is not None:
        subject = getSubjectFromRegex(ageRegex,question)

    if subject is None:
        subject = ''
        '''
    return subject

def getSections(content):
    regex = '===? (.*) ===?\\n((?:[^(?:===? .* ===)]|\\s|\.|\(|\)|\:)*)'
    p = re.compile(regex)
    matches = re.findall(p,content)
    return matches

def getAnswer(question):
    subject = getSubject(question)
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
