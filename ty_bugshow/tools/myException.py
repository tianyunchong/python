#!/bin/python2.7
#coding=utf-8
'''
异常处理类
'''
class MyException(Exception):
    def __init__(self, reason):
            Exception.__init__(self)
            print reason