def keyword_diversity(engine, number_of_words):
    '''
    Hier soll die Einzigartigkeit von Keywords innerhalb der Topics untersucht
    werden, in je weniger Topics ein Wort enthalten ist, desto trennschärfer
    sollten die Topics sein. Vgl. mit der Relevance Metric bei pyLDAvis,
    nähere Infos dazu im oben verlinkten Paper, und dem Exclusivity Score
    im Paper von Thompson/Mimno. Bislang harter Filter, es werden NUR
    einzigartige Wörter gezählt, ich möchte einen Threshold einbauen,
    dass "seltene" Wörter besser bewertet werden, also beispielsweise
    auch Wörter, die in 2-3 Topics vorkommen einen guten Score bekommen,
    Wörter, die in allen Topics vorkommen, einen schlechten. Das könnte
    man dann auch noch mit der jeweiligen Gewichtung im Topic verrechnen.
    Für Dennis hilfreich, weil er möglichst trennscharfe und konsistente
    Topics braucht, um die pluralistischen Inhalte der Sammlung abzubilden.
    -> evtl. noch in Zusammenhang mit Dictionary bringen
    '''

    if engine == 'gensim':

        if load_models == False:
            topwords = []
            toptops = lda_model_gensim.print_topics(num_topics=int(topics), num_words=number_of_words)
            for tupel in toptops:
                words = re.findall(r"\"(.*?)\"", tupel[1])
                for word in words:
                    topwords.append(word)

        if load_models == True:
            topwords = []
            for line in top_words_gensim:
                newline = []
                for i in range(0, number_of_words):
                    newline.append(re.findall(r"\"(.*?)\"", line[1].split(' + ')[i])[0])
                for word in newline:
                    topwords.append(word)

        print(len(topwords))
        print(len(set(topwords)))
        singularity = (len(set(topwords)) / (int(topics_gensim) * number_of_words)) * 100
        print(str(int(singularity)) + '%')

    if engine == 'mallet':
        if load_models == False:
            topwords = []
            toptops = lda_model_mallet.print_topics(num_topics=topics, num_words=number_of_words)
            for tupel in toptops:
                words = re.findall(r"\"(.*?)\"", tupel[1])
                for word in words:
                    topwords.append(word)

        if load_models == True:
            topwords = []
            for line in top_words_mallet:
                newline = []
                for i in range(0, number_of_words):
                    newline.append(re.findall(r"\"(.*?)\"", line[1].split(' + ')[i])[0])
                for word in newline:
                    topwords.append(word)

        print(len(topwords))
        print(len(set(topwords)))
        singularity = (len(set(topwords)) / (int(topics_mallet) * number_of_words)) * 100
        print(str(int(singularity)) + '%')


def topic_search(engine, topic_number, *threshold_custom_value):
    '''
    engine must be 'gensim' or 'mallet'

    if threshold_custom_value is left empty, average topic weight is set as threshold
    treshold_custom_value must be float in range 0.0 and 1.0
    '''

    if engine == 'gensim':

        if threshold_custom_value:
            threshold_topic_weight = threshold_custom_value
        else:
            threshold_topic_weight = average_weight_gensim

        if load_models == True:
            raw_data = load_dataset_gensim

        for j, line in enumerate(doc_tops_gensim):
            for tup in line:
                if tup[0] == topic_number and tup[1] >= threshold_topic_weight:
                    print(raw_data[j])

    if engine == 'mallet':

        if threshold_custom_value:
            threshold_topic_weight = threshold_custom_value
        else:
            threshold_topic_weight = average_weight_mallet

        if load_models == True:
            raw_data = load_dataset_mallet

        for j, line in enumerate(doc_tops_mallet):
            for tup in line:
                if tup[0] == topic_search and tup[1] >= threshold_topic_weight:
                    print(raw_data[j])


def topic_weights_plot(engine, save_doc=False, save_fig=False):
    top_weight_sum = {}

    if engine == 'gensim':

        for i, line in enumerate(doc_tops_gensim):
            for tup in line:
                if tup[0] not in top_weight_sum:
                    top_weight_sum[tup[0]] = tup[1]
                if tup[0] in top_weight_sum:
                    top_weight_sum[tup[0]] += tup[1]

    if engine == 'mallet':

        for i, line in enumerate(doc_tops_mallet):
            for tup in line:
                if tup[0] not in top_weight_sum:
                    top_weight_sum[tup[0]] = tup[1]
                if tup[0] in top_weight_sum:
                    top_weight_sum[tup[0]] += tup[1]

    points = []
    for top, weight in top_weight_sum.items():
        points.append((top, weight))

    weights_reverse = [(tup[1], tup[0]) for tup in points]
    weights_sorted = sorted(weights_reverse, reverse=True)

    x, y = list(zip(*points))
    pylab.bar(x, y)
    pylab.title('Topic Weight Sums')
    pylab.ylabel('Sum Weights')
    pylab.xlabel("Topic Nr.")

    if save_fig:
        if engine == 'mallet':
            pylab.savefig(user_output + user + '_Mallet_topic_weight_sums_' + name_dataset_mallet + '_' + str(
                topics_mallet) + 'topics' + now + '.pdf')
        if engine == 'gensim':
            pylab.savefig(user_output + user + '_Gensim_topic_weight_sums_' + name_dataset_gensim + '_' + str(
                topics_gensim) + 'topics' + now + '.pdf')

    pylab.show()

    if save_doc:
        if engine == 'mallet':
            out = open(user_output + user + '_Mallet_top_weight_sums_' + name_dataset_mallet + '_' + str(
                topics_mallet) + 'topics_' + now + '.txt', 'w', encoding='UTF-8')
        if engine == 'gensim':
            out = open(user_output + user + '_Gensim_top_weight_sums_' + name_dataset_gensim + '_' + str(
                topics_gensim) + 'topics_' + now + '.txt', 'w', encoding='UTF-8')
        for line in weights_sorted:
            out.write(str(line))
        out.close()


def word_count(dataset_wordcount):
    word_count = 0

    if dataset_wordcount == 'data':
        dataset_wordcount = data
    if dataset_wordcount == 'data_words_nostops':
        dataset_wordcount = data_words_nostops
    if dataset_wordcount == 'data_final':
        dataset_wordcount = data_final

    for doc in dataset_wordcount:
        word_count = word_count + len(doc)
    return word_count

