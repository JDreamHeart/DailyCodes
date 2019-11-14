from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.forms import CharField, ModelForm;
from django.forms.widgets import HiddenInput

from Article import models;


# Create your views here.

# 文章表单
class ArticleForm(ModelForm):
    class Meta:
        model = models.Article
        fields = ["title", "sub_title", "brief"]

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs);
        self.fields["brief"].widget = HiddenInput();

# 文章表单
class ArticleContentForm(ModelForm):
    class Meta:
        model = models.ArticleContent
        fields = ["content"]

@csrf_exempt
def release(request):
    print("release get :", request.GET, "release post :", request.POST, "release files :", request.FILES);
    if "title" in request.POST:
        af = ArticleForm(request.POST);
        acf = ArticleContentForm(request.POST);
        if af.is_valid() and acf.is_valid():
            a = models.Article(title = af.cleaned_data["title"], sub_title = af.cleaned_data["sub_title"] or "", brief = af.cleaned_data["brief"], cid = models.ArticleContent(content = acf.cleaned_data["content"]));
            return render(request, "article_item.html", {
                "article" : a,
                "form" : af,
                "content_form" : acf,
            });
    return render(request, "article.html", {
        "form" : ArticleForm(),
        "content_form" : ArticleContentForm(),
    });