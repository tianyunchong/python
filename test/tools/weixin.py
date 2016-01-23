#/bin/python2.7
#coding=utf-8
"""测试"""
import sys, os, json
import httplib
npos = int(__file__.index("trunk"))
path = __file__
root_path = path[0:npos]
sys.path.append(os.path.join(root_path, "trunk"))
from library import http
import datetime
appid = "wxf0f539e388f1182c"
appsecret = "b6298d37405b565c4fea911160967dee"
url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid="+appid+"&secret="+appsecret
data = http.getRemote(url)
if not data:
    print "无法获取到access_token"
    sys.exit()
data = json.loads(data)
access_token = data["access_token"]
#print access_token
url = "https://api.weixin.qq.com/cgi-bin/user/get?access_token="+access_token
#获取用户信息, openid
userData = http.getRemote(url)
userData = json.loads(userData)
openid = userData["data"]["openid"][0]
if not openid:
    print "获取openid失败"
    sys.exit()
print openid
conn = httplib.HTTPConnection("api.weixin.qq.com:80")#微信接口链接
headers = {"Content-type":"application/json"} #application/x-www-form-urlencoded
#开始查询登陆信息
url = "http://192.168.10.10/api.php?name=%E5%BC%A0%E9%98%B3%E5%8D%8E"
loginData = http.getRemote(url)
if not loginData:
    sys.exit("无法获取到登陆信息")
loginData = json.loads(loginData)
weeks = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
dayOfWeek = datetime.datetime.now().weekday()
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
firstDe = "昨日时间:"+str(yesterday)+"\n"
firstDe = "昨日:"+weeks[dayOfWeek]+"\n"
for item in loginData[0:4]:
    firstDe = firstDe + item["date"].encode("utf-8")+"  签到时间:"+item["time"].encode("utf-8")+"\n"
params = ({'touser' : openid,#用户openid
    'template_id' : 'QDAOxWTzaGYRQ1sX0l-7ZkAPr1_yyirkBAm8Fow0HNo',#模板消息ID
    'url' : 'http://oa.gongchang.cn',#跳转链接
    "topcolor" : "#667F00",#颜色
    "data" : {#模板内容
        "first" : {"value" : firstDe, "color" : "#173177"},
    }
})
conn.request("POST", "/cgi-bin/message/template/send?access_token="+access_token, json.JSONEncoder().encode(params), headers)#推送消息请求
response = conn.getresponse()
data = response.read()#推送返回数据
if response.status == 200:
    print 'success'
    print data
else:
    print 'fail'
conn.close()
