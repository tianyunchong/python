#!/usr/bin/python
# coding=utf-8
"""使用mysql测试下汉字转拼音strtr替换方案"""
import MySQLdb
import sys
import time


class Mysql:
    conn = ""
    cur = ""

    def __init__(self, db):
        """初始化mysql链接"""
        try:
            self.conn = MySQLdb.connect(host=db[0], user=db[1], passwd=db[2], port=db[3])
            self.cur = self.conn.cursor()
        except MySQLdb.Error, e:
            print "mysql error%d:%s\n" % (e.args[0], e.args[1])
            sys.exit()

    def findone(self, sql):
        """查询单条的数据"""
        self.cur.execute(sql)
        rs = self.cur.fetchone()
        return rs

    def findall(self, sql):
        """查询多条的数据"""
        self.cur.execute(sql)
        return self.cur.fetchall()

    def query(self, sql):
        pass

    def close(self):
        """关闭数据库链接"""
        self.cur.close()
        self.conn.close()

num = 30
while num > 0:
    start = time.clock()
    db = ['192.168.8.18', 'root', 'gc7232275', 3306]
    str = u"此方法返回当前处理器时间作为浮点"
    li = []
    for i in range(len(str)):
        li.append(str[i])
    mysql = Mysql(db)
    rs = mysql.findone("select pinyin from tianyunzi.pinyin where keyword = '%s' limit 1" % str)
    if rs:
        print rs
        sys.exit()
    sql = "select keyword, pinyin from tianyunzi.pinyin where keyword in ('"+r"','".join(li)+"') limit 50"
    rs = mysql.findall(sql)
    mysql.close()
    for item in rs:
        str = str.replace(item[0].decode("utf-8"), item[1])
    print str
    end = time.clock()
    print("The function run time is : %.03f seconds" %(end-start))
    num = num - 1
