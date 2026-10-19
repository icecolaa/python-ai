"""Convert Markdown to a standalone report (Python-Markdown fallback).

Usage: python scripts/md_to_html.py chapter.md --theme report -o whitepaper.html
Dependency: python -m pip install Markdown
This local implementation replaces the missing SkillHub script/template.
"""

import argparse
import html
import re
import sys
from pathlib import Path
from urllib.parse import quote


CSS = """
:root { color-scheme: light; --ink:#292724; --muted:#746e66; --accent:#a34f32; --line:#ddd6cc; }
* { box-sizing:border-box; }
html { scroll-behavior:smooth; scroll-padding-top:24px; }
body { margin:0; background:#f5f2ec; color:var(--ink);
  font-family:Georgia,'Noto Serif CJK SC','Source Han Serif SC',SimSun,serif;
  font-size:17px; line-height:1.8; overflow-wrap:anywhere; }
.sheet { max-width:940px; margin:48px auto; padding:52px 60px; background:#fffefa; }
.eyebrow { color:var(--accent); font:12px/1.5 sans-serif; letter-spacing:.18em; }
header { padding-bottom:28px; border-bottom:2px solid var(--ink); margin-bottom:30px; }
header h1 { font-size:34px; line-height:1.4; margin:14px 0; }
.subtitle { color:var(--muted); font-size:14px; margin:0; }
nav { border-bottom:1px solid var(--line); padding:0 0 24px; margin-bottom:36px; }
nav summary { cursor:pointer; color:var(--accent); font-weight:bold; }
nav ul { font-size:14px; line-height:1.8; }
nav a { color:var(--muted); }
article h1 { margin:2em 0 .7em; font-size:28px; line-height:1.45; }
article h2 { margin:1.9em 0 .65em; font-size:24px; line-height:1.5; }
article h3 { margin:1.6em 0 .6em; font-size:20px; color:var(--accent); }
article h4 { font-size:18px; }
article p { margin:1.1em 0; }
a { color:var(--accent); text-underline-offset:3px; }
a:hover { text-decoration-thickness:2px; }
li { margin:.35em 0; }
hr { border:0; border-top:1px solid var(--line); margin:2.3em 0; }
code { font-family:'JetBrains Mono',Consolas,monospace; font-size:.86em;
  background:#f1eee7; padding:.15em .3em; }
pre { background:#f4f3ef; padding:20px 22px; overflow-x:auto; line-height:1.65; }
pre code { padding:0; background:transparent; white-space:pre; overflow-wrap:normal; }
blockquote { margin:1.5em 0; padding:4px 24px; border-left:2px solid var(--accent);
  color:var(--muted); font-style:italic; }
.table-scroll { overflow-x:auto; margin:1.5em 0; }
table { border-collapse:collapse; width:100%; font-size:14px; line-height:1.7; }
th,td { border-bottom:1px solid var(--line); padding:12px 14px; text-align:left; vertical-align:top; }
th { background:#eee9df; font-weight:bold; }
img { display:block; max-width:100%; height:auto; margin:24px auto; }
footer { border-top:1px solid var(--line); margin-top:48px; padding-top:18px;
  font-size:12px; color:var(--muted); }
@media(max-width:700px) {
  body { font-size:16px; } .sheet { margin:0; padding:30px 22px; }
  header h1 { font-size:27px; } article h1 { font-size:25px; }
  article h2 { font-size:22px; } pre { padding:16px; }
}
@media print {
  @page { margin:18mm; } body { background:white; font-size:11pt; }
  .sheet { margin:0; padding:0; max-width:none; } nav { display:none; }
  h1,h2,h3 { break-after:avoid; } pre,blockquote,img { break-inside:avoid; }
  pre { white-space:pre-wrap; } pre code { white-space:pre-wrap; }
  a { color:inherit; } .table-scroll { overflow:visible; }
}
"""


def resolve_input(value):
    path = Path(value)
    if path.is_file():
        return path.resolve()
    # A basename is convenient for chapter files nested under course folders.
    if path.parent == Path('.'):
        matches = [p for p in Path.cwd().rglob(path.name) if p.is_file()]
        if len(matches) == 1:
            return matches[0].resolve()
        if matches:
            raise ValueError('Multiple matching files; specify a path: ' + ', '.join(map(str, matches)))
    raise ValueError(f'Input file not found: {value}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    parser.add_argument('--theme', choices=['report'], default='report')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    try:
        import markdown
    except ImportError:
        parser.exit(1, 'Missing dependency: python -m pip install Markdown\n')
    try:
        source = resolve_input(args.input)
        output = Path(args.output).resolve() if args.output else source.with_suffix('.html')
        if source == output:
            raise ValueError('Output must differ from input')
        text = source.read_text(encoding='utf-8-sig')
        # Yuque exports wrap text in font tags, even inside inline code.
        # Remove presentation wrappers before parsing so code remains readable.
        text = re.sub(r'</?font\b[^>]*>', '', text, flags=re.I)
        converter = markdown.Markdown(extensions=['extra', 'toc', 'sane_lists'],
            extension_configs={'toc': {'permalink': False}})
        body = converter.convert(text)
        body = re.sub(r'<table\b[^>]*>.*?</table>',
            lambda m: '<div class="table-scroll">' + m.group(0) + '</div>', body, flags=re.S)
        title = html.escape(source.stem)
        # A base URL preserves local image/link paths when output is elsewhere.
        base = html.escape(source.parent.as_uri() + '/', quote=True)
        document = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<base href="{base}"><title>{title}</title><style>{CSS}</style></head>
<body><main class="sheet">
<header><div class="eyebrow">PYTHON / STUDY REPORT</div><h1>{title}</h1>
<p class="subtitle">Python 编程学习资料 · Report 阅读版</p></header>
<nav aria-label="章节目录"><details open><summary>内容目录</summary>{converter.toc}</details></nav>
<article>{body}</article><footer>{title} · 由 Markdown 转换</footer>
</main></body></html>'''
        # A file:// base changes fragment navigation; keep TOC links on this output.
        document = re.sub(r'href="#([^"]+)"',
            lambda m: 'href="' + html.escape(output.as_uri(), quote=True) + '#' + quote(html.unescape(m.group(1))) + '"', document)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(document, encoding='utf-8')
        print(f'Created: {output}')
        print(f'Source: {source}')
    except (OSError, ValueError) as exc:
        parser.exit(1, str(exc) + '\n')


if __name__ == '__main__':
    main()
