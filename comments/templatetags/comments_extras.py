# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2020/3/26 17:06
# @Author   : tangky
# @Site     : 
# @File     : comments_extras.py
# @Software : PyCharm
from django import template
from ..forms import CommentForm

register = template.Library()


@register.inclusion_tag('comments/inclusions/_form.html', takes_context=True)
def show_comment_form(context, post, form=None):
    if not form:
        form = CommentForm()
    return {
        'form': form,
        'post': post,
    }


@register.inclusion_tag('comments/inclusions/_list.html', takes_context=True)
def show_comments(context, post):
    # Comment和Post通过ForeignKey关联的
    # post.comment_set.all()等价于Comment.objects.filter(post=post)
    comment_list = post.comment_set.all().order_by('-created_time')
    comment_count = comment_list.count()
    return {
        'comment_count': comment_count,
        'comment_list': comment_list,
    }