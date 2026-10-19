[代码.zip](https://www.yuque.com/attachments/yuque/0/2026/zip/35881593/1784539957140-e1f21031-98dd-4733-938f-35bdb7937f61.zip)

[Miniconda3-latest-Windows-x86_64.7z](https://www.yuque.com/attachments/yuque/0/2026/7z/35881593/1784539957269-2e743369-9259-46b5-9f8c-ad1bac5213b1.7z)

# <font style="color:rgb(51, 51, 51);">Python 基础与环境搭建</font>
**<font style="color:rgb(51, 51, 51);">核心驱动问题</font>**<font style="color:rgb(51, 51, 51);">：我们要开始大模型应用开发了，需要写 Python 代码，但为什么不同的项目总因为环境问题跑不起来？怎么才能快速、干净地搭建一套属于自己的 Python 开发环境，让后续学习零障碍？</font>

---

## <font style="color:rgb(51, 51, 51);">1. Python 语言简介与发展历程</font>
### <font style="color:rgb(51, 51, 51);">1.1 为什么选择 Python？</font>
+ **<font style="color:rgb(51, 51, 51);">简洁易读</font>**<font style="color:rgb(51, 51, 51);">：语法接近自然语言，强制缩进使代码结构清晰，非常适合快速原型开发。</font>
+ **<font style="color:rgb(51, 51, 51);">“胶水语言”</font>**<font style="color:rgb(51, 51, 51);">：能轻松调用 C/C++ 等底层代码，兼顾开发速度和运行性能。</font>
+ **<font style="color:rgb(51, 51, 51);">生态庞大</font>**<font style="color:rgb(51, 51, 51);">：拥有 PyPI 数十万第三方库，覆盖 Web、AI、爬虫、自动化运维等几乎所有领域。</font>
+ **<font style="color:rgb(51, 51, 51);">AI 领域统治力</font>**<font style="color:rgb(51, 51, 51);">：NumPy、Pandas、TensorFlow、PyTorch 等核心库使 Python 成为人工智能与数据科学的事实标准。</font>

### <font style="color:rgb(51, 51, 51);">1.2 发展里程碑（精简版）</font>
| **<font style="color:rgb(51, 51, 51);">时间</font>** | **<font style="color:rgb(51, 51, 51);">版本</font>** | **<font style="color:rgb(51, 51, 51);">核心变化与意义</font>** |
| :--- | :--- | :--- |
| <font style="color:rgb(51, 51, 51);">1989-1991</font> | <font style="color:rgb(51, 51, 51);">0.9.0 发布</font> | <font style="color:rgb(51, 51, 51);">Guido van Rossum 创造，初衷是填补 C 和 Shell 之间的空白，名字源自喜剧团体 Monty Python。</font> |
| <font style="color:rgb(51, 51, 51);">1994</font> | <font style="color:rgb(51, 51, 51);">1.0</font> | <font style="color:rgb(51, 51, 51);">引入 lambda、map、filter 等函数式工具。</font> |
| <font style="color:rgb(51, 51, 51);">2000</font> | <font style="color:rgb(51, 51, 51);">2.0</font> | <font style="color:rgb(51, 51, 51);">加入垃圾回收、Unicode 支持，社区驱动开发。</font> |
| <font style="color:rgb(51, 51, 51);">2008</font> | <font style="color:rgb(51, 51, 51);">3.0</font> | <font style="color:rgb(51, 51, 51);">彻底重构，不完全向下兼容（print 变为函数，默认 Unicode），进入 2.x 与 3.x 长期共存期。</font> |
| <font style="color:rgb(51, 51, 51);">2015+</font> | <font style="color:rgb(51, 51, 51);">—</font> | <font style="color:rgb(51, 51, 51);">TensorFlow、PyTorch 等框架出现，Python 在深度学习中确立统治地位。</font> |
| <font style="color:rgb(51, 51, 51);">2020</font> | <font style="color:rgb(51, 51, 51);">2.7 退役</font> | <font style="color:rgb(51, 51, 51);">官方停止维护 Python 2，社区全面转向 Python 3。</font> |
| <font style="color:rgb(51, 51, 51);">2022-至今</font> | <font style="color:rgb(51, 51, 51);">3.11-3.13</font> | <font style="color:rgb(51, 51, 51);">解释器性能大幅提升（“香农计划”），引入 match/case 结构模式匹配、类型提示等现代特性。</font> |


**<font style="color:rgb(119, 119, 119);">学习提示</font>**<font style="color:rgb(119, 119, 119);">：本课程所有代码均基于 </font>**<font style="color:rgb(119, 119, 119);">Python 3.10 及以上</font>**<font style="color:rgb(119, 119, 119);"> 版本，请务必不要再安装 Python 2。</font>

---

## <font style="color:rgb(51, 51, 51);">2. Python 解释器安装（Windows 实操）</font>
<font style="color:rgb(51, 51, 51);">解释器是运行 Python 代码的基础。我们安装最新稳定版（推荐 3.11 或 3.12）。</font>

**<font style="color:rgb(51, 51, 51);">步骤演示</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. <font style="color:rgb(51, 51, 51);">访问 </font>[<font style="color:rgb(65, 131, 196);">python.org</font>](https://www.python.org/)<font style="color:rgb(51, 51, 51);"> ，下载 </font>**<font style="color:rgb(51, 51, 51);">Windows installer (64-bit)</font>**<font style="color:rgb(51, 51, 51);">。</font>
2. <font style="color:rgb(51, 51, 51);">双击安装包，</font>**<font style="color:rgb(51, 51, 51);">务必勾选“Add python.exe to PATH”</font>**<font style="color:rgb(51, 51, 51);">（这样可以在命令行直接使用 </font>`<font style="color:rgb(51, 51, 51);background-color:rgb(243, 244, 244);">python</font>`<font style="color:rgb(51, 51, 51);"> 命令）。</font>
3. <font style="color:rgb(51, 51, 51);">选择“Customize installation”可自定义路径（如 </font>`<font style="color:rgb(51, 51, 51);background-color:rgb(243, 244, 244);">D:\Python312</font>`<font style="color:rgb(51, 51, 51);">），并确保勾选 </font>`<font style="color:rgb(51, 51, 51);background-color:rgb(243, 244, 244);">pip</font>`<font style="color:rgb(51, 51, 51);"> 和 </font>`<font style="color:rgb(51, 51, 51);background-color:rgb(243, 244, 244);">tcl/tk</font>`<font style="color:rgb(51, 51, 51);"> 组件。</font>
4. <font style="color:rgb(51, 51, 51);">安装完成后，打开 </font>**<font style="color:rgb(51, 51, 51);">命令提示符</font>**<font style="color:rgb(51, 51, 51);"> 验证：</font>

```bash
python --version
# 输出示例：Python 3.12.3
pip list
```

<img src="https://cdn.nlark.com/yuque/0/2026/png/35881593/1779876053663-e933b143-bf3d-4d95-b0c3-198fc391ac6b.png" width="1122.4" alt="" title="" crop="0,0,1,1" id="u65b4373e" class="ne-image">

---

## <font style="color:rgb(51, 51, 51);">3. 集成开发环境（IDE）选择与配置</font>
<font style="color:rgb(51, 51, 51);">好的工具能提升数倍效率，我们介绍三款主流 IDE，重点演示 </font>**<font style="color:rgb(51, 51, 51);">VSCode</font>**<font style="color:rgb(51, 51, 51);">（轻量全栈）与 </font>**<font style="color:rgb(51, 51, 51);">PyCharm</font>**<font style="color:rgb(51, 51, 51);">（专业强大），并让 </font>**<font style="color:rgb(51, 51, 51);">Jupyter Notebook</font>**<font style="color:rgb(51, 51, 51);"> 成为数据分析演示利器。</font>

### <font style="color:rgb(51, 51, 51);">3.1 Visual Studio Code（推荐，全栈通用）</font>
+ **<font style="color:rgb(51, 51, 51);">特点</font>**<font style="color:rgb(51, 51, 51);">：微软开源免费，启动快，插件丰富，适合前后端、脚本等多语言开发。</font>
+ **<font style="color:rgb(51, 51, 51);">快速上手</font>**<font style="color:rgb(51, 51, 51);">：</font>
    1. <font style="color:rgb(51, 51, 51);">下载安装 </font>[<font style="color:rgb(65, 131, 196);">VSCode</font>](https://code.visualstudio.com/)<font style="color:rgb(51, 51, 51);">。</font>
    2. <font style="color:rgb(51, 51, 51);">打开 VSCode，点击左侧扩展图标，搜索 </font>`<font style="color:rgb(51, 51, 51);background-color:rgb(243, 244, 244);">Python</font>`<font style="color:rgb(51, 51, 51);"> 并安装官方插件。</font>
    3. <font style="color:rgb(51, 51, 51);">按 </font>`<font style="color:rgb(51, 51, 51);background-color:rgb(243, 244, 244);">Ctrl+Shift+P</font>`<font style="color:rgb(51, 51, 51);"> 打开命令面板，输入 </font>`<font style="color:rgb(51, 51, 51);background-color:rgb(243, 244, 244);">Python: Select Interpreter</font>`<font style="color:rgb(51, 51, 51);">，选择已安装的 Python（或稍后创建的虚拟环境）。</font>
    4. <font style="color:rgb(51, 51, 51);">新建 </font>`<font style="color:rgb(51, 51, 51);background-color:rgb(243, 244, 244);">.py</font>`<font style="color:rgb(51, 51, 51);"> 文件，输入 </font>`<font style="color:rgb(51, 51, 51);background-color:rgb(243, 244, 244);">print("Hello, AI")</font>`<font style="color:rgb(51, 51, 51);">，点击右上角 </font><font style="color:rgb(51, 51, 51);">▶</font><font style="color:rgb(51, 51, 51);"> 运行。</font>

### <font style="color:rgb(51, 51, 51);">3.2 PyCharm（专业大型项目首选）</font>
+ **<font style="color:rgb(51, 51, 51);">版本</font>**<font style="color:rgb(51, 51, 51);">：社区版（免费）足够日常学习，专业版增加 Web 框架与数据库工具。</font>
+ **<font style="color:rgb(51, 51, 51);">关键配置</font>**<font style="color:rgb(51, 51, 51);">：</font>
    1. <font style="color:rgb(51, 51, 51);">下载安装 </font>[<font style="color:rgb(65, 131, 196);">PyCharm</font>](https://www.jetbrains.com/pycharm/)
    2. <font style="color:rgb(51, 51, 51);">安装时勾选“创建桌面快捷方式”和“关联 .py 文件”。</font>
    3. <font style="color:rgb(51, 51, 51);">首次打开选择“Do not import settings”。</font>
    4. <font style="color:rgb(51, 51, 51);">新建项目时，可自动创建虚拟环境（推荐），并在右下角解释器选择器中确认使用正确的 Python。</font>
    5. <img src="https://cdn.nlark.com/yuque/0/2026/png/35881593/1779876039683-412ea65f-5f3d-4785-8e5a-64bcc8037bb4.png" width="529.6" alt="" title="" crop="0,0,1,1" id="u8f9cfea7" class="ne-image">

### <font style="color:rgb(51, 51, 51);">3.3 Jupyter Notebook / Lab（数据探索与教学演示）</font>
+ **<font style="color:rgb(51, 51, 51);">特点</font>**<font style="color:rgb(51, 51, 51);">：浏览器交互，代码、图表、Markdown 混合编写，最适合数据分析与逐步演示。</font>
+ **<font style="color:rgb(51, 51, 51);">安装与使用</font>**<font style="color:rgb(51, 51, 51);">：</font>

```bash
# 注意在项目路径下进入终端
pip install notebook -i https://pypi.tuna.tsinghua.edu.cn/simple    
jupyter lab             # 启动后浏览器自动打开
```

<font style="color:rgb(119, 119, 119);">1、亦可在 VSCode 中进入扩展界面，搜索“jupyter”安装，然后新建 </font>`<font style="color:rgb(119, 119, 119);background-color:rgb(243, 244, 244);">.ipynb</font>`<font style="color:rgb(119, 119, 119);"> 文件，直接获得同等交互体验。</font>

<font style="color:rgb(119, 119, 119);">2、同样可以在新版的PyCharm中新建Jupyter Notebook文件，点击运行安装内核，获取同等交互体验。</font>

---

## <font style="color:rgb(51, 51, 51);">4. 包管理利器：pip 与镜像加速</font>
<font style="color:rgb(51, 51, 51);">Python 的强大离不开第三方库，</font>`<font style="color:rgb(51, 51, 51);background-color:rgb(243, 244, 244);">pip</font>`<font style="color:rgb(51, 51, 51);"> 是官方包管理器，用于安装、卸载和管理依赖。</font>

### <font style="color:rgb(51, 51, 51);">4.1 常用命令速查</font>
```bash
pip install <包名>                  # 安装最新版
pip install <包名>==<版本号>        # 安装指定版本（如 django==4.2）
pip install -r requirements.txt    # 批量安装项目所有依赖
pip freeze > requirements.txt      # 导出当前环境依赖，方便移植
pip uninstall <包名>               # 卸载包
pip list                            # 查看安装列表
pip show <包名>                   # 显示安装包的信息
```

### <font style="color:rgb(51, 51, 51);">4.2 配置国内镜像源（提速必备）</font>
<font style="color:rgb(51, 51, 51);">默认从国外服务器下载很慢，可永久配置清华源。</font><font style="color:rgb(51, 51, 51);">在 Windows 文件管理器地址栏输入 </font>`<font style="color:rgb(51, 51, 51);background-color:rgb(243, 244, 244);">%APPDATA%</font>`<font style="color:rgb(51, 51, 51);"> 回车，新建 </font>`<font style="color:rgb(51, 51, 51);background-color:rgb(243, 244, 244);">pip</font>`<font style="color:rgb(51, 51, 51);"> 文件夹，在其中新建 </font>`<font style="color:rgb(51, 51, 51);background-color:rgb(243, 244, 244);">pip.ini</font>`<font style="color:rgb(51, 51, 51);"> 文件，写入：</font>

```bash
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
extra-index-url = https://mirrors.aliyun.com/pypi/simple/
```

<font style="color:rgb(51, 51, 51);">临时使用：</font>`<font style="color:rgb(51, 51, 51);background-color:rgb(243, 244, 244);">pip install <包名> -i https://pypi.tuna.tsinghua.edu.cn/simple</font>`

---

## <font style="color:rgb(51, 51, 51);">5. 虚拟环境管理——解决环境冲突的银弹</font>
**<font style="color:rgb(51, 51, 51);">痛点</font>**<font style="color:rgb(51, 51, 51);">：项目 A 要用 Django 3.2，项目 B 要用 Django 4.2，直接装系统全局会冲突。</font><font style="color:rgb(51, 51, 51);">虚拟环境为每个项目创建独立的 Python 解释器环境，各自拥有独立的包，互不干扰。</font>

### <font style="color:rgb(51, 51, 51);">5.1 使用 Python 内置 venv（轻量快捷）</font>
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

### <font style="color:rgb(51, 51, 51);">5.2 使用 Conda（数据科学与多语言环境首选）</font>
<font style="color:rgb(51, 51, 51);">Conda 可管理 Python 自身版本以及 C 扩展包，尤其适合 AI 领域。</font>

1. <font style="color:rgb(51, 51, 51);">下载并安装 </font>[<font style="color:rgb(65, 131, 196);">Miniconda</font>](https://docs.anaconda.com/miniconda/)<font style="color:rgb(51, 51, 51);">（体积小，仅包含 conda + Python）。</font>
2. <font style="color:rgb(51, 51, 51);">安装时务必勾选“Add to PATH”（或安装后手动配置环境变量：将 </font>`<font style="color:rgb(51, 51, 51);background-color:rgb(243, 244, 244);">D:\conda</font>`<font style="color:rgb(51, 51, 51);"> 及 </font>`<font style="color:rgb(51, 51, 51);background-color:rgb(243, 244, 244);">D:\conda\Scripts</font>`<font style="color:rgb(51, 51, 51);"> 加入系统 Path）。</font>
3. <font style="color:rgb(51, 51, 51);">验证：打开新终端，输入 </font>`<font style="color:rgb(51, 51, 51);background-color:rgb(243, 244, 244);">conda --version</font>`<font style="color:rgb(51, 51, 51);"> 显示版本即成功。</font>
4. <font style="color:rgb(51, 51, 51);">基本命令：</font>

```bash
conda create -n aicourse python=3.11   # 创建指定 Python 版本的环境
conda activate aicourse                # 激活环境
pip install numpy pandas               # 安装科学计算包
conda deactivate                       # 退出
conda env list                         # 查看所有环境
conda env remove -n aicourse           # 删除环境
```

**<font style="color:rgb(119, 119, 119);">注意</font>**<font style="color:rgb(119, 119, 119);">：激活 conda 环境后，</font>`<font style="color:rgb(119, 119, 119);background-color:rgb(243, 244, 244);">pip</font>`<font style="color:rgb(119, 119, 119);"> 和 </font>`<font style="color:rgb(119, 119, 119);background-color:rgb(243, 244, 244);">conda</font>`<font style="color:rgb(119, 119, 119);"> 安装的包都会进入该环境，互不影响。 </font>

### <font style="color:rgb(51, 51, 51);">5.3 理解系统 Python 与环境 Python</font>
+ **<font style="color:rgb(51, 51, 51);">系统 Python</font>**<font style="color:rgb(51, 51, 51);">：安装在操作系统 Path 中的解释器，用于全局调用。</font>
+ **<font style="color:rgb(51, 51, 51);">环境 Python</font>**<font style="color:rgb(51, 51, 51);">：由 venv/conda 创建的某个目录下的解释器副本，激活后覆盖系统默认 Python。</font><font style="color:rgb(51, 51, 51);">养成“</font>**<font style="color:rgb(51, 51, 51);">一个项目一个环境</font>**<font style="color:rgb(51, 51, 51);">”的习惯，是专业开发的基本素养。</font>

  
 
