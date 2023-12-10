import os
from moviepy.editor import VideoFileClip

# 定义文件夹路径和尺寸信息
videos_folder = 'videos/'
output_folder_1920_vertical = '1920竖屏视频文件夹/'
output_folder_1080_horizontal = '1080横屏视频文件夹/'
output_folder_other = '其他尺寸视频文件夹/'

# 创建输出文件夹
os.makedirs(output_folder_1920_vertical, exist_ok=True)
os.makedirs(output_folder_1080_horizontal, exist_ok=True)
os.makedirs(output_folder_other, exist_ok=True)

# 寻找视频文件
video_files = [file for file in os.listdir(videos_folder) if file.lower().endswith('.mp4') or file.lower().endswith('.mov')]

# 分类处理视频文件
for video_file in video_files:
    video_path = os.path.join(videos_folder, video_file)
    clip = VideoFileClip(video_path)
    width, height = clip.size

    # 根据尺寸放入不同的文件夹
    if width == 1920 and height == 1080:
        output_path = os.path.join(output_folder_1920_vertical, video_file)
        os.rename(video_path, output_path)
    elif width == 1080 and height == 1920:
        output_path = os.path.join(output_folder_1080_horizontal, video_file)
        os.rename(video_path, output_path)
    else:
        output_path = os.path.join(output_folder_other, video_file)
        os.rename(video_path, output_path)

print("视频分类完成！")
