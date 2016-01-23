#/usr/bin/python
#coding=utf-8
"""测试下redis连接"""
import redis
r = redis.Redis(host="172.17.16.87", port=6380)
r.set("test", "aaa")
print r.get("test")
print r.mget(['gc:pd:697210769'])