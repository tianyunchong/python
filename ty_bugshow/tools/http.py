# /bin/python2.7
# coding=utf-8
# 网络处理
import urllib2
import socket
import chardet
from tools import myException

def getRemote(url):
    """获取远程html内容"""
    try:
        req = urllib2.urlopen(url)

    except urllib2.URLError:
        return ''
    html = req.read()
    req.close()
    del (req)
    return html


def convertUnicode(html):
    '''将未知编码的html内容转换成unicde编码'''
    if not html:
        return ""
    encodeDict = chardet.detect(html)
    if encodeDict['encoding'] == 'utf-8' or encodeDict['encoding'] == 'UTF-8':
        return html.decode('utf-8', 'ignore')
    elif encodeDict['encoding'] == 'gbk' or encodeDict['encoding'] == 'GBK':
        return html.decode('gbk', 'ignore')
    elif encodeDict['encoding'] == 'gb2312' or encodeDict['encoding'] == 'GB2312':
        return html.decode('gb2312', 'ignore')
    else:
        raise myException.myException, 'uncatch coding!'
