import os
import requests
import time

# 这里是你想要生成的视频画面描述，你可以随意修改它（英文效果更好）
PROMPT = "A beautiful sunset over a calm ocean, cinematic lighting, 4k resolution"

# 调用的免费 AI 视频生成模型接口
API_URL = "https://api-inference.huggingface.co/models/cerspense/zeroscope_v2_576w"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response

print(f"正在向 AI 发送请求，提示词: '{PROMPT}'...")
response = query({"inputs": PROMPT})

# 如果 AI 模型正在启动，等待并重试
if response.status_code == 503:
    print("模型正在启动，请稍候...")
    time.sleep(20)
    response = query({"inputs": PROMPT})

if response.status_code == 200:
    with open("output_video.mp4", "wb") as f:
        f.write(response.content)
    print("视频生成成功！已保存为 output_video.mp4")
else:
    print(f"生成失败，错误代码: {response.status_code}")
    print(response.text)
