# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2020/3/27 10:14
# @Author   : tangky
# @Site     : 
# @File     : urls.py.py
# @Software : PyCharm

from django.urls import path

from . import views


app_name = 'comments'
urlpatterns = [
    path('comment/<int:post_pk>', views.comment, name='comment'),
]