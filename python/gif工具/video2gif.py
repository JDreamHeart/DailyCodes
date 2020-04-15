# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2020-03-05 17:10:47
# @Last Modified by:   JinZhang
# @Last Modified time: 2020-03-11 15:10:21

import cv2;
import imageio;

def video2gif(videoPath, gifPath, skipFps = 3):
    skipFps = max(skipFps + 1, 1);
    
    cap = cv2.VideoCapture(videoPath);
    tgtFps = cap.get(cv2.CAP_PROP_FPS) / skipFps;

    frames = [];
    i = 0;
    while(cap.isOpened()):
        ret, frame = cap.read();
        if not ret:
            break;
        if (i % skipFps == 0):
            frames.append(frame);
        i += 1;
    cap.release();
    cv2.destroyAllWindows();
    # 生成GIF
    if not gifPath.endswith(".gif"):
        gifPath += ".gif";
    imageio.mimsave(gifPath, frames, "GIF", fps= tgtFps); # 保存为GIF


def revideo(videoPath, tgtPath, skipFps = 3):
    skipFps = max(skipFps + 1, 1);
    
    cap = cv2.VideoCapture(videoPath);
    tgtFps = int(cap.get(cv2.CAP_PROP_FPS) / skipFps);

    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)));

    fourcc = cv2.VideoWriter_fourcc(*'DIV3'); # 编码格式

    video = cv2.VideoWriter(tgtPath, fourcc, tgtFps, size); 

    i = 0;
    while(cap.isOpened()):
        ret, frame = cap.read();
        if not ret:
            break;
        if (i % skipFps == 0):
            video.write(frame);
        i += 1;
    cap.release();
    video.release();
    cv2.destroyAllWindows();


if __name__ == "__main__":
    videoPath = "video/GameStage.mp4"; # 生成的gif文件名称
    tgtPath = "video/NewGameStage.mp4"; # 指定文件名称
    revideo(videoPath, tgtPath);     # 生成git文件