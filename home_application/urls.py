# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'home'),
    (r'^dev-guide/$', 'dev_guide'),
    (r'^contactus/$', 'contactus'),
    (r'^test/$', 'test'),
    (r'^modal/$', 'modal'),
    (r'^api/getJson/$', 'getJson'),
    (r'^api/getEchartsJson/$', 'getEchartsJson'),

    (r'^search_biz/$', 'search_biz'),
    (r'^search_set/$', 'search_set'),
    (r'^search_host/$', 'search_host'),
    (r'^fast_execute_script/$', 'fast_execute_script'),
    (r'^execute_job/$', 'execute_job'),
    (r'^job_detail/$', 'job_detail'),
    (r'^get_log_content/$', 'get_log_content'),
    (r'^fast_push_file/$', 'fast_push_file'),
#作业
    (r'^main/$', 'main'),
    (r'^second/$', 'second'),
    (r'^api/test/$', 'mytest'),
    (r'^api/get_biz_list/$', 'get_biz_list'),
    (r'^api/get_set_list/$', 'get_set_list'),
    (r'^api/get_host_list/$', 'get_host_list'),
    (r'^api/get_host_detail/$', 'get_host_detail'),
    (r'^api/update_host_other/$', 'update_host_other'),
    (r'^api/add_host/$', 'add_host'),
    (r'^api/get_db_host_list/$', 'get_db_host_list'),
    (r'^api/del_host/$', 'del_host'),
    (r'^api/get_fuzai/$', 'get_fuzai'),
    (r'^api/get_disk_rate/$', 'get_disk_rate'),
    (r'^api/get_dict/$', 'get_dict'),
    (r'^api/get_fuzai_list/$', 'get_fuzai_list'),
#二次模拟
    (r'^next/$', 'next'),
    (r'^haha/$', 'haha'),
    (r'^api/test_web/$', 'test_web'),

)
