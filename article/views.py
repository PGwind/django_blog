from django.shortcuts import render
from .models import ArticlePost
import markdown


# Create your views here.

def article_list(request):
    # 取出所有博客文章
    articles = ArticlePost.objects.all()
    # 需要传递给模板（templates）的对象
    context = {'articles': articles}
    # render函数：载入模板，并返回context对象
    return render(request, 'article/list.html', context)


def article_detail(request, article_id):
    article = ArticlePost.objects.get(id=article_id)

    # 将markdown语法渲染成html样式
    article.body = markdown.markdown(article.body,
    extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
    ])

    context = {'article': article}
    return render(request, 'article/detail.html', context)
