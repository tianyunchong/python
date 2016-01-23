# /usr/bin/python
# coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from ty_index import forms
import time, json
from tools import http, html
from ty_bugshow.models import *
from django.core.exceptions import ObjectDoesNotExist
import sys

def test(request):
    params = {
        "tdk": {
            "title": "链接分析"
        },
        "css": [],
    }
    return render_to_response("index/index.html", params)


def add(request):
    params = {
        'tdk': {
            "title": "增加链接-bug分析"
        },
        "css": [
            ["css", "/static/css/index/urls_add.css"]
        ],
        "successTip": False,
        "failureTip": "",
    }
    return render_to_response("index/add.html", params)


def addpost(request):
    params = {
        'tdk': {
            "title": "增加链接-bug分析"
        },
        "css": [
            ["css", "/static/css/index/urls_add.css"]
        ],
        "successTip": True,
        "failureTip": "",
    }
    if request.method != "POST":
        params["failureTip"] = "提交失败!"
        params["successTip"] = False
        return render_to_response("index/add.html", params)
    f = forms.UrladdForm(request.POST)
    if not f.is_valid():
        params["failureTip"] = "提交失败, 请检查提交的链接"
        params["successTip"] = False
        return render_to_response("index/add.html", params)
    cleand = f.cleaned_data
    try:
        """存在记录"""
        bm = BugUrls.objects.get(url=cleand["url"])
        params["failureTip"] = "提交失败, 数据库中已经存在该链接!"
        params["successTip"] = False
    except BugUrls.DoesNotExist:
        """不存在记录"""
        bm = BugUrls(url=cleand["url"], updatetime=int(time.time()))
        bm.save()
    except:
        params["failureTip"] = "提交失败, 数据插入失败!"
        params["successTip"] = False
        """其他错误"""
    return render_to_response("index/add.html", params)


def dele(request):
    """检测链接删除"""
    id = int(request.GET.get("id", 0))
    try:
        bm = BugUrls.objects.get(id=id)
        bm.delete()
        return HttpResponseRedirect("/index/urls/")
    except BugUrls.DoesNotExist:
        return HttpResponse("不存在对应id的链接")
    except:
        return HttpResponse("信息删除失败")


def analy(request):
    """链接的检测"""
    id = int(request.GET.get("id", 0))
    if id < 1:
        return HttpResponse("未知的id，无法检测")
    try:
        bm = BugUrls.objects.get(id=id)
    except:
        return HttpResponse("未知信息，无法进行分析检测")
    params = {
        "tdk": {
            "title": "分析链接-bug分析"
        },
        "js": [
            "/static/js/analy/yibu.js",
        ],
        "urlInfo": bm
    }
    return render_to_response("index/analy.html", params)


def analyinit(request):
    res = {"status": False, "message": "测试下"}
    id = int(request.GET.get("id", 0))
    if id < 1:
        res["message"] = "未知的id，无法检测"
        return HttpResponse(json.dumps(res))
    try:
        bm = BugUrls.objects.get(id=id)
    except:
        res["message"] = "未知信息，无法进行分析检测"
        return HttpResponse(json.dumps(res))
    anurl = BugAnaly.objects.filter(urlid=id)
    if anurl:
        res["message"] = "页面链接已经解析"
        res["status"] = True
        return HttpResponse(json.dumps(res))
    url = bm.url
    phtml = http.getRemote(url)
    unihtml = http.convertUnicode(phtml)
    urllist = html.getAllUrls(unihtml)
    if not urllist:
        res["message"] = "当前页面无法获取到链接"
        return HttpResponse(json.dumps(res))
    for url in urllist:
        #开始将匹配到链接入库
        anay = BugAnaly(urlid=id, url=url[0], text=url[1], status = 0, uptime=0)
        anay.save()
    res["status"] = True
    res["message"] = "所有链接已经抓取并存储"
    return HttpResponse(json.dumps(res))

def analylist(request):
    """分析页面列表"""
    params = {
        'tdk': {
            "title": "分析结果列表-bug分析"
        },
        "css": [
            ['css', '/static/css/index/analy_urls.css']
        ]
    }
    id = int(request.GET.get("id", 0))
    if id < 1:
        return HttpResponse("未知页面")
    urlInfo = BugUrls.objects.filter(id=id)
    if not urlInfo:
        return HttpResponse("未知页面")
    #开始查询出所有的页面信息
    page_size = 10
    after_range_num = 5
    before_range_num = 6
    try:
        page = int(request.GET.get("page", 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    urls = BugAnaly.objects.filter(urlid=id)
    paginator = Paginator(urls, page_size)
    try:
        urls = paginator.page(page)
    except(EmptyPage, InvalidPage, PageNotAnInteger):
        urls = paginator.page(1)
    if page >= after_range_num:
        page_range = paginator.page_range[page - after_range_num:page + before_range_num]
    else:
        page_range = paginator.page_range[0:int(page) + before_range_num]
    params["page_objects"] = urls
    params["page_range"] = page_range
    params["id"] = id
    return render_to_response("index/analy_urls.html", params)

def list(request):
    """分析过的页面的urls"""
    params = {
        'tdk': {
            "title": "分析链接列表-bug分析"
        },
        "css": [
            ['css', '/static/css/index/urls.css']
        ]
    }
    page_size = 10
    after_range_num = 5
    before_range_num = 6
    try:
        page = int(request.GET.get("page", 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    urls = BugUrls.objects.all()
    paginator = Paginator(urls, page_size)
    try:
        urls = paginator.page(page)
    except(EmptyPage, InvalidPage, PageNotAnInteger):
        urls = paginator.page(1)
    if page >= after_range_num:
        page_range = paginator.page_range[page - after_range_num:page + before_range_num]
    else:
        page_range = paginator.page_range[0:int(page) + before_range_num]
    params["page_objects"] = urls
    params["page_range"] = page_range
    return render_to_response("index/urls.html", params)
