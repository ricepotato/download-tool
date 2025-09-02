from django import forms
from .models import Link


class UrlForm(forms.Form):
    url = forms.CharField(label="URL")


class LinkTagForm(forms.ModelForm):
    """링크에 태그를 추가/편집하는 폼"""

    class Meta:
        model = Link
        fields = ["tags"]
        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
        }
