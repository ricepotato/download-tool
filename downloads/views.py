import mimetypes
import os
import pathlib
import subprocess
import tempfile
import uuid
import threading
from datetime import datetime

from django.http import StreamingHttpResponse
from django.shortcuts import render

from .form import FileForm

# Create your views here.


def get_download_jobs():
    """data 폴더 내의 다운로드 작업 목록을 반환"""
    data_dir = pathlib.Path("data")
    if not data_dir.exists():
        return []

    jobs = []
    for work_dir in data_dir.iterdir():
        if work_dir.is_dir():
            job_info = {
                "work_dir": work_dir.name,
                "work_dir_path": str(work_dir),
                "created_time": datetime.fromtimestamp(work_dir.stat().st_ctime),
                "mp4_files": [],
                "has_log": False,
                "log_file": None,
            }

            # 작업 폴더 내의 파일들 확인
            for file_path in work_dir.iterdir():
                if file_path.is_file():
                    if file_path.suffix.lower() == ".mp4":
                        # MP4 파일만 수집
                        file_info = {
                            "name": file_path.name,
                            "size": file_path.stat().st_size,
                            "modified_time": datetime.fromtimestamp(
                                file_path.stat().st_mtime
                            ),
                        }
                        job_info["mp4_files"].append(file_info)
                    elif file_path.suffix.lower() == ".log":
                        # 로그 파일 존재 여부만 확인
                        job_info["has_log"] = True
                        job_info["log_file"] = file_path.name

            # MP4 파일들을 수정 시간순으로 정렬
            job_info["mp4_files"].sort(key=lambda x: x["modified_time"], reverse=True)
            jobs.append(job_info)

    # 작업 폴더들을 생성 시간순으로 정렬 (최신순)
    jobs.sort(key=lambda x: x["created_time"], reverse=True)
    return jobs


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

    # GET 요청 시 다운로드 작업 목록 가져오기
    download_jobs = get_download_jobs()

    return render(request, "index.html", {"form": form, "download_jobs": download_jobs})


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
    log_filepath = download_dir / f"{mp4_file_name}.log"

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

    # 로그 파일을 열어서 stdout과 stderr를 리다이렉트
    with open(log_filepath, "w", encoding="utf-8") as log_file:
        process = subprocess.Popen(
            args,
            stdout=log_file,
            stderr=subprocess.STDOUT,  # stderr도 같은 파일로 리다이렉트
            universal_newlines=True,  # 텍스트 모드로 열기
        )

    # PID 파일 생성
    pid_filepath = download_dir / f"{mp4_file_name}.pid"
    with open(pid_filepath, "w") as pid_file:
        pid_file.write(str(process.pid))

    # 프로세스 종료 시 PID 파일 삭제를 위한 스레드 함수
    def cleanup_pid_file():
        process.wait()  # 프로세스가 종료될 때까지 대기
        try:
            if pid_filepath.exists():
                pid_filepath.unlink()  # PID 파일 삭제
        except Exception as e:
            print(f"PID 파일 삭제 중 오류 발생: {e}")

    # 백그라운드에서 PID 파일 정리 작업 실행
    cleanup_thread = threading.Thread(target=cleanup_pid_file, daemon=True)
    cleanup_thread.start()


def view_log(request, work_dir, log_file):
    """로그 파일 내용을 보여주는 뷰"""
    log_filepath = pathlib.Path("data") / work_dir / log_file

    if not log_filepath.exists():
        return render(
            request,
            "index.html",
            {
                "form": FileForm(),
                "download_jobs": get_download_jobs(),
                "error_message": "로그 파일을 찾을 수 없습니다.",
            },
        )

    try:
        with open(log_filepath, "r", encoding="utf-8") as f:
            log_content = f.read()
    except Exception as e:
        log_content = f"로그 파일을 읽을 수 없습니다: {e}"

    return render(
        request,
        "index.html",
        {
            "form": FileForm(),
            "download_jobs": get_download_jobs(),
            "log_content": log_content,
            "log_file_name": log_file,
        },
    )
