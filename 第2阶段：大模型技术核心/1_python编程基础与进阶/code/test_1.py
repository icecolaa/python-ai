import os

# ✅ 正确：跨平台路径拼接
log_dir = "my_project"
log_file = "app.log"
full_path = os.path.join(log_dir, "logs", log_file)
print(full_path)  # Windows: my_project\logs\app.log  Linux/Mac: my_project/logs/app.log

# 获取当前文件所在目录（常用）
current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)


# 列出目录下所有文件
files = os.listdir('.')
print(files)

print("*"*100)
for root, dirs, files in os.walk(current_dir):
    print('当前目录: ', root)
    print('子目录列表: ', dirs)
    print('文件列表: ', files)