from django.urls import path
from . import views
app_name = 'article'

urlpatterns = [
    #path函数将url映射到视图
    #文章列表
    path('article-list/', views.article_list, name='article_list'),

    # 文章详情
    path('article-detail/<int:article_id>/', views.article_detail, name='article_detail'),
]