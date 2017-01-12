from lxml import html
import requests
page = requests.get('https://en.wikipedia.org/wiki/Michael_Jordan')
tree = html.fromstring(page.content)
paragraphs = tree.xpath('//p/text()')
for p in paragraphs:
    print p
