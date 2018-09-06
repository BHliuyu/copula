#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2018/9/6 1:20 PM
# @Author  : Liuyu
# @File    : Get_emotional_score.py
# @Software: PyCharm

import csv
from aip import AipNlp
from pandas.core.frame import DataFrame

def read_news(filepath):
    with open(filepath) as f:
        reader = csv.reader(f)
        news = [row for row in reader][1:]
        old_news = [text[0] for text in news]
        old_news.reverse()
    return old_news

def get_emotion_score(APP_ID, API_Key, Secret_Key, news):
    client = AipNlp(APP_ID, API_Key, Secret_Key)
    all_score = []

    for i in range(len(news)):
        if len(news[i]) == 0:
            score = 0
            all_score.append(score)
        else:
            result = client.sentimentClassify(news[i][0:500])
            score = (result["items"][0]["positive_prob"] - result["items"][0]["negative_prob"]) * result["items"][0][
                "confidence"]
            all_score.append(score)
    return all_score


if __name__ == '__main__':
    filepath = '/Users/liuyu/copula/csv/JD0523-0817 final.csv'
    output_path = 'BABA_score.csv'
    APP_ID = '11762798'
    API_Key = 'pz0vs9t49qGDRGdiZm7Fye3S'
    Secret_Key = '05o3IClyZV1dQnFNk6rtwPPLQYX8xvez'
    news = read_news(filepath)
    all_score = get_emotion_score(APP_ID, API_Key, Secret_Key, news)
    score_df = DataFrame(all_score)
    score_df.to_csv(output_path, mode='a', index=False, sep=',', encoding='utf_8_sig')

