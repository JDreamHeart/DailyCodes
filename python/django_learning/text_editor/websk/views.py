from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

# Create your views here.
def websk(request):
    print("websk:", request.COOKIES)
    return render(request, "ws.html", {});