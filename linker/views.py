from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView
from django.contrib import messages

from .form import UrlForm, LinkTagForm
from .models import Link


class LinkListView(ListView):
    """링크 목록을 보여주는 뷰"""

    model = Link
    template_name = "linker/index.html"
    context_object_name = "links"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = UrlForm()
        return context

    def post(self, request, *args, **kwargs):
        """새 링크 추가 처리"""
        form = UrlForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            Link.objects.create(url=url)
            messages.success(request, "링크가 성공적으로 추가되었습니다.")
            return HttpResponseRedirect(reverse("link-index"))
        else:
            messages.error(request, "유효하지 않은 URL입니다.")
            return self.get(request, *args, **kwargs)


def add_tags_to_link(request, link_id):
    """링크에 태그 추가/편집"""
    link = get_object_or_404(Link, id=link_id)

    if request.method == "POST":
        form = LinkTagForm(request.POST, instance=link)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"'{link.title or link.url}'에 태그가 업데이트되었습니다."
            )
            return HttpResponseRedirect(reverse("link-index"))
    else:
        form = LinkTagForm(instance=link)

    return render(request, "linker/add_tags.html", {"form": form, "link": link})
