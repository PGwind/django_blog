from django.urls import path
from . import views
app_name = 'article'

urlpatterns = [
    # path函数将url映射到视图
    # 文章列表
    path('article-list/', views.article_list, name='article_list'),

    # 文章详情
    path('article-detail/<int:article_id>/', views.article_detail, name='article_detail'),

    # 写文章
    path('article-create/', views.article_create, name='article_create'),

    # 删除文章
    path('article-safe-delete/<int:article_id>/', views.article_safe_delete, name='article_safe_delete'),

    # 更新文章
    path('article-update/<int:article_id>/', views.article_update, name='article_update'),

]