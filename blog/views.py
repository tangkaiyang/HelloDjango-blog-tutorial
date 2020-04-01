import re

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.utils.text import slugify
from django.views.generic import ListView, DetailView
from django.contrib import messages

import markdown
from markdown.extensions.toc import TocExtension
from pure_pagination import PaginationMixin

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

    # 阅读量+1
    post.increase_views()
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


# 使用类视图
class IndexView(PaginationMixin, ListView):
    # 指定获取的模型
    model = Post
    # 指定视图渲染的模板
    template_name = 'blog/index.html'
    # 指定获取的模型列表数据保存的变量名,这个变量名会传递给模板
    context_object_name = 'post_list'
    # 一般通过django.core.paginator.Paginator完成分页功能
    # ListView只需调用paginate_by
    paginate_by = 10


class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class ArchiveView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        return super(ArchiveView, self).get_queryset().filter(created_time__year=year,
                                                              created_time__month=month,
                                                              ).order_by('-created_time')


class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag).order_by('-created_time')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写get方法的目的是因为每当文章被访问一次,就得将文章的阅读量+1
        # get方法返回的是一个HttpResponse实例
        # 之所以需要先调用父类的get方法,是因为只有当get方法被调用后,
        # 才有self.object属性,其值为Post模型的实例,即被访问的文章post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量+1
        # 注意self.object的值就是被访问的文章post
        self.object.increase_views()

        # 视图必须返回一个HttpResponse对象
        return response

    def get_object(self, queryset=None):
        # 覆写get_object方法的目的是因为需要对post的body值进行渲染
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 记得在顶部引入TocExtension和slugify
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)

        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m else ''

        return post


def search(request):
    q = request.GET.get('q')
    if not q:
        error_msg = '请输入搜索关键词'
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blog:index')
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'post_list': post_list})