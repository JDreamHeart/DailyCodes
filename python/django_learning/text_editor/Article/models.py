from django.db import models

from ckeditor.fields import RichTextField

from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=50)
    # body = RichTextField()
    content = RichTextUploadingField(verbose_name='正文')

class Post(models.Model):
    content = RichTextUploadingField(verbose_name='正文')