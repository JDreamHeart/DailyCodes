# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2020-04-10 17:49:52
# @Last Modified by:   JinZhang
# @Last Modified time: 2020-04-10 18:26:33
import imageio;
import os;

'''
  根据文件夹路径生成gif文件【要求原始图片不包含透明度，否则会导致生成的gif显示异常】
  gifName： 字符串，所生成的 gif 文件名
  path:     需要合成为 gif 的图片所在路径
  fps:      帧率
'''
def createGif(gifName, path, fps = 12):
    frames = [];
    imgFiles = os.listdir(path);
    imageList = [os.path.join(path, f) for f in imgFiles];
    for image_name in imageList:
        frames.append(imageio.imread(image_name)); # 读取 png 图像文件
    if not gifName.endswith(".gif"):
        gifName += ".gif";
    imageio.mimsave(gifName, frames, "GIF", fps=fps); # 保存为GIF
    pass;


if __name__ == "__main__":
    gifName = "frame_anim1"; # 生成的gif文件名称
    imgsPath = "imgs";          # 指定文件路径
    createGif(gifName, imgsPath); # 生成git文件