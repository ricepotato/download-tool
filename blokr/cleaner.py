"""
HTML 파일에서 <script>와 <style> 태그를 제거하는 함수들
"""

import logging
import re
from pathlib import Path

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def remove_script_style_tags(html_content):
    """
    HTML 문자열에서 <script>와 <style> 태그를 제거합니다.

    Args:
        html_content (str): HTML 문자열

    Returns:
        str: script와 style 태그가 제거된 HTML 문자열
    """
    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(html_content, "html.parser")

    # script 태그들 제거
    for script in soup.find_all("script"):
        script.decompose()

    # style 태그들 제거
    for style in soup.find_all("style"):
        style.decompose()

    # link 태그들 제거
    for link in soup.find_all("link"):
        link.decompose()

    return str(soup)


def remove_script_style_tags_regex(html_content):
    """
    정규표현식을 사용하여 <script>와 <style> 태그를 제거합니다.
    (BeautifulSoup보다 빠르지만 덜 안전할 수 있습니다)

    Args:
        html_content (str): HTML 문자열

    Returns:
        str: script와 style 태그가 제거된 HTML 문자열
    """
    # script 태그 제거 (내용 포함)
    html_content = re.sub(
        r"<script[^>]*>.*?</script>", "", html_content, flags=re.DOTALL | re.IGNORECASE
    )

    # style 태그 제거 (내용 포함)
    html_content = re.sub(
        r"<style[^>]*>.*?</style>", "", html_content, flags=re.DOTALL | re.IGNORECASE
    )

    return html_content


def remove_element_by_css_selectors(html_content: str, selectors: list[str]):
    soup = BeautifulSoup(html_content, "html.parser")
    for selector in selectors:
        for element in soup.select(selector):
            element.decompose()
    return str(soup)


def remove_styles_scripts(html_content: str, use_regex=False):
    if use_regex:
        cleaned_html = remove_script_style_tags_regex(html_content)
    else:
        cleaned_html = remove_script_style_tags(html_content)

    return cleaned_html


def crop_element_by_css_selectors(html_content: str, crop_selectors: list[str]):
    soup = BeautifulSoup(html_content, "html.parser")
    element = None
    for selector in crop_selectors:
        element = soup.select_one(selector)
        if element is not None:
            break

    # 새로운 HTML 문서 생성
    new_soup = BeautifulSoup(
        "<!DOCTYPE html>\n<html>\n<head>\n<meta charset='utf-8'>\n<title>Cleaned Content</title>\n</head>\n<body>\n</body>\n</html>",
        "html.parser",
    )

    if new_soup.body is None:
        raise ValueError("'body' element를 찾을 수 없습니다.")

    # at-body div를 새로운 문서의 body에 추가
    if element is not None:
        new_soup.body.append(element)

    return str(new_soup)


def clean_content(origin: Path, output: Path):
    """
    html 에서 불필요한 콘텐츠를 제거하고 정리된 html 파일을 생성합니다.

    파일을 읽어 텍스트를 추출합니다.
    텍스트에서 <script> 와 <style> 을 제거합니다.
    컨텐츠가 들어있는 element 만 추출합니다.


    """

    with open(origin, "r", encoding="utf-8") as f:
        html_content = f.read()

    cleaned_html = remove_styles_scripts(html_content)

    crop_selectors = [
        "#thema_wrapper > div.at-body > div > div > div.col-md-10.at-col.at-main > div > div.view-wrap",
        "#content article.post",
    ]

    cropped_html = crop_element_by_css_selectors(cleaned_html, crop_selectors)

    with open(output, "w", encoding="utf-8") as f:
        f.write(cropped_html)
