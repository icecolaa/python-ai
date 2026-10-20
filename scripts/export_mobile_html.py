"""Package the existing self-contained HTML pages for offline mobile reading.

Usage: python scripts/export_mobile_html.py
"""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / 'outputs'
PAGES = ('PythonAI-学习资料库.html', 'PythonAI-学习计划.html')
INDEX = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PythonAI · 随身学习</title><style>
*{box-sizing:border-box}body{margin:0;background:#f3f7fc;color:#182940;font:16px/1.8 system-ui,"Microsoft YaHei",sans-serif}
main{max-width:680px;margin:8vh auto;padding:24px}small{color:#326be9;letter-spacing:.12em}h1{font-size:36px;line-height:1.3}
p{color:#61758d}a{display:block;background:white;padding:24px;margin:20px 0;border:1px solid #dfe8f2;border-radius:18px;color:#326be9;text-decoration:none}
a strong{display:block;font-size:21px}a span{display:block;font-size:14px;color:#61758d;margin-top:8px}footer{font-size:13px;color:#61758d;margin-top:30px}
</style></head><body><main><small>PYTHONAI / 随身学习</small><h1>随时打开，继续学习。</h1>
<p>适配手机和电脑，正文、样式与脚本均已内嵌，无需安装或联网加载。</p>
<a href="PythonAI-学习资料库.html"><strong>学习资料库 →</strong><span>完整课程正文、章节导航、课程路线与时长汇总</span></a>
<a href="PythonAI-学习计划.html"><strong>我的学习日历 →</strong><span>每日任务、完成勾选、改期与进度备份</span></a>
<footer>将 ZIP 传到手机并完整解压，保留三份 HTML 在同一目录，用支持 JavaScript 的浏览器打开本页。学习进度保存在当前浏览器，可在日历页导出备份；在线资料链接需要联网。</footer>
</main></body></html>'''


def main():
    # Read both pages before writing the bundle so a missing input fails early.
    pages = {name: (ROOT / name).read_bytes() for name in PAGES}
    target = OUTPUT / 'PythonAI-手机静态版'
    target.mkdir(parents=True, exist_ok=True)
    (target / 'index.html').write_text(INDEX, encoding='utf-8')
    for name, content in pages.items():
        (target / name).write_bytes(content)
    archive = OUTPUT / 'PythonAI-手机静态版.zip'
    with ZipFile(archive, 'w', ZIP_DEFLATED) as bundle:
        for name in ('index.html', *PAGES):
            bundle.write(target / name, arcname=name)
    print(f'HTML: {target / "index.html"}')
    print(f'ZIP: {archive}')


if __name__ == '__main__':
    main()
