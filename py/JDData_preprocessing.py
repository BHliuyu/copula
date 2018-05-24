#!/usr/bin/env python 
# -*- coding: utf-8 -*-
"""
Created on Wed May 23 13:19:30 2018

@author: liuyu
"""

import csv
import pandas as pd
import datetime

# Input：
#   starttime :start date；endtime ： end date
# Output：
#   date from start date to end date. Its type is str.
def get_datelist(starttime, endtime):
    startdate = datetime.datetime(int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8]))
    delta = datetime.timedelta(days = 1)
    n = 0
    date_list = []
    while 1:
        if starttime <=endtime:
            days = (startdate + delta * n).strftime('%Y%m%d')
            n = n + 1
            date_list.append(days)
            if days == endtime:
                break
    return date_list

# format raw date.For example:change '2018/5/23' to '20180523'.In order to match with datelist
def change_date_format(row_date):
    changed_date = []
    for i in range(len(row_date)):
        split_date = row_date[i].split('/')
        year = split_date[0]
        month = split_date[1]
        days = split_date[2]
        if len(month) == 1:
            month = '0' + month
        if len(days) == 1:
            days = '0' + days
        date = year + month + days
        changed_date.append(date)
    return changed_date

# Change the date of weekend to the day of following Monday
def merge_date(date):
    for i in range(len(date)):
        starttime = date[i]
        startdate = datetime.datetime(int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8]))
        week = datetime.datetime.strptime(starttime, '%Y%m%d').weekday()
        if week == 6:
            delta = datetime.timedelta(days=1)
            days = (startdate + delta).strftime('%Y%m%d')
            date[i] = days
        elif week == 5:
            delta = datetime.timedelta(days=2)
            days = (startdate + delta).strftime('%Y%m%d')
            date[i] = days
    return date

# Merge the news data which have the same date.
def merge_news(standard_date, text):
    news_detail = {}
    date = []
    article = []
    date.append(standard_date[0])
    article.append(text[0])
    for i in range(1, len(standard_date)):
        if standard_date[i] == date[-1]:
            article[-1] = article[-1] + text[i]
        else:
            date.append(standard_date[i])
            article.append(text[i])
    news_detail['date'] = date
    news_detail['article'] = article
    return news_detail

# Match the date in raw data with 'darelist'.
def news_prcessing(datelist, merge_date, text):
    perfect_news = {}
    process_article = []
    n = 0
    for i in range(len(merge_date)):
        while 1:
            if merge_date[i] == datelist[i + n]:
                process_article.append(text[i])
                break
            else:
                process_article.append('')
                n += 1
                continue
    perfect_news['date'] = datelist
    perfect_news['news'] = process_article
    news_df = pd.DataFrame(perfect_news)
    return news_df

if __name__ == '__main__':
    with open('/Users/liuyu/spider/JDnews.csv') as csvfile:
        reader = csv.reader(csvfile)
        text = [row[1] for row in reader][1:]
    with open('/Users/liuyu/spider/JDnews.csv') as csvfile:
        reader = csv.reader(csvfile)
        row_date = [row[2] for row in reader][1:]

    # get datelist which from '20170517' to '20180521'
    datelist = get_datelist('20170517', '20180521')
    # Change the date of weekend to the day of following Monday
    datelist.reverse()
    datelist = merge_date(datelist)
    # Remove duplicates
    new_datelist = []
    new_datelist.append(datelist[0])
    for i in range(len(datelist)):
        if datelist[i] == new_datelist[-1]:
            pass
        else:
            new_datelist.append(datelist[i])

    # format raw date
    standard_date = change_date_format(row_date)
    # Change the date of weekend to the day of following Monday
    merge_date = merge_date(standard_date)
    # Merge the news data which have the same date.
    news_detail = merge_news(merge_date, text)

    final_date = news_detail['date'][:260]
    final_article = news_detail['article'][:260]

    news_df = news_prcessing(new_datelist, final_date, final_article)

    news_df.to_csv("JDdata_processing.csv", mode='a', index=False, sep=',', encoding='utf_8_sig')
