from spacy.en import English
nlp = English()
doc = nlp(u'A whole document.\nNo preprocessing require.   Robust to arbitrary formating.')
for sent in doc:
    for token in sent:
        if token.is_alpha:
            print token.orth_, token.tag_, token.head.lemma_
