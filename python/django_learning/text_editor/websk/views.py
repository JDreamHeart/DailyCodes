from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

# Create your views here.
def websk(request):
    return render(request, "ws.html", {});