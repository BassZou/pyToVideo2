"""prompt 帮我用python写一段批量剪辑视频的代码，
1. 批量识别videos文件下的所有mp4/MP4或者mov/MOV
2. 读取音频的文件夹music，该文件夹中的第一个文件就是该音乐，该文件可能是一个mp4/MP4格式或者是mov/MOV格式或者是mp3格式，不管什么格式都需要转成mp3音频
3. 将videos文件下的所有视频按照2秒剪切成若干短视频 并去掉音频（不要频繁创建文件，尽量在内存中完成），比如video.without_audio() 
4. 将这些尺寸相同的短视频随机打乱并重新组合在一起组成新的5个长视频，时长与mp3音频的时长一致
比如
    # 打乱顺序
    random.shuffle(video_clips)

5. 5个视频的音频需要全部都替换成music中的这个mp3 ，比如 video.set_audio(music)

# 最后将这替换好的5个长视频进行水平镜像翻转后保存到新的文件夹中，新的文件夹命名为日期，比如12月15日

# 请只用以下工具包完成代码，不要新增库
import os
import random
from moviepy.editor import VideoFileClip, concatenate_videoclips,AudioFileClip, CompositeVideoClip, vfx
from moviepy.audio.fx.volumex import volumex
from datetime import datetime
from tqdm import tqdm 

请把关键的变量拿出来，然后注释好中文，比如：做成多少个新视频，多少秒剪切
在运行过程中请在命令行中展示进度条
"""

import os
import random
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, vfx
from moviepy.audio.fx.volumex import volumex
from datetime import datetime
from tqdm import tqdm

# 生成的视频数量
NUM_VIDEOS = 5
# 视频剪切时长（秒）
CUT_DURATION = 2
# 旋转
my_angle = -0.1
# 对比度
my_contrast = -0.1
# 是否开启镜像
is_mirror = True

# 文件夹路径
videos_folder = '1080横屏视频文件夹/'  # 选择不同文件夹根据需求
music_folder = 'music/'
output_folder = datetime.now().strftime('%m月%d日')

# 创建输出文件夹
os.makedirs(output_folder, exist_ok=True)

"""寻找音频文件"""
def convert_to_mp3():
    music_files = [file for file in os.listdir(music_folder) if file.endswith('.mp4') or file.endswith('.MP4') or file.endswith('.mov') or file.endswith('.MOV') or file.endswith('.mp3')]
    if music_files:
        # 读取并转换音频文件为mp3格式
        music_file = music_files[0]
        music_path = os.path.join(music_folder, music_file)
        music = AudioFileClip(music_path)
        music_mp3_path = os.path.join(music_folder, 'converted_music.mp3')
        music.write_audiofile(music_mp3_path)
        return music, music_mp3_path
    else:
        print("音频文件夹中未找到音频文件")
        return None, None

"""读取视频并进行剪切和去音频"""
def process_videos(video_files, music, music_mp3_path):
    video_clips = []
    for video_file in tqdm(video_files, desc='处理视频-切分碎片'):
        video_path = os.path.join(videos_folder, video_file)
        clip = VideoFileClip(video_path)
        duration = int(clip.duration)
        cut_clips = [clip.subclip(i, i + CUT_DURATION).without_audio() for i in range(0, duration, CUT_DURATION)]
        video_clips.extend(cut_clips)

    n = len(video_clips)
    for i in tqdm(range(n - 1, 0, -1), desc='洗牌视频-随机组合'):
        j = random.randint(0, i)
        video_clips[i], video_clips[j] = video_clips[j], video_clips[i]

    videos = []
    for i in tqdm(range(NUM_VIDEOS), desc='生成视频-进行合并'):
        selected_clips = random.choices(video_clips, k=len(video_clips))
        selected_clips.sort(key=lambda x: video_clips.index(x))
        final_clip = concatenate_videoclips(selected_clips)
        final_clip = final_clip.set_audio(AudioFileClip(music_mp3_path))

        if final_clip.duration > music.duration:
            final_clip = final_clip.subclip(0, music.duration)

        videos.append(final_clip)

    return videos

"""调节视频"""
def apply_video_effects(videos):
    processed_videos = []
    for video in tqdm(videos, desc='调节视频-镜像滤镜旋转'):
        if is_mirror:
            video = video.fx(vfx.mirror_x)
        video = video.fx(vfx.rotate, angle=my_angle)
        video = video.fx(vfx.lum_contrast, contrast=my_contrast)
        processed_videos.append(video)

    return processed_videos

"""保存视频"""
def save_videos(processed_videos):
    for i, video in tqdm(enumerate(processed_videos), desc='保存视频-输出mp4'):
        output_path = os.path.join(output_folder, f'final_video_{i}.mp4')
        video.write_videofile(output_path, codec='libx264', fps=24, audio_codec='aac')

# 获取音频文件信息
music, music_mp3_path = convert_to_mp3()

# 如果有音频文件，则处理视频
if music:
    video_files = [file for file in os.listdir(videos_folder) if file.endswith('.mp4') or file.endswith('.MP4') or file.endswith('.mov') or file.endswith('.MOV')]
    videos = process_videos(video_files, music, music_mp3_path)
    processed_videos = apply_video_effects(videos)
    save_videos(processed_videos)




# 备份

# import os
# import random
# from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, vfx
# from moviepy.audio.fx.volumex import volumex
# from datetime import datetime
# # tqdm显示进度条用的
# from tqdm import tqdm


# # 生成的视频数量
# NUM_VIDEOS = 5
# # 视频剪切时长（秒）
# CUT_DURATION = 2
# # 旋转
# my_angle = -0.1
# # 对比度
# my_contrat = -0.1
# # 是否开启镜像
# is_mirror = True

# # 文件夹路径
# # videos_folder = '1920竖屏视频文件夹/'
# videos_folder = '1080横屏视频文件夹/'
# # videos_folder = 'videos/'
# music_folder = 'music/'
# output_folder = datetime.now().strftime('%m月%d日')

# # 创建输出文件夹
# os.makedirs(output_folder, exist_ok=True)

# # 寻找视频和音频文件
# video_files = [file for file in os.listdir(videos_folder) if file.endswith('.mp4') or file.endswith('.MP4') or file.endswith('.mov') or file.endswith('.MOV')]
# music_files = [file for file in os.listdir(music_folder) if file.endswith('.mp4') or file.endswith('.MP4') or file.endswith('.mov') or file.endswith('.MOV') or file.endswith('.mp3')]


# # 如果音频文件夹中存在音频文件，则处理视频
# if music_files:
#     # 读取并转换音频文件为mp3格式
#     music_file = music_files[0]
#     music_path = os.path.join(music_folder, music_file)
#     music = AudioFileClip(music_path)
#     music_mp3_path = os.path.join(music_folder, 'converted_music.mp3')
#     music.write_audiofile(music_mp3_path)

#     # 读取视频并进行剪切和去音频
#     video_clips = []
#     for video_file in tqdm(video_files, desc='处理视频-切分碎片'):
#         video_path = os.path.join(videos_folder, video_file)
#         clip = VideoFileClip(video_path)
#         duration = int(clip.duration)
#         cut_clips = [clip.subclip(i, i + CUT_DURATION).without_audio() for i in range(0, duration, CUT_DURATION)]
#         video_clips.extend(cut_clips)

#     # # 打乱视频顺序1
#     # random.shuffle(video_clips)
    
#     # # 打乱视频顺序2 - Fisher-Yates 算法打乱视频顺序
#     n = len(video_clips)
#     for i in tqdm(range(n - 1, 0, -1), desc='洗牌视频-随机组合'):
#         j = random.randint(0, i)
#         video_clips[i], video_clips[j] = video_clips[j], video_clips[i]


#     # 创建5个长视频
#     videos = []
#     for i in tqdm(range(NUM_VIDEOS), desc='生成视频-进行合并'):
#         selected_clips = random.choices(video_clips, k=len(video_clips))
#         selected_clips.sort(key=lambda x: video_clips.index(x))
#         final_clip = concatenate_videoclips(selected_clips)
#         final_clip = final_clip.set_audio(AudioFileClip(music_mp3_path))
        
#         # 裁剪多余部分
#         if final_clip.duration > music.duration:
#             final_clip = final_clip.subclip(0, music.duration) 
        
#         videos.append(final_clip)

#     # 保存水平镜像翻转后的视频到新文件夹
#     for i, video in tqdm(enumerate(videos), desc='保存视频-镜像滤镜旋转'):
#         """
#         视频调节 - 开始
#         """
#         # 镜像
#         if is_mirror:
#             video = video.fx(vfx.mirror_x)
#         # 旋转10度
#         video = video.fx(vfx.rotate, angle=my_angle) 
#         # 增加对比度10
#         video = video.fx(vfx.lum_contrast, contrast=my_contrat) 
#         """
#         视频调节 - 结束
#         """
#         # 路径
#         output_path = os.path.join(output_folder, f'final_video_{i}.mp4')
#         # 导出
#         video.write_videofile(output_path, codec='libx264', fps=24, audio_codec='aac')
# else:
#     print("音频文件夹中未找到音频文件")