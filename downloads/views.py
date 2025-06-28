import mimetypes
import os
import pathlib
import subprocess
import tempfile
import uuid

from django.http import StreamingHttpResponse
from django.shortcuts import render

from .form import FileForm

# Create your views here.


def index(request):
    if request.method == "POST":
        form = FileForm(request.POST)
        if form.is_valid():
            file_name = form.cleaned_data["file_name"]
            file_content = form.cleaned_data["file_content"]

            work_dir = new_workdir()
            m3u8_filepath = make_m3u8(file_content, work_dir)
            download_mp4(m3u8_filepath, file_name, work_dir)

            # return stream_mp4(filepath, file_name)
            # return render(request, "index.html", {"form": form})
    else:
        form = FileForm()
    return render(request, "index.html", {"form": form})


def make_m3u8(content: str, work_dir: pathlib.Path):
    file_name = "index.m3u8"
    content = content.replace("\r\n", "\n")
    filepath = work_dir / file_name
    with open(filepath, "w", encoding="utf-8") as fp:
        fp.write(content)
    return filepath


def new_workdir():
    workdir = pathlib.Path("data") / str(uuid.uuid4())
    workdir.mkdir(parents=True, exist_ok=True)
    return workdir


def download_mp4(m3u8_file_name: str, mp4_file_name: str, download_dir: pathlib.Path):
    """아래 명령을 실행

    ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto -i MIE.m3u8 -c copy -bsf:a aac_adtstoasc MIE.mp4"""

    output_filepath = download_dir / f"{mp4_file_name}.mp4"

    args = [
        "ffmpeg",
        "-protocol_whitelist",
        "file,http,https,tcp,tls,crypto",
        "-i",
        f"{m3u8_file_name}",
        "-c",
        "copy",
        "-bsf:a",
        "aac_adtstoasc",
        str(output_filepath),
    ]
    print(" ".join(args))
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # try:
    #     output = subprocess.check_output(args)
    #     print(output)
    # except subprocess.CalledProcessError as e:
    #     print(e.output)
    # return process


# def stream_mp4(m3u8_file_name: str, mp4_file_name: str):
#     """스트리밍 다운로드를 처리하는 뷰 함수"""

#     def file_iterator():
#         process = download_mp4(m3u8_file_name, mp4_file_name)
#         with open(mp4_file_name, "rb") as f:
#             while True:
#                 chunk = f.read(8192)  # 8KB chunks
#                 if not chunk:
#                     break
#                 yield chunk
#         # Clean up the temporary file
#         os.remove(mp4_file_name)

#     # content_type, _ = mimetypes.guess_type(mp4_file_name)
#     response = StreamingHttpResponse(
#         file_iterator(), content_type="application/octet-stream"
#     )
#     response["Content-Disposition"] = f'attachment; filename="{mp4_file_name}"'
#     return response
