from django.contrib import admin
from .models import ArticlePost
from .models import ArticleColumn

# Register your models here.
# 用户注册
admin.site.register(ArticlePost)

# 文章栏目
admin.site.register(ArticleColumn)
