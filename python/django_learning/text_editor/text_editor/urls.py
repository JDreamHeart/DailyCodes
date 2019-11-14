"""text_editor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings

from Article.views import release

from websk.views import websk

from websk.consumers import webConsumer;

from ckeditor_uploader import views

from django.views.decorators.cache import never_cache

urlpatterns = [
    path('admin/', admin.site.urls),
    path('release/', release),
    url(r'^ckeditor/upload/', views.upload, name='ckeditor_upload'),
    url(r'^ckeditor/browse/', never_cache(views.browse), name='ckeditor_browse'),
    path('websk/', websk),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #没有这一句无法显示上传的图片
