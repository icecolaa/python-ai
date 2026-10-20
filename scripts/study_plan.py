"""Build the offline study calendar; course hours come from the library table."""
import json
import re
from pathlib import Path

from lxml import etree, html

ROOT = Path(__file__).resolve().parent.parent
LIBRARY = ROOT / 'PythonAI-学习资料库.html'


def add_course_summary(root):
    """Add computed totals to the roadmap without changing its chapter anchors."""
    for table in root.xpath('.//table'):
        if not table.xpath('.//th[contains(., "课时（60") ]'):
            continue
        if table.get('data-course-hours') or table.find('tfoot') is not None:
            continue
        stages = []
        for row in table.xpath('./tbody/tr'):
            cells = row.findall('td')
            if len(cells) != 4:
                continue
            stage = ''.join(cells[0].itertext()).strip()
            if stage:
                stages.append([stage, 0, row])
            stages[-1][1] += int(''.join(cells[3].itertext()).strip())
            stages[-1][2] = row
        total = sum(hours for _, hours, _ in stages)
        table.set('data-course-hours', str(total))
        for name, hours, last_row in stages:
            row = etree.Element('tr', {'class': 'stage-summary'})
            label = etree.SubElement(row, 'th', colspan='3', scope='row')
            label.text = name + '时长汇总'
            etree.SubElement(row, 'td').text = f'{hours}小时'
            last_row.addnext(row)
        foot = etree.SubElement(table, 'tfoot')
        row = etree.SubElement(foot, 'tr')
        label = etree.SubElement(row, 'th', colspan='3', scope='row')
        label.text = '全部阶段总时长'
        etree.SubElement(row, 'td').text = f'{total}小时'
        note = html.fragment_fromstring('<p class="course-summary">按原表每课时 60 分钟计算，包含第一阶段 1 小时；实际练习可按掌握情况延长。 <a href="PythonAI-学习计划.html">打开日历学习计划 →</a></p>')
        table.addprevious(note)


PYTHON_TOPICS = [
    ('环境搭建与虚拟环境', 'doc-ch01', '安装解释器、配置编辑器，创建 venv 并导出依赖。'),
    ('变量、输入输出与计算器', 'doc-ch02', '独立编写带输入校验的简易计算器。'),
    ('数字、字符串与类型转换', 'doc-ch03-s1', '练习切片、格式化、类型转换及边界输入。'),
    ('列表、元组、集合与字典', 'doc-ch03-s3', '实现成绩数据的增删改查，比较深拷贝与浅拷贝。'),
    ('分支、循环与推导式', 'doc-ch04', '完成猜数字游戏，处理退出和错误输入。'),
    ('函数、参数与作用域', 'doc-ch05-s1', '将成绩统计拆为可复用函数，练习各类参数。'),
    ('闭包、装饰器与生成器', 'doc-ch05-s3', '编写日志装饰器和惰性读取生成器；生成器内容参考大纲补充。'),
    ('类与对象、封装与继承', 'doc-ch06', '用类重构学生管理系统，演示继承与多态。'),
    ('文件、路径与持久化', 'doc-ch07', '将学生数据保存为 JSON，重新读取并处理大文件。'),
    ('模块、异常与正则', 'doc-ch08', '拆分包结构，增加异常兜底与输入验证。'),
    ('协程与异步并发', 'doc-ch09', '用 async/await 和信号量实现受控并发请求。'),
    ('进程、线程与 GIL', 'doc-start-s2-4', '补充大纲专题：比较 CPU / I/O 任务，编写线程池示例。'),
    ('网络请求与 TCP / UDP', 'doc-start-s2-4', '补充大纲专题：实现带超时和错误处理的网络客户端。'),
    ('MQTT 消息收发', 'doc-start-s2-4', '补充大纲专题：在本地测试服务上完成发布与订阅。'),
    ('Git 分支与版本管理', 'doc-start-s2-4', '补充大纲专题：创建练习分支，提交代码并演练冲突解决。'),
    ('Python 综合复盘', 'doc-ch08-s5', '整合文件配置、异常和异步调用；整理 README 并自测。'),
]


def build_plan():
    root = html.fromstring(LIBRARY.read_text(encoding='utf-8'))
    table = root.xpath('//table[.//th[contains(., "课时（60")]]')[0]
    tasks = []
    stage = ''
    for row in table.xpath('./tbody/tr'):
        cells = row.findall('td')
        if len(cells) != 4:
            continue
        stage = cells[0].text_content().strip() or stage
        module = cells[1].text_content().strip()
        hours = int(cells[3].text_content().strip())
        if '第一阶段' in stage:
            continue
        if module.startswith('2.1'):
            topics = PYTHON_TOPICS
        else:
            points = re.split(r'(?<!\d)\d+\.\s+', cells[2].text_content())
            points = [p.strip() for p in points if p.strip()]
            topics = []
            indices = [min(len(points) - 1, i * len(points) // hours) for i in range(hours)]
            for i in range(hours):
                point_index = indices[i]
                point = points[point_index]
                title = re.split(r'[（(、]', point)[0].strip()
                part = indices[:i].count(point_index)
                activity = [
                    ('理解与示例', '梳理概念并运行最小示例，写下输入、输出与关键步骤'),
                    ('编码与验证', '独立实现一个小练习，验证正常输入和边界情况'),
                    ('复盘与扩展', '定位一个常见问题，完善练习代码并记录解决方法'),
                ][min(part, 2)]
                topics.append((f'{title} · {activity[0]}', 'doc-start-s2-4', f'本节范围：{point}。任务：{activity[1]}。'))
        for i, (title, anchor, outcome) in enumerate(topics):
            tasks.append(dict(id=f't{len(tasks)+1:03}', stage=stage, module=module,
                              title=title, anchor=anchor, outcome=outcome,
                              hour=i+1, moduleHours=hours,
                              outline=anchor == 'doc-start-s2-4'))
    template = (ROOT / 'scripts/study_plan_template.html').read_text(encoding='utf-8')
    page = template.replace('@@TASKS@@', json.dumps(tasks, ensure_ascii=False).replace('</', '<\\/'))
    page = page.replace('@@CSS@@', (ROOT / 'scripts/study_plan.css').read_text(encoding='utf-8'))
    page = page.replace('@@JS@@', (ROOT / 'scripts/study_plan.js').read_text(encoding='utf-8'))
    (ROOT / 'PythonAI-学习计划.html').write_text(page, encoding='utf-8')
    print(f'Created study plan: {len(tasks)} hours')


if __name__ == '__main__':
    build_plan()
