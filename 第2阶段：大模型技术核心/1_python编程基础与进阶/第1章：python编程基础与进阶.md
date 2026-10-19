[代码.zip](https://www.yuque.com/attachments/yuque/0/2026/zip/35881593/1784539957140-e1f21031-98dd-4733-938f-35bdb7937f61.zip)

[Miniconda3-latest-Windows-x86_64.7z](https://www.yuque.com/attachments/yuque/0/2026/7z/35881593/1784539957269-2e743369-9259-46b5-9f8c-ad1bac5213b1.7z)

# Python 基础与环境搭建
**核心驱动问题**：我们要开始大模型应用开发了，需要写 Python 代码，但为什么不同的项目总因为环境问题跑不起来？怎么才能快速、干净地搭建一套属于自己的 Python 开发环境，让后续学习零障碍？

---

## 1. Python 语言简介与发展历程
### 1.1 为什么选择 Python？
+ **简洁易读**：语法接近自然语言，强制缩进使代码结构清晰，非常适合快速原型开发。
+ **“胶水语言”**：能轻松调用 C/C++ 等底层代码，兼顾开发速度和运行性能。
+ **生态庞大**：拥有 PyPI 数十万第三方库，覆盖 Web、AI、爬虫、自动化运维等几乎所有领域。
+ **AI 领域统治力**：NumPy、Pandas、TensorFlow、PyTorch 等核心库使 Python 成为人工智能与数据科学的事实标准。

### 1.2 发展里程碑（精简版）
| **时间** | **版本** | **核心变化与意义** |
| :--- | :--- | :--- |
| 1989-1991 | 0.9.0 发布 | Guido van Rossum 创造，初衷是填补 C 和 Shell 之间的空白，名字源自喜剧团体 Monty Python。 |
| 1994 | 1.0 | 引入 lambda、map、filter 等函数式工具。 |
| 2000 | 2.0 | 加入垃圾回收、Unicode 支持，社区驱动开发。 |
| 2008 | 3.0 | 彻底重构，不完全向下兼容（print 变为函数，默认 Unicode），进入 2.x 与 3.x 长期共存期。 |
| 2015+ | — | TensorFlow、PyTorch 等框架出现，Python 在深度学习中确立统治地位。 |
| 2020 | 2.7 退役 | 官方停止维护 Python 2，社区全面转向 Python 3。 |
| 2022-至今 | 3.11-3.13 | 解释器性能大幅提升（“香农计划”），引入 match/case 结构模式匹配、类型提示等现代特性。 |

**学习提示**：本课程所有代码均基于 **Python 3.10 及以上** 版本，请务必不要再安装 Python 2。

---

## 2. Python 解释器安装（Windows 实操）
解释器是运行 Python 代码的基础。我们安装最新稳定版（推荐 3.11 或 3.12）。

**步骤演示**：

1. 访问 [python.org](https://www.python.org/) ，下载 **Windows installer (64-bit)**。
2. 双击安装包，**务必勾选“Add python.exe to PATH”**（这样可以在命令行直接使用 `python` 命令）。
3. 选择“Customize installation”可自定义路径（如 `D:\Python312`），并确保勾选 `pip` 和 `tcl/tk` 组件。
4. 安装完成后，打开 **命令提示符** 验证：

```bash
python --version
# 输出示例：Python 3.12.3
pip list
```

![插图](https://cdn.nlark.com/yuque/0/2026/png/35881593/1779876053663-e933b143-bf3d-4d95-b0c3-198fc391ac6b.png)

---

## 3. 集成开发环境（IDE）选择与配置
好的工具能提升数倍效率，我们介绍三款主流 IDE，重点演示 **VSCode**（轻量全栈）与 **PyCharm**（专业强大），并让 **Jupyter Notebook** 成为数据分析演示利器。

### 3.1 Visual Studio Code（推荐，全栈通用）
+ **特点**：微软开源免费，启动快，插件丰富，适合前后端、脚本等多语言开发。
+ **快速上手**：
    1. 下载安装 [VSCode](https://code.visualstudio.com/)。
    2. 打开 VSCode，点击左侧扩展图标，搜索 `Python` 并安装官方插件。
    3. 按 `Ctrl+Shift+P` 打开命令面板，输入 `Python: Select Interpreter`，选择已安装的 Python（或稍后创建的虚拟环境）。
    4. 新建 `.py` 文件，输入 `print("Hello, AI")`，点击右上角 ▶ 运行。

### 3.2 PyCharm（专业大型项目首选）
+ **版本**：社区版（免费）足够日常学习，专业版增加 Web 框架与数据库工具。
+ **关键配置**：
    1. 下载安装 [PyCharm](https://www.jetbrains.com/pycharm/)
    2. 安装时勾选“创建桌面快捷方式”和“关联 .py 文件”。
    3. 首次打开选择“Do not import settings”。
    4. 新建项目时，可自动创建虚拟环境（推荐），并在右下角解释器选择器中确认使用正确的 Python。
    5. ![插图](https://cdn.nlark.com/yuque/0/2026/png/35881593/1779876039683-412ea65f-5f3d-4785-8e5a-64bcc8037bb4.png)

### 3.3 Jupyter Notebook / Lab（数据探索与教学演示）
+ **特点**：浏览器交互，代码、图表、Markdown 混合编写，最适合数据分析与逐步演示。
+ **安装与使用**：

```bash
# 注意在项目路径下进入终端
pip install notebook -i https://pypi.tuna.tsinghua.edu.cn/simple    
jupyter lab             # 启动后浏览器自动打开
```

1、亦可在 VSCode 中进入扩展界面，搜索“jupyter”安装，然后新建 `.ipynb` 文件，直接获得同等交互体验。

2、同样可以在新版的PyCharm中新建Jupyter Notebook文件，点击运行安装内核，获取同等交互体验。

---

## 4. 包管理利器：pip 与镜像加速
Python 的强大离不开第三方库，`pip` 是官方包管理器，用于安装、卸载和管理依赖。

### 4.1 常用命令速查
```bash
pip install <包名>                  # 安装最新版
pip install <包名>==<版本号>        # 安装指定版本（如 django==4.2）
pip install -r requirements.txt    # 批量安装项目所有依赖
pip freeze > requirements.txt      # 导出当前环境依赖，方便移植
pip uninstall <包名>               # 卸载包
pip list                            # 查看安装列表
pip show <包名>                   # 显示安装包的信息
```

### 4.2 配置国内镜像源（提速必备）
默认从国外服务器下载很慢，可永久配置清华源。在 Windows 文件管理器地址栏输入 `%APPDATA%` 回车，新建 `pip` 文件夹，在其中新建 `pip.ini` 文件，写入：

```bash
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
extra-index-url = https://mirrors.aliyun.com/pypi/simple/
```

临时使用：`pip install <包名> -i https://pypi.tuna.tsinghua.edu.cn/simple`

---

## 5. 虚拟环境管理——解决环境冲突的银弹
**痛点**：项目 A 要用 Django 3.2，项目 B 要用 Django 4.2，直接装系统全局会冲突。虚拟环境为每个项目创建独立的 Python 解释器环境，各自拥有独立的包，互不干扰。

### 5.1 使用 Python 内置 venv（轻量快捷）
```bash
# 在项目根目录打开终端
python -m venv myenv          # 创建名为 myenv 的虚拟环境
# 激活（Windows）
myenv\Scripts\activate
# 激活（macOS/Linux）
source myenv/bin/activate
# 现在命令行前缀会显示 (myenv)，用 pip 安装的包只在此环境生效
pip install numpy
# 退出虚拟环境
deactivate
```

### 5.2 使用 Conda（数据科学与多语言环境首选）
Conda 可管理 Python 自身版本以及 C 扩展包，尤其适合 AI 领域。

1. 下载并安装 [Miniconda](https://docs.anaconda.com/miniconda/)（体积小，仅包含 conda + Python）。
2. 安装时务必勾选“Add to PATH”（或安装后手动配置环境变量：将 `D:\conda` 及 `D:\conda\Scripts` 加入系统 Path）。
3. 验证：打开新终端，输入 `conda --version` 显示版本即成功。
4. 基本命令：

```bash
conda create -n aicourse python=3.11   # 创建指定 Python 版本的环境
conda activate aicourse                # 激活环境
pip install numpy pandas               # 安装科学计算包
conda deactivate                       # 退出
conda env list                         # 查看所有环境
conda env remove -n aicourse           # 删除环境
```

**注意**：激活 conda 环境后，`pip` 和 `conda` 安装的包都会进入该环境，互不影响。

### 5.3 理解系统 Python 与环境 Python
+ **系统 Python**：安装在操作系统 Path 中的解释器，用于全局调用。
+ **环境 Python**：由 venv/conda 创建的某个目录下的解释器副本，激活后覆盖系统默认 Python。养成“**一个项目一个环境**”的习惯，是专业开发的基本素养。
