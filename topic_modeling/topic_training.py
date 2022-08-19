def topic_training_gensim(dataset, name_dataset, user, topics, passes_gensim=500, iterations_gensim=5000, random_state_gensim=100):
    import gensim
    import gensim.corpora as corpora
    from gensim.models import CoherenceModel
    import os
    from datetime import datetime
    import pandas as pd

    id2word = corpora.Dictionary(dataset)

    corpus = [id2word.doc2bow(text) for text in dataset]

    random_state_gensim = 100

    lda_model_gensim = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word,
                                                       num_topics=topics, random_state=random_state_gensim,
                                                       update_every=0, minimum_probability=0, passes=passes_gensim,
                                                       iterations=iterations_gensim, alpha='auto',
                                                       per_word_topics=True)


    # Document-Topics-Liste erstellen und Topic-Weights berechnen

    doc_tops_import = lda_model_gensim.get_document_topics(corpus)

    doc_tops_gensim = []
    sum_top_weights = 0.0
    top_counter = 0
    min_weight_gensim = 1
    max_weight_gensim = 0
    for line in doc_tops_import:
        doc_tops_transfer = []
        for tup in line:
            if float(tup[1]) >= 0:
                sum_top_weights = sum_top_weights + float(tup[1])
                doc_tops_transfer.append(tup)
                top_counter += 1
                if float(tup[1]) < min_weight_gensim:
                    min_weight_gensim = float(tup[1])
                if float(tup[1]) > max_weight_gensim:
                    max_weight_gensim = float(tup[1])
        doc_tops_gensim.append(doc_tops_transfer)

    average_weight_gensim = sum_top_weights / top_counter

    topwords_gensim = lda_model_gensim.print_topics(num_topics=topics, num_words=1000)

    coherence_model_ldagensim = CoherenceModel(model=lda_model_gensim,
                                               texts=dataset, dictionary=id2word, coherence='c_v')
    coherence_ldagensim = coherence_model_ldagensim.get_coherence()
    print('\nCoherence Score: ', coherence_ldagensim)


    print('Minimales Topic-Weight Gensim: ' + str(min_weight_gensim))
    print('Durchschnittliches Topic-Weight Gensim: ' + str(average_weight_gensim))
    print('Maximales Topic-Weight Gensim: ' + str(max_weight_gensim))

    now = str(datetime.now())[:19]

    modeldumps = 'modeldumps/'


    try:
        os.mkdir(modeldumps)
        print('Ordner "Modeldumps" wurde erstellt.')
    except FileExistsError:
        print('Ordner "Modeldumps" existiert bereits.')

    new_model_gensim = 'gensim_' + name_dataset + '_' + str(topics) + 'topics_' + now + '/'
    os.mkdir(modeldumps + new_model_gensim)
    doc_tops_gensim_df = pd.DataFrame(data=doc_tops_gensim)
    doc_tops_gensim_df.to_pickle(
        modeldumps + new_model_gensim + user + '_gensim_' + name_dataset + '_' + str(
            topics) + 'topics_' + now + '.doc_tops_gensim')
    top_words_gensim_df = pd.DataFrame(data=lda_model_gensim.print_topics(num_topics=topics, num_words=1000))
    top_words_gensim_df.to_pickle(
        modeldumps + new_model_gensim + user + '_gensim_' + name_dataset + '_' + str(
            topics) + 'topics_' + now + '.top_words_gensim')
    out = open(modeldumps + new_model_gensim + user + '_gensim_' + name_dataset + '_' + str(
        topics) + 'topics_' + now + '.txt', 'w', encoding='UTF-8')
    out.write(name_dataset + '\n')
    out.write('Anzahl Topics: ' + str(topics) + '\n')
    out.write('random_state_gensim: ' + str(random_state_gensim) + '\n')
    out.write('passes_gensim: ' + str(passes_gensim) + '\n')
    out.write('iterations_gensim: ' + str(iterations_gensim) + '\n')
    out.write('Coherence Score: ' + str(coherence_ldagensim) + '\n')
    out.write('Minimales Topic-Weight Gensim: ' + str(min_weight_gensim) + '\n')
    out.write('Durchschnittliches Topic-Weight Gensim: ' + str(average_weight_gensim) + '\n')
    out.write('Maximales Topic-Weight Gensim: ' + str(max_weight_gensim) + '\n')

    out.close()

    return lda_model_gensim, doc_tops_gensim, topwords_gensim


def topic_training_mallet(dataset, name_dataset, user, topics, mallet_path, optimize_interval_mallet=500, iterations_mallet=5000, random_seed_mallet=100):
    import gensim
    import gensim.corpora as corpora
    from gensim.models import CoherenceModel
    import os
    from datetime import datetime
    import pandas as pd

    id2word = corpora.Dictionary(dataset)

    corpus = [id2word.doc2bow(text) for text in dataset]



    lda_model_mallet = gensim.models.wrappers.ldamallet.LdaMallet(mallet_path, corpus=corpus, id2word=id2word,
                                                                  num_topics=topics, iterations=iterations_mallet,
                                                                  optimize_interval=optimize_interval_mallet,
                                                                  random_seed=random_seed_mallet)


    ## Daten-Output Mallet konvertieren

    doc_tops_import = open(lda_model_mallet.fdoctopics(), mode='r', encoding='UTF-8').read()

    doc_tops_mallet = []
    sum_top_weights = 0.0
    top_counter = 0
    min_weight_mallet = 1
    max_weight_mallet = 0
    for line in doc_tops_import.splitlines():
        doc_tops_transfer = []
        for topic_nr, topic in enumerate(line.split()):
            if '.' in topic:
                topic_float = float(topic)
                if topic_float >= 0:  # Threshold für Weight
                    sum_top_weights = sum_top_weights + topic_float
                    top_counter += 1
                    doc_tops_transfer.append((topic_nr - 2,
                                              topic_float))  # hier Weight als Float, in anderen Zellen als Str -> vereinheitlichen (?)
                    if topic_float < min_weight_mallet:
                        min_weight_mallet = topic_float
                    if topic_float > max_weight_mallet:
                        max_weight_mallet = topic_float
        doc_tops_mallet.append(doc_tops_transfer)

    average_weight_mallet = sum_top_weights / top_counter

    topwords_mallet = lda_model_mallet.print_topics(num_topics=topics, num_words=1000)

    coherence_model_ldamallet = CoherenceModel(model=lda_model_mallet,
                                               texts=dataset, dictionary=id2word, coherence='c_v')
    coherence_ldamallet = coherence_model_ldamallet.get_coherence()
    print('\nCoherence Score: ', coherence_ldamallet)

    print('Minimales Topic-Weight Mallet: ' + str(min_weight_mallet))
    print('Durchschnittliches Topic-Weight Mallet: ' + str(average_weight_mallet))
    print('Maximales Topic-Weight Mallet: ' + str(max_weight_mallet))


    now = str(datetime.now())[:19]

    modeldumps = 'modeldumps/'

    try:
        os.mkdir(modeldumps)
        print('Ordner "Modeldumps" wurde erstellt.')
    except FileExistsError:
        print('Ordner "Modeldumps" existiert bereits.')

    new_model_mallet = 'mallet_' + name_dataset + '_' + str(topics) + 'topics_' + now + '/'
    os.mkdir(modeldumps + new_model_mallet)
    doc_tops_mallet_df = pd.DataFrame(data=doc_tops_mallet)
    doc_tops_mallet_df.to_pickle(
        modeldumps + new_model_mallet + user + '_mallet_' + name_dataset + '_' + str(
            topics) + 'topics_' + now + '.doc_tops_mallet')
    top_words_mallet_df = pd.DataFrame(data=lda_model_mallet.print_topics(num_topics=topics, num_words=1000))
    top_words_mallet_df.to_pickle(
        modeldumps + new_model_mallet + user + '_mallet_' + name_dataset + '_' + str(
            topics) + 'topics_' + now + '.top_words_mallet')
    out = open(modeldumps + new_model_mallet + user + '_mallet_' + name_dataset + '_' + str(
        topics) + 'topics_' + now + '.txt', 'w', encoding='UTF-8')
    out.write(name_dataset + '\n')
    out.write('Anzahl Topics: ' + str(topics) + '\n')
    out.write('random_seed_mallet: ' + str(random_seed_mallet) + '\n')
    out.write('optimiize_interval_mallet: ' + str(optimize_interval_mallet) + '\n')
    out.write('iterations_mallet: ' + str(iterations_mallet) + '\n')
    out.write('Coherence Score: ' + str(coherence_ldamallet) + '\n')
    out.write('Minimales Topic-Weight Gensim: ' + str(min_weight_mallet) + '\n')
    out.write('Durchschnittliches Topic-Weight Gensim: ' + str(average_weight_mallet) + '\n')
    out.write('Maximales Topic-Weight Gensim: ' + str(max_weight_mallet) + '\n')
    out.close()

    return lda_model_mallet, doc_tops_mallet, topwords_mallet

def print_topics_gensim(top_words_gensim, number_of_words, name_dataset_gensim, save_doc=False):
    """
    engines can be 'gensim' or 'mallet'
    to save list include save_doc=True
    to save include optional arguments name_dataset and user
    """
    from datetime import datetime
    import re
    now = str(datetime.now())[:19]

    if save_doc:
                out = open('keywords_gensim_' + name_dataset_gensim + '_' + str(
                    len(top_words_gensim.splitlines())) + 'topics_' + str(number_of_words) + 'keywords' + now + '.txt', 'w',
                           encoding='UTF-8')
                for line in top_words_gensim:
                    newline = []
                    for i in range(0, number_of_words):
                        newline.append(line[1].split(' + ')[i])
                    out_line = str(int(line[0])) + ' ' + str(re.findall(r"\"(.*?)\"", str(newline))) + '\n'
                    out.write(out_line)
                    print(out_line)
                out.close()

    else:
                for line in top_words_gensim:
                    newline = []
                    for i in range(0, number_of_words):
                        newline.append(line[1].split(' + ')[i])
                    out_line = str(int(line[0])) + ' ' + str(re.findall(r"\"(.*?)\"", str(newline))) + '\n'
                    print(out_line)

def print_topics_mallet(top_words_mallet, number_of_words, name_dataset_mallet, save_doc=False):
    from datetime import datetime
    import re
    import gensim
    now = str(datetime.now())[:19]

    if save_doc:
                out = open('keywords_mallet_' + name_dataset_mallet + '_' + str(len(top_words_mallet.splitlines())
                    ) + 'topics_' + str(number_of_words) + 'keywords' + now + '.txt', 'w',
                           encoding='UTF-8')
                for line in top_words_mallet:
                    newline = []
                    for i in range(0, number_of_words):
                        newline.append(line[1].split(' + ')[i])
                    out_line = str(int(line[0])) + ' ' + str(re.findall(r"\"(.*?)\"", str(newline))) + '\n'
                    out.write(out_line)
                    print(out_line)
                out.close()

    else:
                for line in top_words_mallet:
                    newline = []
                    for i in range(0, number_of_words):
                        newline.append(line[1].split(' + ')[i])
                    out_line = str(int(line[0])) + ' ' + str(re.findall(r"\"(.*?)\"", str(newline))) + '\n'
                    print(out_line)
