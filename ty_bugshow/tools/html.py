#!/bin/python2.7
#coding=utf-8
import re,sys
'''html页面内容处理'''
def getAllUrls(html):
    '''获取所有的url链接'''
    urls = re.findall(r'<a.*?href="(.*?)".*?>(.*?)</a>', html)
    return urls