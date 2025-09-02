from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .form import UrlForm
from .models import Link


# Create your views here.
def index(request):
    if request.method == "GET":
        return index_get(request)

    if request.method == "POST":
        return index_post(request)

    return HttpResponse("Method not allowed", status=405)


def index_get(request):
    form = UrlForm()
    return render(request, "linker/index.html", {"form": form})


def index_post(request):
    form = UrlForm(request.POST)
    if not form.is_valid():
        return HttpResponse("Invalid form", status=400)

    url = form.cleaned_data["url"]
    link = Link.objects.create(url=url)
    return HttpResponseRedirect(reverse("link-index"))
