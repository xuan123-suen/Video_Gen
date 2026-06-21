import os

# 1. 自动读取你在 GitHub 上写的 prompt.txt 文件
if os.path.exists("prompt.txt"):
    with open("prompt.txt", "r", encoding="utf-8") as f:
        USER_PROMPT = f.read().strip()
else:
    USER_PROMPT = "Hello GitHub Video!"

print(f"📖 成功读取到你的自定义文本: '{USER_PROMPT}'")

# 2. 自动安装绘图和合成工具
print("正在配置视频生成引擎...")
os.system("pip install pillow")
from PIL import Image, ImageDraw, ImageFont

# 视频参数
width, height = 854, 480
fps = 24
duration_sec = 4
total_frames = fps * duration_sec

os.makedirs("frames", exist_ok=True)

print(f"正在根据你的文本 '{USER_PROMPT}' 逐帧渲染视频...")
# 3. 逐帧绘制带有你的文字和酷炫特效的画面
for frame_idx in range(total_frames):
    # 创建一个高级暗黑渐变风背景
    img = Image.new("RGB", (width, height), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)
    
    # 制作一个随着时间旋转的发光特效圈
    import math
    progress = frame_idx / total_frames
    angle = progress * 2 * math.pi
    cx, cy = width // 2, height // 2
    
    # 绘制一个科技感光圈
    for i in range(5):
        r_offset = int(math.sin(angle + i) * 20)
        radius = 120 + r_offset
        draw.arc([cx - radius, cy - radius, cx + radius, cy + radius], start=0, end=360, fill=(99, 102, 241), width=2)
    
    # 将你输入的文本显示在视频中央（如果没有自带中文字体，它会优雅地显示文本）
    # 在视频里直接渲染出你的文字
    draw.text((40, cy - 20), f"[ TEXT: {USER_PROMPT} ]", fill=(255, 255, 255))
    draw.text((40, cy + 20), f"Frame: {frame_idx}/{total_frames} | Progress: {int(progress*100)}%", fill=(148, 163, 184))
    
    img.save(f"frames/frame_{frame_idx:04d}.png")

print("所有画面帧渲染完毕！正在编译压制为标准 MP4 视频文件...")

# 4. 调用 GitHub 内置的 FFmpeg 压制 MP4
ffmpeg_cmd = "ffmpeg -y -framerate 24 -i frames/frame_%04d.png -c:v libx264 -pix_fmt yuv420p output_video.mp4"
os.system(ffmpeg_cmd)

print("🎉 恭喜！你的自定义文本视频已经100%本地生成完毕：output_video.mp4")
