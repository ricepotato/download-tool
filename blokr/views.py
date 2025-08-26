import pathlib
import random
import shutil
import string
import uuid

import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from slugify import slugify

from .cleaner import clean_content, get_title_from_file
from .form import UrlForm


def index(request):
    if request.method == "GET":
        return index_get(request)

    if request.method == "POST":
        return index_post(request)

    return HttpResponse("Method not allowed", status=405)


def index_get(request):
    form = UrlForm()
    listdir = pathlib.Path("blokr_data").glob("*")
    return render(request, "blokr/index.html", {"form": form, "data": listdir})


def index_post(request):
    form = UrlForm(request.POST)
    if not form.is_valid():
        return HttpResponse("Invalid form", status=400)

    url = form.cleaned_data["url"]
    temp_dir = tmp_dir()
    html_file = download_html(url, temp_dir)

    title = get_title_from_file(html_file)
    work_dir = pathlib.Path("blokr_data") / slugify(title, allow_unicode=True)
    work_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(html_file, work_dir / "index_origin.html")
    clean_content(html_file, work_dir / "index.html")

    return HttpResponseRedirect(f"/blokr/{work_dir.name}")


def detail(_, work_dir: str):
    work_path = pathlib.Path("blokr_data") / pathlib.Path(work_dir)
    with open(work_path / "index.html", "r", encoding="utf-8") as fp:
        html = fp.read()
    return HttpResponse(html)


def download_html(url: str, work_dir: pathlib.Path):
    r = requests.get(url, timeout=5)
    r.raise_for_status()

    html_file_name = "index_origin.html"
    html_file_path = work_dir / html_file_name
    with open(html_file_path, "w", encoding="utf-8") as fp:
        fp.write(r.text)
    return html_file_path


def new_workdir():
    workdir = pathlib.Path("blokr_data") / str(uuid.uuid4())
    workdir.mkdir(parents=True, exist_ok=True)
    return workdir


def random_text():
    return "".join(random.choices(string.ascii_letters + string.digits, k=10))


def tmp_dir():
    tmp_path = pathlib.Path(__file__).parent.parent / "tmp"
    tmp_path.mkdir(parents=True, exist_ok=True)
    tmp_path = tmp_path / random_text()
    tmp_path.mkdir(parents=True, exist_ok=True)
    return tmp_path
