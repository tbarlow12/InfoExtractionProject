#chcp 65001
#set PYTHONIOENCODING=utf-8
#run these commands in windows console to get utf-8 encoding
import wikipedia
import fileinput
import sys
import re #https://docs.python.org/2/howto/regex.html

def getSubject(question):
    p = re.compile('Who is (.*)\?')
    m = p.match(question)
    subject = m.group(1)
    print 'subject: ' + subject
    return subject

def getSections(content):
    regex = '===? (.*) ===?\\n((?:[^(?:===? .* ===)]|\\s|\.|\(|\)|\:)*)'
    p = re.compile(regex)
    matches = re.findall(p,content)
    return matches

def getAnswer(question):
    subject = getSubject(question)
    page = wikipedia.page(subject)
    summary = page.summary
    content = page.content.encode('utf-8')
    sections = getSections(content)
    print str(len(sections))
    return page.title

def main():
    while True:
        question = sys.stdin.readline()
        if(len(question) == 0):
            return
        getAnswer(question)


if __name__ == '__main__':
    main()
