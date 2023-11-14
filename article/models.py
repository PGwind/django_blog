from django.db import models
#导入内建的User模型
from django.contrib.auth.models import User
#timezone用于处理时间相关事务
from django.utils import timezone

# Create your models here.
class ArticlePost(models.Model):
    #文章作者   on_delete指定数据删除方式
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    #文章标题   models.CharField为字符串字段，用于保存较短的字符串，如标题
    title = models.CharField(max_length=100);

    #文章正文   保存大量文本
    body = models.TextField(default='')

    #文章创建时间    default=timezone.now 指定其在创建数据时默认写入当前时间
    created = models.DateTimeField(default=timezone.now)

    #文章更新时间     auto_now=true 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)

    #内部类 class Meta 用于给model定义元数据
    class Meta:
        #ordering 指定模型返回的数据的排列顺序
        #'-created' 表明数据应该以倒序排列
        ordering = ('-created',)

    #函数_str_定义当调用对象的str()方法时返回值内容
    def _str_(self):
        #return self.title 返回文章标题
        return self.title