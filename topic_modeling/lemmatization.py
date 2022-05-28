

def lemmatization(texts, allowed_postags=['NOUN', 'PROPN', 'VERBS', 'ADJ', 'ADV']):
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc])  # if token.pos_ in allowed_postags])
    return texts_out


def process_lemmatization(data, allowed_postags, min_wordlen):
    nlp = spacy.load('de_core_news_lg', disable=['parser', 'ner'])
    data_lemmatized = lemmatization(data_words_nostops,
                                    allowed_postags=allowed_postags)  # hier können POS-Tags ein-/ausgeschlossen werden

    data_out = [[word for word in doc if len(word) > min_wordlen and word not in stoplist] for doc in
                data_lemmatized]  # Hier werden wörter mit weniger als drei Buchstaben ausgeschlossen
    return data_out
