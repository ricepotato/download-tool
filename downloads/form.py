"""파일 이름과 내용을 저장하는 form.
파일 이름은 text input
파일 내용은 textarea 로 설정
"""

from django import forms


class FileForm(forms.Form):
    file_name = forms.CharField(label="파일 이름", initial="video")
    file_content = forms.CharField(label="파일 내용", widget=forms.Textarea)
