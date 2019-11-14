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
        fields = ["title", "sub_title", "brief", "content"]

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs);
        self.fields["brief"].widget = HiddenInput();

@csrf_exempt
def release(request):
    print("release get :", request.GET, "release post :", request.POST, "release files :", request.FILES);
    if "title" in request.POST:
        af = ArticleForm(request.POST);
        print("==========af===========", af.is_valid(), af.cleaned_data);
        if af.is_valid():
            a = models.Article(title = af.cleaned_data["title"], sub_title = af.cleaned_data["sub_title"] or "", brief = af.cleaned_data["brief"], content = af.cleaned_data["content"]);
            return render(request, "article_item.html", {
                "article" : a,
                "form" : af,
            });
    return render(request, "article.html", {
        "form" : ArticleForm(),
    });