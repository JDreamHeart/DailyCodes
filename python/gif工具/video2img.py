# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2020-03-05 17:10:47
# @Last Modified by:   JinZhang
# @Last Modified time: 2020-03-11 15:10:21

import os;
import cv2;
import imageio;

def video2img(videoPath, imgDir, name, skipFps=10):
    skipFps = max(skipFps + 1, 1);
    
    cap = cv2.VideoCapture(videoPath);

    if not os.path.exists(imgDir):
        os.makedirs(imgDir);
    imgPath = os.path.join(imgDir, name+"_{}.png");

    i, idx = 0, 0;
    while(cap.isOpened()):
        ret, frame = cap.read();
        if not ret:
            break;
        if (i % skipFps == 0):
            imageio.imwrite(imgPath.format(idx), frame);
            idx += 1;
        i += 1;
    cap.release();
    cv2.destroyAllWindows();


if __name__ == "__main__":
    videoPath = "video/bg_anim.mp4";
    tgtPath = "images/studio_bg_anim";
    video2img(videoPath, tgtPath, "studio_bg_anim", 5);