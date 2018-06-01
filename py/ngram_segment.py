#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2018/5/31 下午6:06
# @Author  : Liuyu
# @File    : ngram_segment.py
# @Software: PyCharm

import csv
import jieba
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

# segmente with ngram
def word_ngrams(tokens, stopwords = None, ngram_range = (1,1)):
    if stopwords is not None:
        tokens = [w for w in tokens if w not in stopwords]
    min_n, max_n = ngram_range
    if max_n != 1:
        original_tokens = tokens
        tokens = []
        n_original_tokens = len(original_tokens)
        for n in range(min_n, min(max_n + 1, n_original_tokens + 1)):
            for i in range(n_original_tokens - n +1):
                tokens.append(''.join(original_tokens[i:i+n]))
    return tokens

def wordslist(text, ngram_range = (1,1)):
    wordslist = []
    stop_word = [line.rstrip() for line in open('/Users/liuyu/spider/stopwords.txt')]
    for content in text:
        seg_list = jieba.cut(content, cut_all=False, HMM=False)
        seg_list_after = []
        for seg in seg_list:
            if seg not in stop_word:
                seg_list_after.append(seg)
        ngram_result = word_ngrams(tokens = seg_list_after, ngram_range=ngram_range)
        result = ' '.join(ngram_result)
        wordslist.append(result)
    return wordslist

# return a weight array
if __name__ == '__main__':
    with open('/Users/liuyu/spider/csv/Alidata_processing.csv') as csvfile:
        reader = csv.reader(csvfile)
        text = [row[1] for row in reader][1:]
    corpus = wordslist(text,ngram_range=(2,2))
    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
    word = vectorizer.get_feature_names()
    weight = tfidf.toarray()
