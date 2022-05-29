def lemmatization(texts, min_wordlen, stoplist= False, allowed_postags=False):
    try:
        import spacy
    except ModuleNotFoundError:
        return 'Ist Spacy installiert?'
    try:
        nlp = spacy.load('de_core_news_lg', disable=['parser', 'ner'])
    except IOError:
        return 'Ist de_core_news_lg installiert?'

    texts_lemmatized = []

    for text in texts:
        print(text)
        doc = nlp(" ".join(text))
        print(doc)
    if allowed_postags:
        texts_lemmatized.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
        print(texts_lemmatized)
    if not allowed_postags:
        texts_lemmatized.append([token.lemma_ for token in doc])

    if stoplist:
        data_out = [[word for word in doc if len(word) > min_wordlen and word not in stoplist] for doc in
                texts_lemmatized]  # Hier werden wörter mit weniger als drei Buchstaben ausgeschlossen

    if not stoplist:
        data_out = [[word for word in doc if len(word) > min_wordlen] for doc in
                texts_lemmatized]  # Hier werden wörter mit weniger als drei Buchstaben ausgeschlossen


    return data_out

print(lemmatization([['Das', 'ist', 'ein', 'Text']], 2, allowed_postags=['NOUN', 'PROPNOUN']))