#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Ellis"
# Date: 2017/11/10

import requests
from gevent import monkey;monkey.patch_all()
from gevent.pool import Pool
from bs4 import BeautifulSoup
import gevent
import json


def get_poetry(url):
    """爬取诗句，作者，题目"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    poems = soup.select('.sons')[0].select('.cont')
    l = []
    for poem in poems:
        content = poem.find_all('a')[0].text
        message = poem.find_all('a')[1].text

        author = message.split('《')[0]
        poem_title = message.split('《')[1].split('》')[0]
        data = {'author_name':author,'poem_title':poem_title,'content':content}
        l.append(data)
    return l


def get_url(i):
    url = 'http://so.gushiwen.org/mingju/Default.aspx?p=%s' % i
    return url


def get_save_poem():

    print('start to get poem....')
    p = Pool(10)
    obj_lists = []
    poem_message = []
    for i in range(1, 50):

        g = p.spawn(get_poetry,get_url(i))
        obj_lists.append(g)

    gevent.joinall(obj_lists)

    for g in gevent.joinall(obj_lists):
        l = g.value
        poem_message.extend(l)
    print('end.')
    return poem_message


if __name__ == '__main__':
    get_save_poem()