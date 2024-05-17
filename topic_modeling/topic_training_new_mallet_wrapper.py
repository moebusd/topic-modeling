
import mallet_wrapper.corpora as corpora
from mallet_wrapper.ldamallet import LdaMallet
from mallet_wrapper.coherencemodel import CoherenceModel
import os
from datetime import datetime
import pandas as pd
def topic_training_mallet(dataset, name_dataset, user, topics, mallet_path, optimize_interval_mallet=500, iterations_mallet=5000, random_seed_mallet=100, alpha = 'auto'):

    id2word = corpora.Dictionary(dataset)

    corpus = [id2word.doc2bow(text) for text in dataset]



    lda_model_mallet = LdaMallet(mallet_path, corpus=corpus, id2word=id2word,
                                                                  num_topics=topics, iterations=iterations_mallet,
                                                                  optimize_interval=optimize_interval_mallet,
                                                                  random_seed=random_seed_mallet, alpha = alpha)


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

    # modeldumps = 'modeldumps/'
    #
    # try:
    #     os.mkdir(modeldumps)
    #     print('Ordner "Modeldumps" wurde erstellt.')
    # except FileExistsError:
    #     print('Ordner "Modeldumps" existiert bereits.')
    #
    # new_model_mallet = 'mallet_' + name_dataset + '_' + str(topics) + 'topics_' + now + '/'
    # os.mkdir(modeldumps + new_model_mallet)
    # doc_tops_mallet_df = pd.DataFrame(data=doc_tops_mallet)
    # doc_tops_mallet_df.to_pickle(
    #     modeldumps + new_model_mallet + user + '_mallet_' + name_dataset + '_' + str(
    #         topics) + 'topics_' + now + '.doc_tops_mallet')
    # top_words_mallet_df = pd.DataFrame(data=lda_model_mallet.print_topics(num_topics=topics, num_words=1000))
    # top_words_mallet_df.to_pickle(
    #     modeldumps + new_model_mallet + user + '_mallet_' + name_dataset + '_' + str(
    #         topics) + 'topics_' + now + '.top_words_mallet')
    # out = open(modeldumps + new_model_mallet + user + '_mallet_' + name_dataset + '_' + str(
    #     topics) + 'topics_' + now + '.txt', 'w', encoding='UTF-8')
    # out.write(name_dataset + '\n')
    # out.write('Anzahl Topics: ' + str(topics) + '\n')
    # out.write('random_seed_mallet: ' + str(random_seed_mallet) + '\n')
    # out.write('optimiize_interval_mallet: ' + str(optimize_interval_mallet) + '\n')
    # out.write('iterations_mallet: ' + str(iterations_mallet) + '\n')
    # out.write('Coherence Score: ' + str(coherence_ldamallet) + '\n')
    # out.write('Minimales Topic-Weight Gensim: ' + str(min_weight_mallet) + '\n')
    # out.write('Durchschnittliches Topic-Weight Gensim: ' + str(average_weight_mallet) + '\n')
    # out.write('Maximales Topic-Weight Gensim: ' + str(max_weight_mallet) + '\n')
    # out.close()

    return lda_model_mallet, doc_tops_mallet, topwords_mallet


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
