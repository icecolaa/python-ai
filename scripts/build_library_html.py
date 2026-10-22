#!/usr/bin/env python3
"""Build the single-file PythonAI study library from the Markdown notes.

Usage:
    python scripts/build_library_html.py
    python scripts/build_library_html.py --out PythonAI-学习资料库.html

The output is self-contained (CSS/JS/images inlined) and can be opened offline.
"""

from __future__ import annotations

import argparse
import base64
import html
import io
import mimetypes
import re
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path
from urllib.parse import quote, unquote

try:
    import markdown
except ImportError:
    sys.exit("Missing dependency: python -m pip install Markdown")

try:
    from lxml import etree, html as lxml_html
except ImportError:
    sys.exit("Missing dependency: python -m pip install lxml")

try:
    from PIL import Image
except ImportError:
    Image = None


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
ASSETS = SCRIPT_DIR

GROUPS = [
    {
        "id": "start",
        "kicker": "PART 01",
        "label": "START",
        "title": "开始 · 课程导览",
        "desc": "仓库说明与零基础入门，先建立大模型应用开发的全景认知。",
    },
    {
        "id": "python",
        "kicker": "PART 02",
        "label": "PYTHON",
        "title": "Python 编程基础与进阶",
        "desc": "第 2 阶段技术核心的 9 章教程，从环境搭建、语法与数据结构，一路走到协程并发。",
    },
]

DOCS = [
    {
        "id": "doc-repo",
        "group": "start",
        "path": "README.md",
        "nav_no": "01",
        "badge": "导览 01",
        "short": "仓库说明",
        "title": "仓库说明：PythonAI 学习路线",
        "desc": "仓库目录、环境准备、API Key 配置、示例运行方式与六阶段学习路线，先从这里了解全局。",
    },
    {
        "id": "doc-start",
        "group": "start",
        "path": "第1阶段：大模型开发入门/入门.md",
        "nav_no": "02",
        "badge": "导览 02",
        "short": "大模型开发入门",
        "title": "大模型开发入门",
        "desc": "从 AI 发展简史与大模型原理出发，完成 API 密钥配置、云端环境搭建，并写出第一个单轮 / 多轮聊天机器人。",
        "heading_mode": "flatten_h1",
    },
    {
        "id": "doc-ch01",
        "group": "python",
        "path": "第2阶段：大模型技术核心/1_python编程基础与进阶/第1章：python编程基础与进阶.md",
        "nav_no": "01",
        "badge": "第 01 章",
        "short": "环境搭建",
        "title": "Python 基础与环境搭建",
        "desc": "Python 解释器安装、VS Code / PyCharm 配置、pip 镜像加速与 venv / Conda 虚拟环境，一次把开发环境搭稳。",
    },
    {
        "id": "doc-ch02",
        "group": "python",
        "path": "第2阶段：大模型技术核心/1_python编程基础与进阶/第2章：基本语法与输入输出.md",
        "nav_no": "02",
        "badge": "第 02 章",
        "short": "基本语法与输入输出",
        "title": "Python 基础语法——让程序与你对话并完成计算",
        "desc": "代码规范、变量、输入输出、运算符与类型转换，用一个简易计算器串起 Python 的第一段交互式程序。",
    },
    {
        "id": "doc-ch03",
        "group": "python",
        "path": "第2阶段：大模型技术核心/1_python编程基础与进阶/第3章：核心数据类型.md",
        "nav_no": "03",
        "badge": "第 03 章",
        "short": "核心数据类型",
        "title": "Python 核心数据结构——让数据管理井井有条",
        "desc": "数字、字符串、列表、元组、集合、字典六大数据结构，围绕班级成绩管理系统讲清增删改查与选型。",
    },
    {
        "id": "doc-ch04",
        "group": "python",
        "path": "第2阶段：大模型技术核心/1_python编程基础与进阶/第4章：控制流与循环结构.md",
        "nav_no": "04",
        "badge": "第 04 章",
        "short": "控制流与循环",
        "title": "流程控制——赋予程序“决策”与“循环”能力",
        "desc": "条件判断、循环、推导式与流程控制，让程序具备决策与重复执行的能力。",
    },
    {
        "id": "doc-ch05",
        "group": "python",
        "path": "第2阶段：大模型技术核心/1_python编程基础与进阶/第5章：函数.md",
        "nav_no": "05",
        "badge": "第 05 章",
        "short": "函数",
        "title": "函数——构建可复用的代码块",
        "desc": "函数定义、参数传递、作用域、闭包与高阶函数，把代码组织成可复用的积木。",
    },
    {
        "id": "doc-ch06",
        "group": "python",
        "path": "第2阶段：大模型技术核心/1_python编程基础与进阶/第6章：面向对象编程.md",
        "nav_no": "06",
        "badge": "第 06 章",
        "short": "面向对象编程",
        "title": "面向对象编程——用“对象思维”组织代码",
        "desc": "类与对象、继承与多态、魔术方法与封装，用对象思维组织复杂程序。",
    },
    {
        "id": "doc-ch07",
        "group": "python",
        "path": "第2阶段：大模型技术核心/1_python编程基础与进阶/第7章：文件操作.md",
        "nav_no": "07",
        "badge": "第 07 章",
        "short": "文件操作",
        "title": "文件操作——让数据持久化",
        "desc": "文件读写、路径处理与上下文管理，让程序的数据能够持久保存。",
    },
    {
        "id": "doc-ch08",
        "group": "python",
        "path": "第2阶段：大模型技术核心/1_python编程基础与进阶/第8章：模块与包+异常处理+正则.md",
        "nav_no": "08",
        "badge": "第 08 章",
        "short": "模块、包与异常处理",
        "title": "模块化、异常处理与正则表达式",
        "desc": "模块与包的组织方式、异常处理机制与正则表达式，让代码更健壮、更有序。",
    },
    {
        "id": "doc-ch09",
        "group": "python",
        "path": "第2阶段：大模型技术核心/1_python编程基础与进阶/第9章：协程与异步并发.md",
        "nav_no": "09",
        "badge": "第 09 章",
        "short": "协程与异步并发",
        "title": "协程与异步编程——单线程的高效并发",
        "desc": "协程、async/await 与异步并发，理解单线程处理海量 I/O 任务的现代方案。",
    },
]

STAGES = [
    "大模型开发入门",
    "大模型技术核心",
    "NLP 核心",
    "大模型技术进阶",
    "多模态大模型",
    "具身智能",
]

FENCE_RE = re.compile(r"^\s*(?:```|~~~)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")

ICON_SEARCH = (
    '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" '
    'stroke-linecap="round" aria-hidden="true"><circle cx="7" cy="7" r="4.5"></circle>'
    '<path d="M10.5 10.5 14 14"></path></svg>'
)
ICON_MENU = (
    '<svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5" '
    'stroke-linecap="round" aria-hidden="true"><path d="M3 5h12M3 9h12M3 13h12"></path></svg>'
)
ICON_CHEVRON_RIGHT = (
    '<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.4" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4.5 2.5 8 6l-3.5 3.5"></path></svg>'
)
ICON_CHEVRON_DOWN = (
    '<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.4" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.5 4.5 6 8l3.5-3.5"></path></svg>'
)
ICON_UP = (
    '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 13V3M3.5 7.5 8 3l4.5 4.5"></path></svg>'
)

IMAGE_CACHE: dict[str, tuple[bytes, str] | None] = {}

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@@TITLE@@</title>
<meta name="description" content="@@DESC@@">
<meta name="theme-color" content="#f5f9ff">
<link rel="icon" href="@@FAVICON@@">
<style>
@@CSS@@
</style>
</head>
<body id="top">
<a class="skip-link" href="#main">跳到正文</a>
<header class="topbar" id="topbar">
  <div class="topbar-inner">
    <button class="menu-btn" id="menuBtn" type="button" aria-label="打开目录" aria-expanded="false" aria-controls="sidebar">@@ICON_MENU@@</button>
    <a class="brand" href="#top" aria-label="PythonAI 学习资料库首页">
      <span class="brand-mark" aria-hidden="true">Py</span>
      <span class="brand-text"><strong>PythonAI</strong><small>STUDY LIBRARY</small></span>
    </a>
    <div class="topbar-actions">
      <a class="topbar-link" href="PythonAI-学习计划.html" aria-label="打开学习计划">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" aria-hidden="true"><rect x="2" y="3.5" width="12" height="10.5" rx="2"></rect><path d="M5 2v3M11 2v3M2 6.5h12"></path></svg><span>学习计划</span>
      </a>
      <button class="search-trigger" id="searchTrigger" type="button" aria-label="搜索文档或章节">
        @@ICON_SEARCH@@<span>搜索</span><kbd>Ctrl K</kbd>
      </button>
      <span class="topbar-meta">@@TOPBAR_META@@</span>
    </div>
  </div>
  <div class="progress-track" aria-hidden="true"><span id="progressBar"></span></div>
</header>

<div class="shell">
  <aside class="sidebar" id="sidebar" aria-label="资料库目录">
    <div class="sidebar-head">
      <p class="kicker">LIBRARY INDEX</p>
      <h2>资料目录</h2>
      <p class="sidebar-note">@@SIDEBAR_META@@</p>
    </div>
    <label class="search-box" for="navSearch">
      @@ICON_SEARCH@@
      <input id="navSearch" type="search" placeholder="搜索文档或章节…" autocomplete="off" aria-label="搜索文档或章节">
      <kbd>Ctrl K</kbd>
    </label>
    <nav class="toc" aria-label="文档导航">
      <a class="nav-overview" href="#index"><span>文档索引</span><em>INDEX</em></a>
      @@NAV@@
    </nav>
    <p class="nav-empty" id="navEmpty" hidden>没有匹配的文档或章节</p>
    <div class="sidebar-foot">
      <strong>PYTHONAI / LOCAL EDITION</strong>
      @@SIDEBAR_FOOT@@
    </div>
  </aside>

  <main class="main" id="main">
    <section class="hero" aria-labelledby="hero-title">
      <div class="hero-copy">
        <p class="eyebrow"><span class="eyebrow-dot" aria-hidden="true"></span>PYTHONAI · STUDY LIBRARY</p>
        <h1 id="hero-title">PythonAI<span>学习资料库</span></h1>
        <p class="hero-sub">@@HERO_SUB@@</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="#@@FIRST_DOC@@">开始阅读</a>
          <a class="btn btn-ghost" href="#index">浏览文档索引</a>
        </div>
        <dl class="hero-stats">
          <div><dt>文档</dt><dd>@@DOC_COUNT@@<small>篇</small></dd></div>
          <div><dt>字符</dt><dd>@@CHAR_COUNT@@<small>万</small></dd></div>
          <div><dt>阅读</dt><dd>@@READ_HOURS@@<small>小时</small></dd></div>
        </dl>
      </div>
      <aside class="roadmap" aria-label="六阶段学习路线">
        <div class="roadmap-head"><span>学习路线</span><em>06 STAGES</em></div>
        <p class="roadmap-note">本册覆盖 01–02 阶段，其余为后续路线。</p>
        <ol class="stage-list">
          @@STAGES@@
        </ol>
        <div class="roadmap-foot"><span class="pulse" aria-hidden="true"></span>从 API 调用到企业级全栈</div>
      </aside>
    </section>

    <section class="index-section" id="index" aria-labelledby="index-title">
      <div class="section-head">
        <p class="kicker">DOCUMENT INDEX</p>
        <h2 id="index-title">文档索引</h2>
        <p>共 @@DOC_COUNT@@ 篇，按学习顺序排列。点击任意条目，直接跳到对应正文。</p>
      </div>
      <div class="index-grid">
        @@INDEX@@
      </div>
    </section>

    @@GROUPS@@

    <footer class="site-foot">
      <strong>PythonAI 学习资料库</strong>
      <p>共 @@DOC_COUNT@@ 篇文档 · @@TOPIC_COUNT@@ 个章节 · 全部正文已收录</p>
      <p>由本地 Markdown 一键生成 · @@BUILD_DATE@@</p>
    </footer>
  </main>
</div>

<div class="overlay" id="overlay" hidden></div>
<button class="back-top" id="backTop" type="button" aria-label="回到顶部">@@ICON_UP@@</button>
<script>
@@JS@@
</script>
</body>
</html>
"""


def strip_front_matter(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")
    if text.startswith("---\n"):
        match = re.match(r"^---\n.*?\n---\n", text, re.S)
        if match:
            text = text[match.end():]
    return text


def normalize_markdown(text: str, mode: str = "") -> tuple[str, str | None]:
    """Drop the document title and make every file use H2 for its top sections."""
    text = strip_front_matter(text)
    lines = text.split("\n")
    fence = False
    first_idx = None
    first_level = 0
    first_title = None

    for i, line in enumerate(lines):
        if FENCE_RE.match(line):
            fence = not fence
            continue
        if fence:
            continue
        match = HEADING_RE.match(line)
        if match and len(match.group(1)) <= 2:
            first_idx = i
            first_level = len(match.group(1))
            first_title = match.group(2).strip()
            break

    if first_idx is None:
        return text.strip() + "\n", None

    before = lines[:first_idx]
    after = lines[first_idx + 1:]

    fence = False
    has_extra_h1 = False
    for line in after:
        if FENCE_RE.match(line):
            fence = not fence
            continue
        if not fence and re.match(r"^#\s+", line):
            has_extra_h1 = True
            break

    if first_level == 1:
        if mode == "flatten_h1":
            shift = 0
        else:
            shift = 1 if has_extra_h1 else 0
    else:
        shift = -1

    out: list[str] = []
    fence = False
    for line in before + [""] + after:
        if FENCE_RE.match(line):
            fence = not fence
            out.append(line)
            continue
        if not fence:
            match = HEADING_RE.match(line)
            if match:
                level = max(2, min(6, len(match.group(1)) + shift))
                line = "#" * level + " " + match.group(2)
        out.append(line)

    return "\n".join(out).strip() + "\n", first_title


def render_markdown(body: str) -> str:
    converter = markdown.Markdown(
        extensions=["extra", "sane_lists"],
        output_format="html5",
    )
    return converter.convert(body)


def element_text(element: etree._Element) -> str:
    return "".join(element.itertext()).strip()


def has_meaningful_content(element: etree._Element) -> bool:
    if element.text and element.text.strip():
        return True
    for child in element:
        if child.tag == "hr":
            continue
        if element_text(child):
            return True
        if child.tag in ("img", "figure", "table", "pre", "blockquote"):
            return True
    return False


def wrap_tables(root: etree._Element) -> None:
    for table in list(root.iter("table")):
        parent = table.getparent()
        if parent is None:
            continue
        if parent.tag == "div" and "table-wrap" in (parent.get("class") or ""):
            continue
        wrapper = etree.Element("div")
        wrapper.set("class", "table-wrap")
        parent.replace(table, wrapper)
        wrapper.append(table)


def process_links(root: etree._Element) -> None:
    for link in root.iter("a"):
        href = link.get("href") or ""
        if href.startswith(("http://", "https://")):
            link.set("target", "_blank")
            link.set("rel", "noopener noreferrer")
        if href.lower().endswith((".zip", ".7z", ".rar", ".pdf", ".docx", ".xlsx")):
            classes = (link.get("class") or "").split()
            if "file-link" not in classes:
                classes.append("file-link")
            link.set("class", " ".join(classes))


def make_placeholder(img: etree._Element, label: str, note: str) -> None:
    safe_label = label if len(label) <= 64 else label[:61] + "…"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="440" viewBox="0 0 1200 440">
<rect width="1200" height="440" fill="#eef5ff"/>
<rect x="2" y="2" width="1196" height="436" rx="20" fill="none" stroke="#b9d4f8" stroke-width="2" stroke-dasharray="12 10"/>
<text x="600" y="206" text-anchor="middle" font-family="Georgia, serif" font-size="32" fill="#1e3a6e">{html.escape(note)}</text>
<text x="600" y="250" text-anchor="middle" font-family="Consolas, monospace" font-size="17" fill="#5b7699">{html.escape(safe_label)}</text>
<text x="600" y="292" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#7d93b0">可在源 Markdown 中补充图片后重新生成</text>
</svg>"""
    img.set("src", "data:image/svg+xml;charset=utf-8," + quote(svg, safe=""))
    img.set("width", "1200")
    img.set("height", "440")
    img.set("class", "img-placeholder")
    img.set("alt", f"{note}：{label}")
    figure = img.getparent()
    if figure is not None and figure.tag == "figure":
        caption = figure.find("figcaption")
        if caption is not None:
            caption.text = f"{note} · {safe_label}"


def fetch_image(url: str) -> tuple[bytes, str] | None:
    if url in IMAGE_CACHE:
        return IMAGE_CACHE[url]
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
            "Accept": "image/avif,image/webp,image/png,image/jpeg,image/*,*/*;q=0.8",
        },
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=12) as response:
                data = response.read(3_000_001)
                if len(data) > 3_000_000:
                    break
                content_type = response.headers.get_content_type() or "image/png"
            IMAGE_CACHE[url] = (data, content_type)
            return IMAGE_CACHE[url]
        except Exception:
            if attempt < 2:
                time.sleep(1.2)
    IMAGE_CACHE[url] = None
    return None


def image_dimensions(data: bytes) -> tuple[int, int] | None:
    if Image is None:
        return None
    try:
        with Image.open(io.BytesIO(data)) as image:
            return image.size
    except Exception:
        return None


def process_images(root: etree._Element, doc_path: Path) -> tuple[int, int]:
    for img in list(root.iter("img")):
        parent = img.getparent()
        if parent is not None and parent.tag == "p" and len(parent) == 1:
            figure = etree.Element("figure")
            figure.set("class", "figure")
            grandparent = parent.getparent()
            if grandparent is not None:
                grandparent.replace(parent, figure)
                figure.append(img)
                caption = etree.SubElement(figure, "figcaption")
                caption.text = img.get("alt") or "插图"

    inlined = 0
    missing = 0
    for img in root.iter("img"):
        src = (img.get("src") or "").strip()
        data = None
        mime = "image/png"
        if src.startswith("data:"):
            inlined += 1
            continue
        if src.startswith(("http://", "https://")):
            fetched = fetch_image(src)
            if fetched is not None:
                data, mime = fetched
            else:
                make_placeholder(img, "网络图片", "插图未能内联")
                missing += 1
        else:
            relative = unquote(src.split("?")[0].split("#")[0])
            candidate = (doc_path.parent / relative).resolve()
            try:
                candidate.relative_to(ROOT)
                inside_root = True
            except ValueError:
                inside_root = False
            if inside_root and candidate.is_file() and candidate.stat().st_size <= 3_000_000:
                data = candidate.read_bytes()
                mime = mimetypes.guess_type(candidate.name)[0] or "image/png"
            else:
                make_placeholder(img, relative, "插图暂缺")
                missing += 1

        if data is not None:
            size = image_dimensions(data)
            if size:
                img.set("width", str(size[0]))
                img.set("height", str(size[1]))
            encoded = base64.b64encode(data).decode("ascii")
            img.set("src", f"data:{mime};base64,{encoded}")
            inlined += 1

        img.set("loading", "lazy")
        img.set("decoding", "async")

    return inlined, missing


def build_document(doc: dict) -> dict:
    source_path = ROOT / doc["path"]
    raw = source_path.read_text(encoding="utf-8-sig")
    body_md, removed_title = normalize_markdown(raw, doc.get("heading_mode", ""))
    fragment = render_markdown(body_md)
    parser = lxml_html.HTMLParser(encoding="utf-8")
    root = lxml_html.fromstring('<div class="md-root">' + fragment + "</div>", parser=parser)
    from study_plan import add_course_summary
    add_course_summary(root)

    lead = etree.Element("div")
    lead.set("class", "doc-lead")
    sections: list[etree._Element] = []
    current = lead
    for child in list(root):
        if child.tag == "h2":
            section = etree.Element("section")
            section.set("class", "topic")
            section.append(child)
            sections.append(section)
            current = section
        else:
            current.append(child)

    topics = []
    for index, section in enumerate(sections, 1):
        heading = section.find("h2")
        if heading is None:
            continue
        topic_id = f"{doc['id']}-s{index}"
        heading.set("id", topic_id)
        topics.append({"id": topic_id, "title": element_text(heading)})
        sub_index = 0
        for heading in section.iter():
            if heading.tag not in ("h3", "h4", "h5", "h6"):
                continue
            sub_index += 1
            heading.set("id", f"{topic_id}-{sub_index}")

    lead_index = 0
    for heading in lead.iter():
        if heading.tag in ("h2", "h3", "h4", "h5", "h6"):
            lead_index += 1
            heading.set("id", f"{doc['id']}-lead-{lead_index}")

    nodes = [lead, *sections]
    for node in nodes:
        for heading in list(node.iter("h2", "h3", "h4", "h5", "h6")):
            level = int(heading.tag[1])
            heading.tag = f"h{min(6, level + 1)}"

    for node in nodes:
        for heading in node.iter("h3", "h4", "h5", "h6"):
            heading_id = heading.get("id")
            if not heading_id:
                continue
            anchor = etree.SubElement(heading, "a")
            anchor.set("class", "heading-anchor")
            anchor.set("href", "#" + heading_id)
            anchor.set("aria-hidden", "true")
            anchor.text = "#"

    inlined = 0
    missing = 0
    for node in nodes:
        process_links(node)
        wrap_tables(node)
        node_inlined, node_missing = process_images(node, source_path)
        inlined += node_inlined
        missing += node_missing
    lead_html = ""
    if has_meaningful_content(lead):
        lead_html = lxml_html.tostring(lead, encoding="unicode", method="html")
    sections_html = "".join(
        lxml_html.tostring(section, encoding="unicode", method="html")
        for section in sections
    )

    plain_length = len(re.sub(r"\s+", "", raw))
    return {
        **doc,
        "topics": topics,
        "lead_html": lead_html,
        "sections_html": sections_html,
        "chars": len(raw),
        "minutes": max(3, int(round(plain_length / 400))),
        "inlined": inlined,
        "missing": missing,
        "source_title": removed_title,
    }


def build_nav(docs: list[dict]) -> str:
    blocks = []
    for group in GROUPS:
        group_docs = [doc for doc in docs if doc["group"] == group["id"]]
        if not group_docs:
            continue
        parts = [
            '<div class="nav-group">',
            f'<div class="nav-group-head"><span>{html.escape(group["title"])}</span><em>{len(group_docs):02d}</em></div>',
        ]
        for doc in group_docs:
            search_bits = [doc["title"], doc["desc"]] + [topic["title"] for topic in doc["topics"]]
            search_value = html.escape(" ".join(search_bits), quote=True)
            parts.append(f'<div class="nav-item" data-doc="{doc["id"]}" data-search="{search_value}">')
            parts.append('<div class="nav-row">')
            parts.append(
                f'<a class="nav-link" href="#{doc["id"]}"><span class="nav-no">{doc["nav_no"]}</span>'
                f'<span class="nav-title">{html.escape(doc["short"])}</span></a>'
            )
            if doc["topics"]:
                parts.append(
                    f'<button class="nav-expand" type="button" aria-expanded="false" '
                    f'aria-controls="subs-{doc["id"]}" aria-label="展开 {html.escape(doc["short"], quote=True)} 的章节">'
                    f'{ICON_CHEVRON_RIGHT}</button>'
                )
            parts.append("</div>")
            if doc["topics"]:
                parts.append(f'<div class="nav-subs" id="subs-{doc["id"]}" hidden>')
                for topic in doc["topics"]:
                    parts.append(
                        f'<a class="nav-sub" href="#{topic["id"]}">{html.escape(topic["title"])}</a>'
                    )
                parts.append("</div>")
            parts.append("</div>")
        parts.append("</div>")
        blocks.append("".join(parts))
    return "\n".join(blocks)


def build_index(docs: list[dict]) -> str:
    panels = []
    for group in GROUPS:
        group_docs = [doc for doc in docs if doc["group"] == group["id"]]
        if not group_docs:
            continue
        items = []
        for doc in group_docs:
            items.append(
                f'<li><a href="#{doc["id"]}"><span class="index-no">{doc["nav_no"]}</span>'
                f'<span class="index-title">{html.escape(doc["short"])}</span>'
                f'<span class="index-meta">{doc["minutes"]} 分钟</span></a></li>'
            )
        panels.append(
            f'<article class="index-panel index-panel--{group["id"]}">'
            f'<p class="kicker">{group["kicker"]} · {group["label"]}</p>'
            f'<h3>{html.escape(group["title"])}</h3>'
            f'<p>{html.escape(group["desc"])}</p>'
            f'<ol class="index-list">{"".join(items)}</ol>'
            f'</article>'
        )
    return "\n".join(panels)


def build_document_html(doc: dict) -> str:
    if doc["topics"]:
        toc_items = "".join(
            f'<li><a href="#{topic["id"]}">{html.escape(topic["title"])}</a></li>'
            for topic in doc["topics"]
        )
        toc = (
            '<details class="doc-toc">'
            f'<summary><span>本文章节</span><em>{len(doc["topics"])}</em>{ICON_CHEVRON_DOWN}</summary>'
            f'<ol>{toc_items}</ol></details>'
        )
    else:
        toc = ""

    return (
        f'<article class="doc reveal" id="{doc["id"]}" data-doc="{doc["id"]}">'
        f'<header class="doc-head">'
        f'<div class="doc-meta"><span class="doc-badge">{doc["badge"]}</span>'
        f'<span class="meta-dot" aria-hidden="true"></span><span>约 {doc["minutes"]} 分钟</span>'
        f'<span class="meta-dot" aria-hidden="true"></span><span>{doc["chars"]:,} 字符</span>'
        f'<span class="meta-dot" aria-hidden="true"></span><span>{len(doc["topics"])} 节</span></div>'
        f'<h2 class="doc-title">{html.escape(doc["title"])}</h2>'
        f'<p class="doc-desc">{html.escape(doc["desc"])}</p>'
        f'</header>{toc}<div class="paper">{doc["lead_html"]}{doc["sections_html"]}</div>'
        f'<div class="doc-end"><a href="#index">↑ 返回文档索引</a></div>'
        f'</article>'
    )


def build_groups(docs: list[dict]) -> str:
    blocks = []
    for group in GROUPS:
        group_docs = [doc for doc in docs if doc["group"] == group["id"]]
        if not group_docs:
            continue
        docs_html = "\n".join(build_document_html(doc) for doc in group_docs)
        blocks.append(
            f'<section class="doc-group" aria-labelledby="group-{group["id"]}-title">'
            f'<div class="group-head reveal" id="group-{group["id"]}">'
            f'<div><p class="kicker">{group["kicker"]} · {group["label"]}</p>'
            f'<h2 id="group-{group["id"]}-title">{html.escape(group["title"])}</h2>'
            f'<p>{html.escape(group["desc"])}</p></div>'
            f'<span class="group-stamp" aria-hidden="true">{len(group_docs):02d}<small>篇</small></span>'
            f'</div>{docs_html}</section>'
        )
    return "\n".join(blocks)


def build_stages() -> str:
    items = []
    for index, name in enumerate(STAGES, 1):
        included = index <= 2
        classes = ' class="is-included"' if included else ""
        state = "已收录" if included else "路线"
        items.append(
            f'<li{classes}><span class="stage-no">{index:02d}</span>'
            f'<span class="stage-name">{html.escape(name)}</span>'
            f'<span class="stage-state">{state}</span></li>'
        )
    return "".join(items)


def make_favicon() -> str:
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
        '<rect width="64" height="64" rx="16" fill="#2f6bff"/>'
        '<text x="32" y="42" text-anchor="middle" font-family="Consolas,monospace" '
        'font-size="25" font-weight="700" fill="#f8fbff">Py</text></svg>'
    )
    return "data:image/svg+xml;charset=utf-8," + quote(svg, safe="")


def build_page(docs: list[dict], out_path: Path) -> str:
    css = (ASSETS / "library_style.css").read_text(encoding="utf-8")
    js = (ASSETS / "library_app.js").read_text(encoding="utf-8")

    total_chars = sum(doc["chars"] for doc in docs)
    total_topics = sum(len(doc["topics"]) for doc in docs)
    total_minutes = sum(doc["minutes"] for doc in docs)
    read_hours = f"{total_minutes / 60:.1f}"
    title = "PythonAI 学习资料库"
    desc = "PythonAI 学习资料库：11 篇课程文档的可视化阅读版，含章节导航、目录检索与阅读进度。"

    values = {
        "@@TITLE@@": html.escape(title),
        "@@DESC@@": html.escape(desc, quote=True),
        "@@FAVICON@@": make_favicon(),
        "@@CSS@@": css,
        "@@JS@@": js,
        "@@ICON_MENU@@": ICON_MENU,
        "@@ICON_SEARCH@@": ICON_SEARCH,
        "@@ICON_UP@@": ICON_UP,
        "@@TOPBAR_META@@": f"{len(docs)} 篇 · {total_topics} 节",
        "@@SIDEBAR_META@@": f"{len(docs)} 篇文档 · {total_topics} 个章节",
        "@@SIDEBAR_FOOT@@": "全部正文已收录<br>离线可读 · 目录可检索",
        "@@HERO_SUB@@": (
            f"把当前目录里的 {len(docs)} 篇 Markdown 汇成一册：完整保留正文，"
            "加入章节导航、目录检索与阅读进度，双击即可离线阅读。"
        ),
        "@@FIRST_DOC@@": docs[0]["id"] if docs else "index",
        "@@DOC_COUNT@@": str(len(docs)),
        "@@TOPIC_COUNT@@": str(total_topics),
        "@@CHAR_COUNT@@": f"{total_chars / 10000:.1f}",
        "@@READ_HOURS@@": read_hours,
        "@@STAGES@@": build_stages(),
        "@@NAV@@": build_nav(docs),
        "@@INDEX@@": build_index(docs),
        "@@GROUPS@@": build_groups(docs),
        "@@BUILD_DATE@@": date.today().isoformat(),
    }

    page = PAGE_TEMPLATE
    for key, value in values.items():
        page = page.replace(key, value)
    return page


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        default=str(ROOT / "PythonAI-学习资料库.html"),
        help="output HTML path (default: PythonAI-学习资料库.html)",
    )
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    docs = []
    for doc in DOCS:
        source = ROOT / doc["path"]
        if not source.is_file():
            print(f"Skip missing source: {source.relative_to(ROOT)}")
            continue
        built = build_document(doc)
        docs.append(built)
        print(
            f"Read {doc['path']}: {len(built['topics'])} sections, "
            f"{built['chars']:,} chars, {built['inlined']} image(s) inlined, "
            f"{built['missing']} placeholder(s)"
        )

    if not docs:
        sys.exit("No Markdown sources found.")

    out_path = Path(args.out).resolve()
    page = build_page(docs, out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(page, encoding="utf-8")

    print(f"Created: {out_path}")
    print(f"Documents: {len(docs)} | Size: {out_path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
