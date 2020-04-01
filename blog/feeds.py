# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2020/4/1 18:41
# @Author   : tangky
# @Site     : 
# @File     : feeds.py
# @Software : PyCharm
from django.contrib.syndication.views import Feed


from .models import Post


class AllPostsRssFeed(Feed):
    # 显示在聚合阅读器上的标题
    title = 'HelloDjango-blog-tutorial'
    # 通过聚合阅读器跳转到网站地址
    link = "/"
    # 显示在聚合阅读器上的描述信息
    description = "HelloDjango-blog-tutorial 全部文章"
    # 需要显示的内容条目
    def items(self):
        return Post.objects.all()

    # 聚合器中显示的内容条目的标题
    def item_title(self, item):
        return "[%s] %s" % (item.category, item.title)

    # 聚合器中显示的内容条目的描述
    def item_description(self, item):
        return item.body_html
