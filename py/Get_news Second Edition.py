#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2018/7/22 下午7:23
# @Author  : Liuyu
# @File    : get_news edi2.py
# @Software: PyCharm

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from lxml import etree



class GetNews:
    def __init__(self, minpage, maxpage, header, base_url):
        self.header = header
        self.base_url = base_url
        self.page_url = self.get_page_url(minpage, maxpage)
        self.all_news_url = self.get_all_news_url()

    # get all page url
    def get_page_url(self, minpage, maxpage):
        page_url = []
        for i in range(minpage, maxpage + 1):
            url = self.base_url + str(i)
            page_url.append(url)
        return page_url

    # get all news url in one page
    def get_news_url(self, url):
        res = requests.get(url, params=self.header)
        res.encoding = res.apparent_encoding
        selector = etree.HTML(res.text)
        news_url = selector.xpath('//div[@class="searchxt"]/a/@href')
        return news_url

    # get all news url in all page
    def get_all_news_url(self):
        all_news_url = []
        for url in self.page_url:
            one_page_url = self.get_news_url(url)
            all_news_url.extend(one_page_url)
        return all_news_url

    # when the news channel is 'finance','companies','opinion','china','index','international',we can get news details by follow function
    def get_news_detail(self, url):
        news_detail = {}
        res = requests.get(url, params=self.header)
        res.encoding = res.apparent_encoding
        selector = etree.HTML(res.text)
        soup = BeautifulSoup(res.text, 'html.parser')
        # get news date from url by regular expression
        pattern = re.compile(r'.*?(\d{4}-\d{2}-\d{2}).*?')
        re_result = re.findall(pattern, url)
        # get news channel form url by regular expression
        source_pattern = re.compile(r'http://(.*?).caixin.*?')
        source_result = re.findall(source_pattern, url)
        source = source_result[0]
        # get news title
        title = selector.xpath('//div[@id="conTit"]/h1')
        clean_title = title[0].text.strip()
        # get news content
        content = ' '.join([p.text.strip().lstrip('【财新网】') for p in soup.select('#Main_Content_Val p')])
        # Use regular expressions to remove reporter information from the news text
        strip_pattern = re.compile(r'(（.*?）).*')
        result = re.findall(strip_pattern, content)

        if len(result) > 0:
            news_detail['content'] = content.lstrip(result[0])
        else:
            news_detail['content'] = content
        news_detail['date'] = re_result[0]
        news_detail['title'] = clean_title
        news_detail['url'] = url
        news_detail['channel'] = source
        return news_detail

    # when the news channel is 'promote',we can get news detail by follow function
    def get_promote_new(self, url):
        news_detail = {}
        header = 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        res = requests.get(url, params=header)
        res.encoding = res.apparent_encoding
        selector = etree.HTML(res.text)
        soup = BeautifulSoup(res.text, 'html.parser')
        # get news date from url by regular expression
        pattern = re.compile(r'.*?(\d{4}-\d{2}-\d{2}).*?')
        re_result = re.findall(pattern, url)
        # get news channel form url by regular expression
        source_pattern = re.compile(r'http://(.*?).caixin.*?')
        source_result = re.findall(source_pattern, url)
        source = source_result[0]
        # get news title
        title = selector.xpath('//div[@class="tit"]')
        clean_title = title[0].text.strip()
        # get news content
        content = ' '.join([p.text.strip().lstrip('【财新网】') for p in soup.select('#news_text p')])
        # Use regular expressions to remove reporter information from the news text
        strip_pattern = re.compile(r'(（.*?）).*')
        result = re.findall(strip_pattern, content)

        if len(result) > 0:
            news_detail['content'] = content.lstrip(result[0])
        else:
            news_detail['content'] = content
        news_detail['date'] = re_result[0]
        news_detail['title'] = clean_title
        news_detail['url'] = url
        news_detail['channel'] = source
        return news_detail

    # when the news channel is 'corp',we can get news detail by follow function
    def get_corp_new(self, url):
        news_detail = {}
        header = 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        res = requests.get(url, params=header)
        res.encoding = res.apparent_encoding
        selector = etree.HTML(res.text)
        soup = BeautifulSoup(res.text, 'html.parser')
        # get news date from url by regular expression
        pattern = re.compile(r'.*?(\d{4}-\d{2}-\d{2}).*?')
        re_result = re.findall(pattern, url)
        # get news channel form url by regular expression
        source_pattern = re.compile(r'http://(.*?).caixin.*?')
        source_result = re.findall(source_pattern, url)
        source = source_result[0]
        # get news title
        title = selector.xpath('//div[@class="title"]/h1')
        clean_title = title[0].text.strip()
        # get news content
        content = ' '.join([p.text.strip().lstrip('【财新网】') for p in soup.select('.article p')])
        # Use regular expressions to remove reporter information from the news text
        strip_pattern = re.compile(r'(（.*?）).*')
        result = re.findall(strip_pattern, content)

        if len(result) > 0:
            news_detail['content'] = content.lstrip(result[0])
        else:
            news_detail['content'] = content
        news_detail['date'] = re_result[0]
        news_detail['title'] = clean_title
        news_detail['url'] = url
        news_detail['channel'] = source
        return news_detail

    # when the news channel is 'gbiz',we can get news detail by follow function
    def get_gbiz_news(self, url):
        news_detail = {}
        header = 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        res = requests.get(url, params=header)
        res.encoding = res.apparent_encoding
        selector = etree.HTML(res.text)
        soup = BeautifulSoup(res.text, 'html.parser')
        # get news date from url by regular expression
        pattern = re.compile(r'.*?(\d{4}-\d{2}-\d{2}).*?')
        re_result = re.findall(pattern, url)
        # get news channel form url by regular expression
        source_pattern = re.compile(r'http://(.*?).caixin.*?')
        source_result = re.findall(source_pattern, url)
        source = source_result[0]
        # get news title
        title = selector.xpath('//h2[@class="title"]')
        clean_title = title[0].text.strip()
        # get news content
        content = ' '.join([p.text.strip().lstrip('【财新网】') for p in soup.select('#Main_Content_Val p')])
        # Use regular expressions to remove reporter information from the news text
        strip_pattern = re.compile(r'(（.*?）).*')
        result = re.findall(strip_pattern, content)

        if len(result) > 0:
            news_detail['content'] = content.lstrip(result[0])
        else:
            news_detail['content'] = content
        news_detail['date'] = re_result[0]
        news_detail['title'] = clean_title
        news_detail['url'] = url
        news_detail['channel'] = source
        return news_detail


    def get_all_news_details(self):
        all_news_detail = []
        i = 1
        for url in self.all_news_url:
            try:
                source_pattern = re.compile(r'http://(.*?).caixin.*?')
                source_result = re.findall(source_pattern, url)
                source = source_result[0]
                if source == 'gbiz':
                    news_detail = self.get_gbiz_news(url)
                elif source == 'promote':
                    news_detail = self.get_promote_new(url)
                elif source == 'corp':
                    news_detail = self.get_corp_new(url)
                elif source == 'culture':
                    pass
                elif source == 'conferences':
                    pass
                else:
                    news_detail = self.get_news_detail(url)
                all_news_detail.append(news_detail)
            except:
                print(url)
            print('第{}条新闻正在写入'.format(i))
            i += 1
        return all_news_detail


if __name__ == '__main__':

    minpage = 1
    maxpage = 1
    header = 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    base_url = 'http://search.caixin.com/search/search.jsp?special=false&keyword=%E4%BA%AC%E4%B8%9C&channel=0&type=2&sort=1&time=&startDate=&endDate=&page='

    news = GetNews(minpage, maxpage, header, base_url)
    all_news_detail = news.get_all_news_details()
    df = pd.DataFrame(all_news_detail)
    df.to_csv("sample.csv", mode='a', index=False, sep=',', encoding='utf_8_sig')


