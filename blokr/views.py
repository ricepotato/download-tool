import pathlib
import uuid

import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .form import UrlForm


def index(request):
    if request.method == "POST":
        form = UrlForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            work_dir = new_workdir()
            download_html(url, work_dir)
            return HttpResponseRedirect(f"/blokr/{work_dir.name}")
    else:
        form = UrlForm()
    return render(request, "blokr/index.html", {"form": form})


def detail(request, work_dir: str):
    work_dir = pathlib.Path("blokr_data") / work_dir
    with open(work_dir / "index.html", "r", encoding="utf-8") as fp:
        html = fp.read()
    return HttpResponse(html)


def download_html(url: str, work_dir: pathlib.Path):
    r = requests.get(url, timeout=5)
    r.raise_for_status()

    html_file_name = "index.html"
    html_file_path = work_dir / html_file_name
    with open(html_file_path, "w", encoding="utf-8") as fp:
        fp.write(r.text)
    return html_file_path


def new_workdir():
    workdir = pathlib.Path("blokr_data") / str(uuid.uuid4())
    workdir.mkdir(parents=True, exist_ok=True)
    return workdir
