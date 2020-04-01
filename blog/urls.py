# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2020/3/25 15:57
# @Author   : tangky
# @Site     : 
# @File     : urls.py
# @Software : PyCharm


from django.urls import path
from . import views

# 视图函数命名空间,告诉django这个urls.py属于blog应用
app_name = 'blog'
urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.IndexView.as_view(), name='index'),
    # <int:pk>django路由匹配规则的特殊写法,匹配路由中的数字并传递给views.detail函数
    # path('posts/<int:pk>/', views.detail, name='detail'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    # path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    path('archives/<int:year>/<int:month>/', views.ArchiveView.as_view(), name='archive'),
    # path('categories/<int:pk>/', views.category, name='category'),
    path('categories/<int:pk>/', views.CategoryView.as_view(), name='category'),
    # path('tags/<int:pk>/', views.tag, name='tag'),
    path('tags/<int:pk>/', views.TagView.as_view(), name='tag'),
    path('search/', views.search, name='search'),
]
