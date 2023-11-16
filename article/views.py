from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ArticlePost, ArticleColumn
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from comment.models import Comment
import markdown
# 引入评论表单
from comment.forms import CommentForm
from django.views import View

# Create your views here.

# 文章列表
def article_list(request):
    # 搜索
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    # 初始化查询集
    article_list = ArticlePost.objects.all()

    # 搜索查询集
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        # 将 search 参数重置为空
        search = ''

    # 栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    # 标签查询集
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    # 查询集排序
    if order == 'total_views':
        # 按热度排序博文
        article_list = article_list.order_by('-total_views')

    # 每页显示 1 篇文章
    paginator = Paginator(article_list, 3)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    # 需要传递给模板（templates）的对象
    context = {
        'articles': articles,
        'order': order,
        'search': search,
        'column': column,
        'tag': tag,
    }
    # render函数：载入模板，并返回context对象
    return render(request, 'article/list.html', context)


# 单个文章页面
def article_detail(request, article_id):
    article = ArticlePost.objects.get(id=article_id)

    # 取出文章评论
    comments = Comment.objects.filter(article=article_id)
    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])

    # 修改 Markdown 语法渲染
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)

    # 引入评论表单
    comment_form = CommentForm()
    # 需要传递给模板的对象
    context = {
        'article': article,
        'toc': md.toc,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'article/detail.html', context)


# 写文章
@login_required(login_url='/userprofile/login/')
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据但不提交到数据库
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=request.user.id)
            # 栏目
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            # 将新文章保存到数据库
            new_article.save()
            # tags表单,保存tags多对多关系
            article_post_form.save_m2m();
            # 完成后返回到文章列表
            return redirect("article:article_list")
        # 如果数据不合法
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单实例
        article_post_form = ArticlePostForm()
        # 栏目
        columns = ArticleColumn.objects.all()
        # 赋值上下文
        context = {'article_post_form': article_post_form, 'columns': columns}
        # 返回模板
        return render(request, 'article/create.html', context)


# 删除文章
@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, article_id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=article_id)

        # 过滤非作者的用户
        if request.user != article.author:
            return HttpResponse("抱歉，你无权修改这篇文章。")

        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")


# 更新文章
@login_required(login_url='/userprofile/login/')
def article_update(request, article_id):
    """
     更新文章的视图函数
     通过POST方法提交表单，更新titile、body字段
     GET方法进入初始表单页面
     id： 文章的 id
     """

    # 获取文章id
    article = ArticlePost.objects.get(id=article_id)

    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")

    # 判断用户是否为POST提交表单数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型要求
        if article_post_form.is_valid():
            # 保存新写入的title、body、column数据
            article.title = request.POST['title']
            article.body = request.POST['body']

            # 文章栏目
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None

            # 文章头图
            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')

            # 文章标签
            article.tags.set(request.POST.get('tags').split(','), clear=True)

            article.save()
            # 完成后返回到修改的文章中 (这里article_id不能修改)
            return redirect("article:article_detail", article_id=article_id)
        # 如果数据不合法
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户GET请求数据
    else:
        # 创建表单实例
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {
            'article': article,
            'article_post_form': article_post_form,
            'columns': columns,
            'tags': ','.join([x for x in article.tags.names()]),
        }
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)


# 点赞数 +1
class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        article = ArticlePost.objects.get(id=kwargs.get('id'))
        article.likes += 1
        article.save()
        return HttpResponse('success')
