# -*- coding: utf-8 -*-
import json
import datetime
import requests
from django.http import JsonResponse
from home_application.models import *
from account.decorators import login_exempt
from common.mymako import render_mako_context
from  common.mymako import render_json
from conf.default import APP_ID, APP_TOKEN, BK_PAAS_HOST
from home_application.esb_helper import cc_search_biz, cc_search_set, run_fast_execute_script, cc_search_host, \
    get_job_instance_log, get_host_ip_list, cc_get_job_detail, run_execute_job, cc_fast_push_file
from django.db.models import Sum, Avg, Q, Count, Max, Min, F
import suds
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def home(request):
    """
    首页
    """
    id = request.GET.get('id')
    return render_mako_context(request, '/home_application/home.html',{ "id":id})


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')


def test(request):
    """
    测试
    """
    return render_mako_context(request, '/home_application/test.html')

def modal(request):
    """
    测试
    """
    return render_mako_context(request, '/home_application/modal.html')

def getJson(request):
    data = [
        {'time': '1月1日',  'cpu': 89.3, 'men': 96.4, 'disk':88},
        {'time': '1月2日',  'cpu': 79.3, 'men': 88.4, 'disk': 78},
        {'time': '1月3日',  'cpu': 88.3, 'men': 78.4, 'disk': 84},
        {'time': '1月4日', 'cpu': 78.3, 'men': 63.4, 'disk': 76},
        {'time': '1月5日',  'cpu': 74.3, 'men': 94.4, 'disk': 79},
        {'time': '1月6日',  'cpu': 85.3, 'men': 87.4, 'disk': 98}
    ]
    return render_json({"result": True,"data": data})
# 返回echarts 图标拼接格式数据
# series 下面的type 表示需要渲染哪种图表类型
# line:折线图   bar:柱状图
def getEchartsJson(request):
    data ={
        "xAxis": ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
        "series": [
            {
                "name": "cpu",
                "type": "line",
                "data": [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
            },
            {
                "name": "men",
                "type": "line",
                "data": [3.6, 6.9, 8.0, 21.4, 23.7, 78.7, 165.6, 152.2, 68.7, 28.8, 7.0, 8.3]
            },
            {
                "name": "disk",
                "type": "bar",
                "data": [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
            }
        ]
    }
    return render_json({"result": True,"data": data})
# 该方法一般不作修改
def search_biz(request):
    data = cc_search_biz(request.user.username)
    return JsonResponse(data)


def search_set(request):
    """
    传递参数
    :param 业务id   biz_id
    :param request:
    :return:
    """
    biz_id = request.GET.get('biz_id')
    data = cc_search_set(biz_id)
    return JsonResponse(data)


def search_host(request):
    """
    :param request:
    传递参数
    :param 业务id   biz_id,
    biz_id,ip_list = ['10.92.190.214','10.92.190.215']
    get请求获取的ip_list，转换成列表，请调用get_host_ip_list
    :return:
    """
    biz_id = request.GET.get('biz_id')
    ip_list = []
    if 'ip' in request.GET:
        ip = request.GET.get('ip')
        ip_list = get_host_ip_list(ip)
    data = cc_search_host(biz_id,ip_list)
    return JsonResponse(data)


def fast_execute_script(request):
    """
    :param request:
    传递参数
    :param 业务id   biz_id,
         ip_list = [
            {
                "bk_cloud_id": 0,
                "ip": "10.92.190.214"
            }
            {
                "bk_cloud_id": 0,
                "ip": "10.92.190.215"
            }
        ]
    :return:
    """
    biz_id = request.GET.get('biz_id')
    script_content = """
         df -h
    """
    ip_list = [
        {
            "bk_cloud_id": 0,
            "ip": "192.168.240.43"
        }
    ]
    data = run_fast_execute_script(biz_id,script_content,ip_list,request.user.username)
    return JsonResponse(data)


def execute_job(request):
    """
    :param request:
    传递参数
    :param 业务id       biz_id,
    :param 作业模板id    job_id,
    :param ip列表     ip_list = [
            {
                "bk_cloud_id": 0,
                "ip": "10.92.190.214"
            }
            {
                "bk_cloud_id": 0,
                "ip": "10.92.190.215"
            }
        ]
    :return:
    """
    biz_id = request.GET.get('biz_id')
    job_id = request.GET.get('job_id')
    ip_list = [
        {
            "bk_cloud_id": 0,
            "ip": "192.168.240.43"
        }
    ]
    data = run_execute_job(biz_id, job_id, ip_list,request.user.username)
    return JsonResponse(data)


def get_log_content(request):
    """
        :param request:
        传递参数
        :param 业务id       biz_id,
        :param 作业实例id    instance_id,
        :return:
        """
    biz_id = request.GET.get('biz_id')
    job_instance_id = request.GET.get('instance_id')
    result = get_job_instance_log(biz_id, job_instance_id,request.user.username)
    data = {
        "data": result
    }
    return JsonResponse(data)


def job_detail(request):
    """
        :param request:
        传递参数
        :param 业务id       biz_id,
        :param 作业实例id    instance_id,
        :return:
        """
    biz_id = request.GET.get('biz_id')
    job_id = request.GET.get('job_id')
    data = cc_get_job_detail(biz_id, job_id, request.user.username)
    return JsonResponse(data)


def fast_push_file(request):
    biz_id = request.GET.get('biz_id')
    file_target_path = "/tmp/"
    target_ip_list = [{
      "bk_cloud_id": 0,
      "ip": "192.168.240.52"
    },
        {
      "bk_cloud_id": 0,
      "ip": "192.168.240.55"
    }
    ]
    file_source_ip_list = [{
            "bk_cloud_id": 0,
            "ip": "192.168.240.43"
        }
    ]
    file_source = ["/tmp/test12.txt","/tmp/test123.txt"]
    data = cc_fast_push_file(biz_id, file_target_path, file_source, target_ip_list, file_source_ip_list,request.user.username)
    return JsonResponse(data)


#作业接口
def main(request):
    """
    主页
    """
    return render_mako_context(request, '/home_application/main.html')

def second(request):
    """
    测试
    """
    ip = request.GET.get("ip")
    biz_id = request.GET.get("biz_id")
    yun_id = request.GET.get("yun_id")
    return render_mako_context(request, '/home_application/second.html',{ "ip":ip,"biz_id":biz_id,"yun_id":yun_id})

@login_exempt
def mytest(request):
    name = request.user.username
    return render_json({"result":u"OK","username":name})

#获取业务列表
@login_exempt
def get_biz_list(request):
    try:
        biz_list = []
        result = cc_search_biz()
        if result["result"]:
            biz_list = result["data"]["info"]
        return render_json({"result":True,"data":biz_list})
    except Exception, e:
        return render_json({"result":False,"message":u"系统出错，请联系管理员","data":str(e)})

#获取业务下的集群
def get_set_list(request):
    try:
        set_list = []
        biz = request.GET.get("biz_id")
        result = cc_search_set(biz)
        if result["result"]:
            set_list = result["data"]["info"]
        return render_json({"result":True,"data":set_list})
    except Exception, e:
        return render_json({"result":False,"message":u"系统出错，请联系管理员","data":str(e)})

#获取业务下主机
@login_exempt
def get_host_list(request):
    try:
        host_list = []
        biz_id = int(request.GET.get("biz_id"))
        set_id = int(request.GET.get("set_id"))
        ip_list = []
        result = cc_search_host(biz_id,ip_list,set_id)
        if result["result"]:
            data_list = result["data"]["info"]
            for item in data_list:
                host_list.append(item["host"])
        return render_json({"result":True,"data":host_list})
    except Exception, e:
        return render_json({"result":False,"message":u"系统出错，请联系管理员","data":str(e)})
    
#新增主机
@login_exempt
def add_host(request):
    try:
        biz_id = int(request.GET.get("biz_id"))
        set_id =  int(request.GET.get("set_id"))
        ip_list = []
        ip = request.GET.get("ip")
        ip_list.append(ip)
        result = cc_search_host(biz_id,ip_list,set_id)
        if result["result"] and result["data"]["count"] >0:
            hosts = result["data"]["info"][0]["host"]
            biz = result["data"]["info"][0]["biz"]
            new_host = host()
            new_host.ip = hosts["bk_host_innerip"]
            host.objects.filter(ip=new_host.ip).delete()
            new_host.name = hosts["bk_host_name"]
            new_host.yun = hosts["bk_cloud_id"][0]["bk_inst_name"]
            new_host.system = hosts["bk_os_name"]
            new_host.yun_id = str(hosts["bk_cloud_id"][0]["bk_inst_id"])
            new_host.biz = biz[0]["bk_biz_name"]
            new_host.biz_id = str(biz[0]["bk_biz_id"])
            host_list = host.objects.filter(ip=new_host.ip)
            if host_list.count()>0:
                new_host.id = host_list[0].id
            new_host.save()
            return render_json({"result":True,"data":u"新增成功！"})
        else:
            return render_json({"result":True,"data":u"新增失败！"})
    except Exception, e:
        return render_json({"result":False,"message":u"系统出错，请联系管理员","data":str(e)})



@login_exempt
def get_db_host_list(request):
    try:
        ip = request.GET.get("ip")
        data_list = list(host.objects.filter(ip__contains=ip).values())
        for item in data_list:
            item["when_created"] = ""
        return render_json({"result":True,"data":data_list})
    except Exception, e:
        return render_json({"result":False,"message":u"系统出错，请联系管理员","data":str(e)})
#获取详情
def get_host_detail(request):
    try:
        id = int(request.GET.get("id"))
        host_list = list(host.objects.filter(id=id).values())
        if len(host_list)>0:
            hosts = host_list[0]
        else:
            hosts = {}
        return render_json({"result":True,"data":hosts})
    except Exception, e:
        return render_json({"result":False,"message":u"系统出错，请联系管理员","data":str(e)})
#修改备注
def update_host_other(reuqest):
    try:
        id = int(reuqest.GET.get("id"))
        other = reuqest.GET.get("other")
        myhost = host.objects.get(id=id)
        myhost.other = other
        myhost.save()
        return render_json({"result":True,"data":u"修改成功"})
    except Exception, e:
        return render_json({"result":False,"message":u"系统出错，请联系管理员","data":str(e)})
@login_exempt
def del_host(request):
    try:
        ip = request.GET.get("ip")
        host.objects.filter(ip=ip).delete()
        return render_json({"result":True,"data":u"删除成功"})
    except Exception, e:
        return render_json({"result":False,"message":u"系统出错，请联系管理员","data":str(e)})

@login_exempt
def get_fuzai(request):
    try:
        ip = request.GET.get("ip")
        biz_id = int(request.GET.get("biz_id"))
        yun_id = int(request.GET.get("yun_id"))
        ip_list = [{
            "ip":ip,
            "bk_cloud_id":yun_id
        }]
        strip = """
        #!/bin/bash
        cat /proc/loadavg
        """
        result = run_fast_execute_script(biz_id,strip,ip_list)
        if result["result"]:
            job_id = int(result["data"])
            log = get_job_instance_log(biz_id,job_id)[0]
            if log["is_success"]:
                logs = log["log_content"].split(" ")[1]
            else:
                logs = 0

        return render_json({"result":True,"data":logs})
    except Exception, e:
        return render_json({"result":False,"message":u"系统出错，请联系管理员","data":str(e)})

@login_exempt
def get_disk_rate(request):
    try:
        ip = request.GET.get("ip")
        biz_id = int(request.GET.get("biz_id"))
        yun_id = int(request.GET.get("yun_id"))
        ip_list = [{
            "ip":ip,
            "bk_cloud_id":yun_id
        }]
        strip = """
        #!/bin/bash
        free -m
        """
        result = run_fast_execute_script(biz_id,strip,ip_list)
        data = {
                    "title": '',
                    "series": [
                        { 'name': '已使用', 'value': 0 },
                        { 'name': '未使用', 'value': 0 }
                    ]
                }
        if result["result"]:
            job_id = int(result["data"])
            log = get_job_instance_log(biz_id,job_id)[0]
            if log["is_success"]:
                logs = log["log_content"].split("\n")[1]
                datas = list(filter(None,logs.split(" ")))
                total = int(datas[1])
                used = int(datas[2])
                data = {
                    "title": '',
                    "series": [
                        { 'name': '已使用', 'value': used },
                        { 'name': '未使用', 'value': total-used }
                    ]
                }
        return render_json({"result":True,"data":data})
    except Exception, e:
        return render_json({"result":False,"message":u"系统出错，请联系管理员","data":str(e)})

@login_exempt
def get_dict(request):
    try:
        ip = request.GET.get("ip")
        biz_id = int(request.GET.get("biz_id"))
        yun_id = int(request.GET.get("yun_id"))
        ip_list = [{
            "ip":ip,
            "bk_cloud_id":yun_id
        }]
        strip = """
        #!/bin/bash
        df -h
        """
        result = run_fast_execute_script(biz_id,strip,ip_list)
        data_list = []
        if result["result"]:
            job_id = int(result["data"])
            log = get_job_instance_log(biz_id,job_id)[0]
            if log["is_success"]:
                logs = log["log_content"].split("\n")[1:-1]
                for item in logs:
                    datas = list(filter(None,item.split(" ")))
                    dl = {}
                    dl["filesystem"] = datas[0]
                    dl["size"] = datas[1]
                    dl["used"] = datas[2]
                    dl["avail"] = datas[3]
                    dl["use"] = datas[4]
                    dl["mounton"] = datas[5]
                    data_list.append(dl)
        return render_json({"result":True,"data":data_list})
    except Exception, e:
        return render_json({"result":False,"message":u"系统出错，请联系管理员","data":str(e)})

@login_exempt
def get_fuzai_list(request):
    try:
        ip = request.GET.get("ip")
        start_time = request.GET.get("start_time")
        end_time = request.GET.get("end_time")
        query = Q()
        query.connector = "AND"
        if not start_time and not end_time:
            time_now = datetime.datetime.now()
            end_time = time_now.strftime("%Y-%m-%d %H:%M:%S")
            start_time = (time_now - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        query.children.append(("when_created__lte",end_time))
        query.children.append(("when_created__gte",start_time))
        data_list = list(FuZai.objects.filter(query).filter(ip=ip).values("when_created","value"))
        time_list = []
        value_list = []
        for item in data_list:
            time_list.append(item["when_created"].strftime("%Y-%m-%d %H:%M:%S"))
            value_list.append(item["value"])
        lineData = {
              "xAxis":time_list,
                "series" : [
                    {
                        "name":"负载值",
                        "type":"line",
                        "data":value_list
                    }]
            }
        return render_json({"result":True,"data":lineData})
    except Exception, e:
        return render_json({"result":False,"message":u"系统出错，请联系管理员","data":str(e)})

#二次模拟

def next(request):
    """
    主页
    """
    return render_mako_context(request, '/home_application/next.html')
def haha(request):
    """
    主页
    """
    ip = request.GET.get("ip")
    biz_id = request.GET.get("biz_id")
    yun_id = request.GET.get("yun_id")
    return render_mako_context(request, '/home_application/haha.html',{ "ip":ip,"biz_id":biz_id,"yun_id":yun_id})

def test_web(request):
    try:
        url = "http://localhost:53973/WebService.asmx?wsdl"
        client = suds.client.Client(url)
        print(client)
        key = client.factory.create('typekey')
        key.name = "haha"
        key.user = 1
        key.age = "haha"
        aa = client.service.GetTypekey(key)
        print(aa)  
        return render_json({"reuslt":True})
    except Exception, e:
        return render_json({"reuslt":str(e)})
