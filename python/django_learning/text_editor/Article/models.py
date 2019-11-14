from django.db import models

from ckeditor.fields import RichTextField

from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    sub_title = models.CharField(max_length=50, blank=True, null=True, verbose_name='子标题')
    # body = RichTextField()
    brief = models.CharField(max_length=255)
    content = RichTextUploadingField(verbose_name='正文')

class ArticleContent(models.Model):
    content = RichTextUploadingField(verbose_name='正文')

    
# class Article(models.Model):
#     title = models.CharField(max_length=50, verbose_name='标题')
#     sub_title = models.CharField(max_length=50, blank=True, null=True, verbose_name='子标题')
#     # body = RichTextField()
#     brief = models.CharField(max_length=255)
#     cid = models.ForeignKey('ArticleContent', models.DO_NOTHING, db_column='cid')

# class ArticleContent(models.Model):
#     id = models.IntegerField(primary_key=True)
#     content = RichTextUploadingField(verbose_name='正文')