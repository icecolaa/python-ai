import os
from openai import OpenAI

client = OpenAI(
    # API密钥
    api_key=os.getenv("STEP_API_KEY"),
    base_url="https://api.stepfun.com/v1",
)

# 1、初始化一个空列表 用于存储聊天记录
messages = []

# 2、开始循环对话
while True:
    # 3、用户输入 并 判断
    user_input = input("用户：")
    if user_input == "退出":
        break
    # 4、将用户 问 存起来
    messages.append({"role": "user", "content": user_input})
    # 5、发起请求，让LLM回复
    response = client.chat.completions.create(
        model="step-5-preview",
        messages=messages
    )

    # 6、解析并输出结果
    ai_reply = response.choices[0].message.content
    print(f"AI助手：{ai_reply}")

    # 7、讲 AI 的 答 存起来
    messages.append({"role": "assistant", "content": ai_reply})
