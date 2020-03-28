from django.shortcuts import render, get_object_or_404
import markdown
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

# Create your views here.
from .models import Post, Category, Tag


def index(request):
    # return render(request, 'blog/index.html', context={
    #     'title': '我的博客首页',
    #     'welcome': '欢迎访问我的博客首页'
    # })
    post_list = Post.objects.all().order_by('-created_time')  # -表示逆序
    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 在模板中显示{{ post.body }},就不再是原始的Markdown文本了,而是解析过后的HTML文本
    # post.body = markdown.markdown(post.body,
    md = markdown.Markdown(  # 再页面任何位置插入目录
        extensions=[
            'markdown.extensions.extra',  # 包含很多基础拓展
            'markdown.extensions.codehilite',  # 语法高亮拓展
            # 'markdown.extensions.fenced_code',
            # 'markdown.extensions.toc', # 允许自动生成目录
            TocExtension(slugify=slugify),  # 美化标题的锚点
        ])
    post.body = md.convert(post.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m else ''
    return render(request, 'blog/detail.html', context={'post': post})


# 使用了模型管理器(objects)的filter方法,created_time是达特对象,有year,month属性
# 通常使用date.year和date.month调用属性,但是在变量中引用django要求使用双下划线date__year和date__month
# 由于归档页面和首页展示文章的形式是一样的,因此直接复用了index.html模板
def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month,
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def tag(request, pk):
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
