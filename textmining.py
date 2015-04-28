# coding: utf-8
import os
import pymorphy2
import nltk
import codecs
import pickle
import numpy
import lda


with codecs.open('/home/chubakur/Документы/data/stopwords.txt', encoding='utf-8') as _fh:
    stopwords = _fh.read().split()

morpher = pymorphy2.MorphAnalyzer()

if __name__ == '__main__':
    create_hist = False
    if create_hist:
        book_dir = '/home/chubakur/Документы/data/война и мир'
        histogram = dict()
        for filename in os.listdir(book_dir):
            print filename
            with codecs.open("%s/%s" % (book_dir, filename), encoding='utf-8') as _fh:
                content = _fh.read()
                atoms = nltk.word_tokenize(content)
                atoms = filter(lambda word: word not in stopwords, atoms)
                # clear_atoms = []
                for atom in atoms:
                    forms = morpher.parse(atom)
                    prob_form = forms[0]
                    if 'PNCT' in prob_form.tag:
                        continue
                    if 'LATN' in prob_form.tag:
                        continue
                    if 'UNKN' in prob_form.tag:
                        continue
                    # nform = prob_form.normal_form
                    nform = atom
                    if len(nform) < 3:
                        continue
                    if prob_form.normal_form in stopwords:
                        continue
                    if nform in histogram:
                        if filename in histogram[nform]:
                            histogram[nform][filename] += 1
                        else:
                            histogram[nform][filename] = 1
                    else:
                        histogram[nform] = {filename: 1}
                    # clear_atoms.append(nform)
        with open('cache.bin', 'wb') as _fh:
            pickle.dump(histogram, _fh)
    else:
        with open('cache.bin', 'rb') as _fh:
            histogram = pickle.load(_fh)
        docs = set()
        for value in histogram.values():
            [docs.add(k) for k in value.keys()]
        matrix = numpy.ndarray((len(docs), len(histogram.keys())))
        for doc_idx, doc_name in enumerate(docs):
            for word_idx, (word, counts) in enumerate(histogram.items()):
                matrix[doc_idx, word_idx] = counts[doc_name] if doc_name in counts else 0
        model = lda.LDA(n_topics=7, n_iter=1500, random_state=1)
        model.fit(matrix)
        topic_word = model.topic_word_
        n_top_words = 20
        for i, topic_dist in enumerate(topic_word):
            topic_words = numpy.array(histogram.keys())[numpy.argsort(topic_dist)][:-n_top_words:-1]
            print(u'Topic {}: {}'.format(i, ' '.join(topic_words)))
        doc_topic = model.doc_topic_
        for idx, doc in enumerate(docs):
            print("{} (top topic: {})".format(doc, doc_topic[idx].argmax()))
