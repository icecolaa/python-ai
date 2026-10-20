# PythonAI — 大模型应用开发学习仓库

从零基础到企业级大模型开发工程师的实战代码仓库，按课程阶段组织，每个阶段配套可运行的练手项目。

## 学习日历

双击打开 [PythonAI-学习计划.html](./PythonAI-学习计划.html)。从 2026-10-20 的 2.1 Python 编程基础与进阶开始，工作日每天 2 小时，周六、周日各 4 小时；剩余 144 小时初始预计在 2026-12-14 完成，其中 2.1 的 16 小时安排至 2026-10-25。

点击日历日期查看每日任务及文档链接。完成后勾选 √，未完成任务可指定新日期或顺延至空闲日；超出当天预算会显示提示。进度保存在当前浏览器，支持 JSON 备份导入导出。资料尚未收录的任务会标注并链接至课程大纲。

重新生成页面（资料库生成脚本需要 Markdown、lxml，可选 Pillow）：

```powershell
python scripts/build_library_html.py
python scripts/study_plan.py
```

每个阶段和全部课程的时长汇总由原课程表自动计算，完整课程共 145 小时。

## 目录结构

```
PythonAI/
└── 第1阶段：大模型开发入门/
    ├── 入门.md                     # 课程讲义：大模型原理 + API 调用入门
    ├── 大模型应用开发全栈.html      # 课程总览（学习路线与项目清单）
    └── llm_project/
        ├── 02-单轮对话机器人.py     # 单轮对话：发一条，回一条
        ├── 02-多轮对话机器人.py     # 多轮对话：维护 messages 列表实现上下文记忆
        └── demo_vs.py              # 接口调用演示
```

## 环境准备

- Python 3.9+（推荐 3.10 / 3.11）
- 依赖安装：

```bash
pip install openai
```

## 配置 API Key（必读）

**不要把密钥写死在代码里。** 所有示例都从环境变量读取，请先在系统里配置：

当前示例（阶跃星辰）使用 `STEP_API_KEY`，按你实际接入的平台设置对应变量即可：

```bash
# macOS / Linux
export STEP_API_KEY="你的密钥"
export DASHSCOPE_API_KEY="你的密钥"      # 阿里云百炼
export SILICONFLOW_API_KEY="你的密钥"    # 硅基流动

# Windows PowerShell
$env:STEP_API_KEY="你的密钥"
$env:DASHSCOPE_API_KEY="你的密钥"
$env:SILICONFLOW_API_KEY="你的密钥"
```

也可以在仓库根目录新建 `.env` 文件（已被 `.gitignore` 忽略，不会提交）：

```
STEP_API_KEY=你的密钥
DASHSCOPE_API_KEY=你的密钥
SILICONFLOW_API_KEY=你的密钥
```

### 密钥获取渠道

| 平台 | 地址 | 环境变量 |
| --- | --- | --- |
| 阶跃星辰 | platform.stepfun.com | `STEP_API_KEY` |
| 阿里云百炼 | bailian.console.aliyun.com | `DASHSCOPE_API_KEY` |
| 硅基流动 SiliconFlow | account.siliconflow.cn | `SILICONFLOW_API_KEY` |
| 百度千帆 | console.bce.baidu.com/qianfan | 自定义 |

> ⚠️ API Key 等同于账号密码。一旦泄露请立即到平台禁用并重新创建。

## 运行示例

```bash
cd "第1阶段：大模型开发入门/llm_project"

python 02-单轮对话机器人.py
python 02-多轮对话机器人.py    # 输入「退出」结束对话
```

## 学习路线

| 阶段 | 主题 | 核心内容 |
| --- | --- | --- |
| 第一阶段 | 大模型开发入门 | API 调用原理、单轮/多轮对话机器人 |
| 第二阶段 | 大模型技术核心 | Python 进阶、数据处理、机器学习基础 |
| 第三阶段 | NLP 核心 | 深度学习、RNN、Transformer |
| 第四阶段 | 大模型技术进阶 | 微调与部署、Agent、RAG |
| 第五阶段 | 多模态大模型 | OpenCV、CNN/YOLO、语音 |
| 第六阶段 | 具身智能 | PyBullet 仿真、LLM 驱动决策 |

详细的知识点课时安排与项目清单见 [`第1阶段：大模型开发入门/大模型应用开发全栈.html`](./第1阶段：大模型开发入门/大模型应用开发全栈.html)。

## 贡献与规范

- 提交前请确认代码中**不含任何明文 API Key**，一律使用环境变量。
- 示例脚本保持简洁可读，优先服务于教学理解。
