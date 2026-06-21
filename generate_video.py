import os
import requests
import time

# 1. 自动读取你刚刚在 GitHub 网页上写的 prompt.txt 文件
if os.path.exists("prompt.txt"):
    with open("prompt.txt", "r", encoding="utf-8") as f:
        USER_PROMPT = f.read().strip()
else:
    USER_PROMPT = "A beautiful cinematic shot of a futuristic city"

print(f"📖 成功读取到你的自定义文本提示词: '{USER_PROMPT}'")

# 2. 调用 Hugging Face 上非常强大且稳定的开源文本转视频大模型 (ModelScope/AnimateDiff 核心)
API_URL = "https://api-inference.huggingface.co/models/damo-vilab/text-to-video-ms-1.7b"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

def query(payload):
    # 这里我们加入了超时和重试机制，防止网络波动
    for attempt in range(3):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            return response
        except Exception as e:
            print(f"网络连接略有延迟，正在进行第 {attempt + 1} 次重试...")
            time.sleep(5)
    return None

print("🚀 正在将你的文本发送给 AI 视频大模型，请稍候...")
response = query({"inputs": USER_PROMPT})

# 3. 如果模型处于睡眠状态需要唤醒，代码会自动等待并重新呼叫
if response and response.status_code == 503:
    print("⏰ AI 正在排队启动中，给它 25 秒热身时间...")
    time.sleep(25)
    response = query({"inputs": USER_PROMPT})

# 4. 保存生成的 MP4 视频
if response and response.status_code == 200:
    with open("output_video.mp4", "wb") as f:
        f.write(response.content)
    print("🎉 奇迹发生了！AI 已经根据你的文字成功生成了视频：output_video.mp4")
else:
    status_code = response.status_code if response else "Unknown"
    print(f"❌ 遭遇未知错误，代码: {status_code}。请确保你的 HF_TOKEN 密钥填写正确。")
