import os
import gensim
from gensim import corpora
import datetime

#def setup_topic_training(mallet=False, gensim=False):
#
#    if mallet:
#        !apt-get install -y openjdk-8-jdk-headless -qq > /dev/null  # install openjdk
#        !wget http://mallet.cs.umass.edu/dist/mallet-2.0.8.zip
#        !unzip mallet-2.0.8.zip
#
#        os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"  # set environment variable
#        os.environ['MALLET_HOME'] = '/content/mallet-2.0.8'
#        mallet_path = '/content/mallet-2.0.8/bin/mallet'  # you should NOT need to change this
#        return 'MALLET SUCCESSFULLY INSTALLED'
#
#    if gensim:
#        !pip install gensim == 3.8.3
#        import gensim
#        import gensim.corpora as corpora
#        from gensim.utils import simple_preprocess
#        from gensim.models import CoherenceModel
#
#        return 'GENSIM  SUCCESSFULLY INSTALLED'




# def topic_training(dataset, topics, passes_gensim=500, iterations_gensim=5000, optimize_interval_mallet=500,
#                    iterations_mallet=5000):
#     chunks = len(dataset)
#
#     id2word = corpora.Dictionary(dataset)
#
#     corpus = [id2word.doc2bow(text) for text in dataset]
#
#     # Berechnung beider Modelle (Gensim, Mallet)
#     # @markdown ##Parametertuning
#     # @markdown ###Gensim
#
#     random_state_gensim = 100
#     passes_gensim = passes_gensim
#     iterations_gensim = iterations_gensim
#
#     # @markdown ###Mallet
#
#     random_seed_mallet = 100  # @param {type:"integer"}
#     optimize_interval_mallet = optimize_interval_mallet
#     iterations_mallet = iterations_mallet
#
#     lda_model_gensim = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word,
#                                                        num_topics=topics, random_state=random_state_gensim,
#                                                        update_every=0, minimum_probability=0, passes=passes_gensim,
#                                                        iterations=iterations_gensim, alpha='auto',
#                                                        per_word_topics=True)
#
#     lda_model_mallet = gensim.models.wrappers.ldamallet.LdaMallet(mallet_path, corpus=corpus, id2word=id2word,
#                                                                   num_topics=topics, iterations=iterations_mallet,
#                                                                   optimize_interval=optimize_interval_mallet,
#                                                                   random_seed=random_seed_mallet)
#
#     # Document-Topics-Liste erstellen und Topic-Weights berechnen
#
#     doc_tops_import = lda_model_gensim.get_document_topics(corpus)
#
#     doc_tops_gensim = []
#     sum_top_weights = 0.0
#     top_counter = 0
#     min_weight_gensim = 1
#     max_weight_gensim = 0
#     for line in doc_tops_import:
#         doc_tops_transfer = []
#         for tup in line:
#             if float(tup[1]) >= 0:
#                 sum_top_weights = sum_top_weights + float(tup[1])
#                 doc_tops_transfer.append(tup)
#                 top_counter += 1
#                 if float(tup[1]) < min_weight_gensim:
#                     min_weight_gensim = float(tup[1])
#                 if float(tup[1]) > max_weight_gensim:
#                     max_weight_gensim = float(tup[1])
#         doc_tops_gensim.append(doc_tops_transfer)
#
#     average_weight_gensim = sum_top_weights / top_counter
#
#     print('Minimales Topic-Weight Gensim: ' + str(min_weight_gensim))
#     print('Durchschnittliches Topic-Weight Gensim: ' + str(average_weight_gensim))
#     print('Maximales Topic-Weight Gensim: ' + str(max_weight_gensim))
#
#     ## Daten-Output Mallet konvertieren
#
#     doc_tops_import = open(lda_model_mallet.fdoctopics(), mode='r', encoding='UTF-8').read()
#
#     doc_tops_mallet = []
#     sum_top_weights = 0.0
#     top_counter = 0
#     min_weight_mallet = 1
#     max_weight_mallet = 0
#     for line in doc_tops_import.splitlines():
#         doc_tops_transfer = []
#         for topic_nr, topic in enumerate(line.split()):
#             if '.' in topic:
#                 topic_float = float(topic)
#                 if topic_float >= 0:  # Threshold für Weight
#                     sum_top_weights = sum_top_weights + topic_float
#                     top_counter += 1
#                     doc_tops_transfer.append((topic_nr - 2,
#                                               topic_float))  # hier Weight als Float, in anderen Zellen als Str -> vereinheitlichen (?)
#                     if topic_float < min_weight_mallet:
#                         min_weight_mallet = topic_float
#                     if topic_float > max_weight_mallet:
#                         max_weight_mallet = topic_float
#         doc_tops_mallet.append(doc_tops_transfer)
#
#     average_weight_mallet = sum_top_weights / top_counter
#
#     print('Minimales Topic-Weight Mallet: ' + str(min_weight_mallet))
#     print('Durchschnittliches Topic-Weight Mallet: ' + str(average_weight_mallet))
#     print('Maximales Topic-Weight Mallet: ' + str(max_weight_mallet))
#
#     load_models = False
#     topics_gensim = topics
#     topics_mallet = topics


# def safe_model(load_models):
#     if load_models == True:
#         print("Modell bereits gespeichert")
#
#     else:
#         now = str(datetime.now())[:19]
#
#         new_model_mallet = user + '_mallet_' + name_dataset_mallet + '_' + str(topics) + 'topics_' + now + '/'
#         os.mkdir(modeldumps + new_model_mallet)
#         doc_tops_mallet_df = pd.DataFrame(data=doc_tops_mallet)
#         doc_tops_mallet_df.to_pickle(
#             modeldumps + new_model_mallet + user + '_mallet_' + name_dataset_mallet + '_' + str(
#                 topics) + 'topics_' + now + '.doc_tops_mallet')
#         top_words_mallet_df = pd.DataFrame(data=lda_model_mallet.print_topics(num_topics=topics, num_words=1000))
#         top_words_mallet_df.to_pickle(
#             modeldumps + new_model_mallet + user + '_mallet_' + name_dataset_mallet + '_' + str(
#                 topics) + 'topics_' + now + '.top_words_mallet')
#         out = open(modeldumps + new_model_mallet + user + '_mallet_' + name_dataset_mallet + '_' + str(
#             topics) + 'topics_' + now + '.txt', 'w', encoding='UTF-8')
#         out.write(name_dataset_mallet + '\n')
#         out.write('Anzahl Topics: ' + str(topics) + '\n')
#         if name_dataset_mallet == 'data_final':
#             out.write('Stopwords: ' + open_stoplist + '\n')
#             out.write('Lemmatisiert, Pos-Tag-Filter: ' + str(allowed_postags) + '\n')
#         if name_dataset_mallet == 'data_words_nostops':
#             out.write('Stopwords: ' + open_stoplist + '\n')
#         if name_dataset_mallet == 'data':
#             out.write('Kein Data Cleaning durchgeführt' + '\n')
#         out.write('random_seed_mallet: ' + str(random_seed_mallet) + '\n')
#         out.write('optimiize_interval_mallet: ' + str(optimize_interval_mallet) + '\n')
#         out.write('iterations_mallet: ' + str(iterations_mallet) + '\n')
#         out.close()
#
#         new_model_gensim = user + '_gensim_' + name_dataset_gensim + '_' + str(topics) + 'topics_' + now + '/'
#         os.mkdir(modeldumps + new_model_gensim)
#         doc_tops_gensim_df = pd.DataFrame(data=doc_tops_gensim)
#         doc_tops_gensim_df.to_pickle(
#             modeldumps + new_model_gensim + user + '_gensim_' + name_dataset_gensim + '_' + str(
#                 topics) + 'topics_' + now + '.doc_tops_gensim')
#         top_words_gensim_df = pd.DataFrame(data=lda_model_gensim.print_topics(num_topics=topics, num_words=1000))
#         top_words_gensim_df.to_pickle(
#             modeldumps + new_model_gensim + user + '_gensim_' + name_dataset_gensim + '_' + str(
#                 topics) + 'topics_' + now + '.top_words_gensim')
#         out = open(modeldumps + new_model_gensim + user + '_gensim_' + name_dataset_gensim + '_' + str(
#             topics) + 'topics_' + now + '.txt', 'w', encoding='UTF-8')
#         out.write(name_dataset_gensim + '\n')
#         out.write('Anzahl Topics: ' + str(topics) + '\n')
#         if name_dataset_gensim == 'data_final':
#             out.write('Stopwords: ' + open_stoplist + '\n')
#             out.write('Lemmatisiert, Pos-Tag-Filter: ' + str(allowed_postags) + '\n')
#         if name_dataset_gensim == 'data_words_nostops':
#             out.write('Stopwords: ' + open_stoplist + '\n')
#         if name_dataset_gensim == 'data':
#             out.write('Kein Data Cleaning durchgeführt' + '\n')
#         out.write('random_state_gensim: ' + str(random_state_gensim) + '\n')
#         out.write('passes_gensim: ' + str(passes_gensim) + '\n')
#         out.write('iterations_gensim: ' + str(iterations_gensim) + '\n')
#         out.close()
#
#
#
# def print_topics(engine, number_of_words, save_doc=False):
#     """
#     engines can be 'gensim' or 'mallet'
#     to save list include save_doc=True
#     """
#
#     now = str(datetime.now())[:19]
#
#     if engine == 'gensim':
#
#         if load_models == False:
#             output = lda_model_gensim.print_topics(num_topics=topics, num_words=number_of_words)
#
#             if save_doc:
#                 out = open(user_output + user + '_keywords_gensim_' + name_dataset_gensim + '_' + str(
#                     topics) + 'topics_' + str(number_of_words) + 'keywords' + now + '.txt', 'w', encoding='UTF-8')
#                 for line in output:
#                     out_line = str(int(line[0])) + ' ' + str(re.findall(r"\"(.*?)\"", line[1])) + '\n'
#                     out.write(out_line)
#                     print(out_line)
#                 out.close()
#             else:
#                 for line in output:
#                     out_line = str(int(line[0])) + ' ' + str(re.findall(r"\"(.*?)\"", line[1])) + '\n'
#                     print(out_line)
#
#         if load_models == True:
#             if save_doc:
#                 out = open(user_output + user + '_keywords_gensim_' + name_dataset_gensim + '_' + str(
#                     topics_gensim) + 'topics_' + str(number_of_words) + 'keywords' + now + '.txt', 'w',
#                            encoding='UTF-8')
#                 for line in top_words_gensim:
#                     newline = []
#                     for i in range(0, number_of_words):
#                         newline.append(line[1].split(' + ')[i])
#                     out_line = str(int(line[0])) + ' ' + str(re.findall(r"\"(.*?)\"", str(newline))) + '\n'
#                     out.write(out_line)
#                     print(out_line)
#                 out.close()
#
#             else:
#                 for line in top_words_gensim:
#                     newline = []
#                     for i in range(0, number_of_words):
#                         newline.append(line[1].split(' + ')[i])
#                     out_line = str(int(line[0])) + ' ' + str(re.findall(r"\"(.*?)\"", str(newline))) + '\n'
#                     print(out_line)
#
#     if engine == 'mallet':
#         if load_models == False:
#             output = lda_model_mallet.print_topics(num_topics=topics, num_words=number_of_words)
#
#             if save_doc:
#                 out = open(user_output + user + '_keywords_mallet_' + name_dataset_mallet + '_' + str(
#                     topics) + 'topics_' + str(number_of_words) + 'keywords' + now + '.txt', 'w', encoding='UTF-8')
#                 for line in output:
#                     out_line = str(int(line[0])) + ' ' + str(re.findall(r"\"(.*?)\"", line[1])) + '\n'
#                     out.write(out_line)
#                     print(out_line)
#                 out.close()
#
#             else:
#                 for line in output:
#                     out_line = str(int(line[0])) + ' ' + str(re.findall(r"\"(.*?)\"", line[1])) + '\n'
#                     print(out_line)
#
#         if load_models == True:
#             if save_doc:
#                 out = open(user_output + user + '_keywords_mallet_' + name_dataset_mallet + '_' + str(
#                     topics_mallet) + 'topics_' + str(number_of_words) + 'keywords' + now + '.txt', 'w',
#                            encoding='UTF-8')
#                 for line in top_words_mallet:
#                     newline = []
#                     for i in range(0, number_of_words):
#                         newline.append(line[1].split(' + ')[i])
#                     out_line = str(int(line[0])) + ' ' + str(re.findall(r"\"(.*?)\"", str(newline))) + '\n'
#                     out.write(out_line)
#                     print(out_line)
#                 out.close()
#
#             else:
#                 for line in top_words_mallet:
#                     newline = []
#                     for i in range(0, number_of_words):
#                         newline.append(line[1].split(' + ')[i])
#                     out_line = str(int(line[0])) + ' ' + str(re.findall(r"\"(.*?)\"", str(newline))) + '\n'
#                     print(out_line)
#
#
