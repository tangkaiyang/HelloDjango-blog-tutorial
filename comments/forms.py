# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2020/3/26 16:59
# @Author   : tangky
# @Site     : 
# @File     : forms.py
# @Software : PyCharm
from django import forms
from .models import Comment


# django的表单类必须继承自forms.Form类或者forms.ModelForm类
# 如果表单对应有个数据库模型,使用ModelForm类会简单很多
# django会根据表单类的定义自动生成表单的HTML代码
class CommentForm(forms.ModelForm):
    class Meta:
        # 表明这个表单对应的数据库模型是Comment类
        model = Comment
        fields = ['name', 'email', 'url', 'text']
