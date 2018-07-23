#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2018/7/23 10:51 AM
# @Author  : Liuyu
# @File    : Data preprocessing Second Edition.py
# @Software: PyCharm

import csv
import pandas as pd
import datetime
import re

class DataProprecessing:

    def __init__(self, path, starttime, endtime):
        self.text, self.rawdate, self.old_title = self.read_news(path)
        self.datelist = self.get_datelist(starttime, endtime)
        self.new_datelist = self.get_new_datelist()
        self.standard_date = self.change_date_format()
        self.merged_date = self.merge_weekend()
        self.final_date, self.final_article, self.final_title = self.merge_news()
    # get news details
    def read_news(self,path):
        with open(path) as csvfile:
            reader = csv.reader(csvfile)
            text = [row[1] for row in reader][1:]
        with open(path) as csvfile:
            reader = csv.reader(csvfile)
            raw_date = [row[2] for row in reader][1:]
        with open(path) as csvfile:
            reader = csv.reader(csvfile)
            title = [row[3] for row in reader][1:]
        return text, raw_date, title

    # get datelist
    def get_datelist(self, starttime, endtime):
        startdate = datetime.datetime(int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8]))
        delta = datetime.timedelta(days=1)
        n = 0
        date_list = []
        while 1:
            if starttime <= endtime:
                days = (startdate + delta * n).strftime('%Y%m%d')
                n = n + 1
                date_list.append(days)
                if days == endtime:
                    break
        date_list.reverse()
        return date_list

    # Remove duplicates
    def get_new_datelist(self):
        new_datelist = []
        new_datelist.append(self.datelist[0])
        for i in range(len(self.datelist)):
            if self.datelist[i] == new_datelist[-1]:
                pass
            else:
                new_datelist.append(self.datelist[i])
        return new_datelist

    # format raw date.For example:change '2018/5/23' to '20180523'.In order to match with datelist
    def change_date_format(self):
        standard_date = []
        for i in range(len(self.rawdate)):
            split_date = re.split('/|-', self.rawdate[i])
            year = split_date[0]
            month = split_date[1]
            days = split_date[2]
            if len(month) == 1:
                month = '0' + month
            if len(days) == 1:
                days = '0' + days
            date = year + month + days
            standard_date.append(date)
        return standard_date

    def merge_weekend(self):
        merged_date = self.standard_date.copy()
        for i in range(len(self.standard_date)):
            starttime = self.standard_date[i]
            startdate = datetime.datetime(int(starttime[0:4]), int(starttime[4:6]), int(starttime[6:8]))
            week = datetime.datetime.strptime(starttime, '%Y%m%d').weekday()
            if week == 6:
                delta = datetime.timedelta(days=1)
                days = (startdate + delta).strftime('%Y%m%d')
                merged_date[i] = days
            elif week == 5:
                delta = datetime.timedelta(days=2)
                days = (startdate + delta).strftime('%Y%m%d')
                merged_date[i] = days
            else:
                merged_date[i] = self.standard_date[i]
        return merged_date

    def merge_news(self):
        date = []
        article = []
        title = []
        date.append(self.standard_date[0])
        article.append(self.text[0])
        title.append(self.old_title[0])
        for i in range(1, len(self.standard_date)):
            if self.standard_date[i] == date[-1]:
                article[-1] = article[-1] + self.text[i]
                title[-1] = self.old_title[-1] + self.old_title[i]
            else:
                date.append(self.standard_date[i])
                article.append(self.text[i])
                title.append(self.old_title[i])
        return date, article, title

    # Match the date in raw data with 'datelist'.
    def news_prcessing(self):
        perfect_news = {}
        process_article = []
        process_title = []
        n = 0
        for i in range(len(self.final_date)):
            while 1:
                if self.final_date[i] == self.new_datelist[i + n]:
                    process_article.append(self.final_article[i])
                    process_title.append(self.final_title[i])
                    break
                else:
                    process_article.append('')
                    process_title.append('')
                    n += 1
                    continue
        perfect_news['date'] = self.new_datelist
        perfect_news['news'] = process_article
        perfect_news['title'] = process_title
        news_df = pd.DataFrame(perfect_news)
        return news_df

    def write_to_csv(self):
        news_df = self.news_prcessing()
        news_df.to_csv("JDsample_processing.csv", mode='a', index=False, sep=',', encoding='utf_8_sig')


if __name__ == '__main__':
    path = '/Users/liuyu/Desktop/JDnews.csv'
    starttime = '20170517'
    endtime = '20180720'

    Proprecessing = DataProprecessing(path, starttime, endtime)
    Proprecessing.write_to_csv()
