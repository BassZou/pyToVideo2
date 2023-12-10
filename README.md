将所有视频打碎重组成新的20个视频




# prompt
# 帮我用python写一段批量剪辑视频的代码，
# 1. 批量识别videos文件下的所有mp4/MP4或者mov/MOV
# 2. 读取音频的文件夹music，该文件夹中的第一个文件就是该音乐，该文件可能是一个mp4/MP4格式或者是mov/MOV格式或者是mp3格式，不管什么格式都需要转成mp3音频
# 3. 将videos文件下的所有视频按照2秒剪切成若干短视频 并去掉音频（不要频繁创建文件，尽量在内存中完成），比如video.without_audio() 
# 4. 将这些尺寸相同的短视频随机打乱并重新组合在一起组成新的5个长视频，时长与mp3音频的时长一致
# 比如
#     # 打乱顺序
#     random.shuffle(video_clips)

# 5. 5个视频的音频需要全部都替换成music中的这个mp3 ，比如 video.set_audio(music)

# # 最后将这替换好的5个长视频进行水平镜像翻转后保存到新的文件夹中，新的文件夹命名为日期，比如12月15日

# # 请只用以下工具包完成代码，不要新增库
# import os
# import random
# from moviepy.editor import VideoFileClip, concatenate_videoclips,AudioFileClip, CompositeVideoClip, vfx
# from moviepy.audio.fx.volumex import volumex
# from datetime import datetime

# 请把关键的变量拿出来，然后注释好中文，比如：做成多少个新视频，多少秒剪切
# 在运行过程中请在命令行中展示进度条