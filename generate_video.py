import os
import math

print("正在初始化本地视频渲染引擎...")

# 确保安装了图片处理库
os.system("pip install pillow")
from PIL import Image, ImageDraw

# 视频参数
width, height = 640, 360
fps = 24
duration_sec = 3
total_frames = fps * duration_sec

print(f"正在生成基础画面帧，总计 {total_frames} 帧...")

# 创建一个临时文件夹存放图片帧
os.makedirs("frames", exist_ok=True)

# 循环绘制每一帧（做一个炫酷的色彩渐变和文字动画效果）
for frame_idx in range(total_frames):
    # 创建画布
    img = Image.new("RGB", (width, height), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    
    # 计算动态波浪效果
    progress = frame_idx / total_frames
    angle = progress * 2 * math.pi
    
    # 画一个动态的彩色发光球体
    cx = int(width / 2 + math.sin(angle) * 100)
    cy = int(height / 2 + math.cos(angle) * 50)
    radius = 40 + int(math.sin(angle * 2) * 15)
    
    # 渐变颜色
    r = int(127 + 127 * math.sin(angle))
    g = int(127 + 127 * math.cos(angle))
    b = 255
    
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=(r, g, b))
    
    # 保存单帧图片
    img.save(f"frames/frame_{frame_idx:04d}.png")

print("所有画面帧生成完毕！正在调用系统 FFmpeg 合成视频...")

# 使用 GitHub 服务器自带的 FFmpeg 工具将图片序列合成为 MP4 视频
ffmpeg_cmd = "ffmpeg -y -framerate 24 -i frames/frame_%04d.png -c:v libx264 -pix_fmt yuv420p output_video.mp4"
exit_code = os.system(ffmpeg_cmd)

if exit_code == 0:
    print("🎉 视频完美生成！成功保存为 output_video.mp4")
else:
    print("FFmpeg 合成失败，请检查系统环境。")
