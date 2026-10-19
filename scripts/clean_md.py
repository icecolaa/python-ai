# -*- coding: utf-8 -*-
"""
把语雀/网页导出的 Markdown 中的 HTML 标签清洗为纯 Markdown 可读形式。

处理范围（仅限代码块之外，``` 围栏内的内容原样保留）：
  1. <font style="...">文本</font>        -> 文本
  2. <img src="X" ...>                   -> ![插图](X)
  3. <br> / <br/>                        -> 换行
  4. <b>/<strong>、<i>/<em>、<u>、<s>    -> ** / * / ~~
  5. <span>/<div>/<p>/<a> 等残留行内标签  -> 去除标签保留文本（<a> 保留 href 为 Markdown 链接）
  6. &nbsp; &amp; &lt; &gt; &quot;       -> 对应字符
  7. \\_  \\*  \\#  等转义                -> 还原
  8. 收尾整理：空粗体 ****、行尾空格、连续空行

用法：
  python scripts/clean_md.py                       # 处理默认目录（第2阶段/1_python编程基础与进阶）
  python scripts/clean_md.py <文件或目录> [...]    # 处理指定路径
  python scripts/clean_md.py --dry-run             # 只预览改动统计，不写盘
"""
import io
import os
import re
import sys

DEFAULT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                           '第2阶段：大模型技术核心', '1_python编程基础与进阶')

FONT_RE = re.compile(r'</?font\b[^>]*>', re.I)
IMG_RE = re.compile(r'<img\b[^>]*>', re.I)
BR_RE = re.compile(r'<br\s*/?>', re.I)
BOLD_RE = re.compile(r'</?(?:b|strong)\b[^>]*>', re.I)
ITAL_RE = re.compile(r'</?(?:i|em)\b[^>]*>', re.I)
U_RE = re.compile(r'</?u\b[^>]*>', re.I)
DEL_RE = re.compile(r'</?(?:s|del|strike)\b[^>]*>', re.I)
ANCHOR_RE = re.compile(r'<a\b[^>]*href="([^"]*)"[^>]*>(.*?)</a>', re.I | re.S)
STRIP_RE = re.compile(r'</?(?:span|div|p|section|article|font|small|big|code|pre|mark)\b[^>]*>', re.I)
ATTR_SRC = re.compile(r'\bsrc="([^"]*)"', re.I)
ATTR_ALT = re.compile(r'\balt="([^"]*)"', re.I)
ATTR_TITLE = re.compile(r'\btitle="([^"]*)"', re.I)

ENTITIES = [
    ('&nbsp;', ' '), ('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'),
    ('&quot;', '"'), ('&apos;', "'"), ('&#39;', "'"),
]


def clean_line(line):
    """清洗一行（调用方保证这行不在代码块内）。"""
    # 图片：整段 <img ...> -> Markdown 图片语法
    def img_repl(m):
        tag = m.group(0)
        src = ATTR_SRC.search(tag)
        if not src:
            return ''
        alt = ATTR_ALT.search(tag)
        title = ATTR_TITLE.search(tag)
        alt_text = (alt.group(1).strip() if alt and alt.group(1).strip()
                    else (title.group(1).strip() if title and title.group(1).strip() not in ('', 'null')
                          else '插图'))
        return '![%s](%s)' % (alt_text, src.group(1))
    line = IMG_RE.sub(img_repl, line)

    # 链接：保留 href，转成 Markdown
    def a_repl(m):
        return '[%s](%s)' % (re.sub(r'<[^>]+>', '', m.group(2)).strip(), m.group(1))
    line = ANCHOR_RE.sub(a_repl, line)

    line = BR_RE.sub('  \n', line)
    line = BOLD_RE.sub('**', line)
    line = ITAL_RE.sub('*', line)
    line = U_RE.sub('', line)
    line = DEL_RE.sub('~~', line)
    line = FONT_RE.sub('', line)
    line = STRIP_RE.sub('', line)

    # HTML 实体
    for ent, ch in ENTITIES:
        line = line.replace(ent, ch)

    # 反斜杠转义（保护 markdown 语义的常见转义符之外的还原）
    line = line.replace('\\_', '_').replace('\\*', '*').replace('\\#', '#')

    # 收尾：空的强调标记
    line = line.replace('****', '').replace('** **', ' ').replace('* *', ' ')
    line = re.sub(r'\*\*\s*\*\*', '', line)
    if not line.strip():
        return ''
    # 保留行尾两个空格的 Markdown 硬换行，其余行尾空白清掉
    hard_break = re.search(r'[ \t]{2,}$', line) is not None
    return re.sub(r'[ \t]+$', '', line) + ('  ' if hard_break else '')


def clean_text(text):
    out = []
    in_fence = False
    fence_mark = ''
    for line in text.split('\n'):
        stripped = line.lstrip()
        if not in_fence and stripped.startswith('```'):
            in_fence = True
            fence_mark = '```'
            out.append(line)
            continue
        if in_fence and stripped.startswith(fence_mark):
            in_fence = False
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        out.append(clean_line(line))
    result = '\n'.join(out)
    # 连续 3 个以上空行压成 2 个
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result.rstrip() + '\n'


def process(path, dry_run=False):
    with io.open(path, 'r', encoding='utf-8') as f:
        before = f.read()
    after = clean_text(before)
    changed = before != after
    if changed and not dry_run:
        with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(after)
    return changed, before, after


def main():
    args = [a for a in sys.argv[1:]]
    dry_run = '--dry-run' in args
    args = [a for a in args if a != '--dry-run']
    targets = args or [DEFAULT_DIR]

    files = []
    for t in targets:
        if os.path.isdir(t):
            for name in sorted(os.listdir(t)):
                if name.lower().endswith('.md'):
                    files.append(os.path.join(t, name))
        elif os.path.isfile(t):
            files.append(t)
        else:
            print('跳过（不存在）:', t)

    total_changed = 0
    for path in files:
        changed, before, after = process(path, dry_run)
        n_font = len(FONT_RE.findall(before))
        n_img = len(IMG_RE.findall(before))
        n_other = len(re.findall(r'</?(?:span|div|br|a|b|i|u|s|p)\b', before, re.I))
        flag = '改写' if changed else '无需改动'
        if dry_run:
            flag = '将改写' if changed else '无需改动'
        print('%-46s %s  font:%-4d img:%-3d 其他:%-3d' % (
            os.path.basename(path), flag, n_font, n_img, n_other))
        if changed:
            total_changed += 1
    print('\n共 %d 个文件，%s %d 个。%s' % (
        len(files), '将改写' if dry_run else '已改写', total_changed,
        '（dry-run，未写盘）' if dry_run else ''))


if __name__ == '__main__':
    main()
