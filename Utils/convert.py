# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: MIDEP
# @FileName: Utils/convert
# @Author：Ryan Zhang    (https://github.com/hz157)
# @DateTime: 11/1/2023 上午1:19

from datetime import datetime

import cv2
import os

from Utils.logutils import LogUtils

logutils = LogUtils()


def v2i(path):
    try:
        cap = cv2.VideoCapture(os.path.join(path, "video.mp4"))
        # video fps
        fps = cap.get(cv2.CAP_PROP_FPS)
        # video frames
        frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        index = 0
        images = []
        while cv2.waitKey(0):
            retval, image = cap.read()
            index += 1
            # print(f"fps:{index}")
            if index == int(frames) or index == 1:
                prefix = str(index).zfill(8) + ".png"
                cv2.imwrite(os.path.join(path, prefix), image)
                images.append(index)
            elif index < int(frames):
                if index % int(fps) == 0:
                    prefix = str(index).zfill(8) + ".png"
                    cv2.imwrite(os.path.join(path, prefix), image)
                    images.append(index)
            elif index > frames:
                break
        return images
    except Exception as e:
        logutils.error(e)
    return None


def CNConvertInt(data: str):
    try:
        data = data.replace("次播放", "")
        unit = ["万", "亿"]
        default_dic = {"万": 10000, "亿": 100000000}
        current = {}
        if data[-1] in unit:
            current = default_dic[data[-1]]
        else:
            return int(data)
        data = data[0:-1]
        point = data.split(".")
        point[1] = "0." + point[1]
        for i in range(0, len(point)):
            point[i] = float(point[i])
            point[i] = point[i] * current
        result = point[0] + point[1]
        return int(result)
    except Exception as e:
        logutils.error(e)
    return None


def UTCConvertFormat(date):
    try:
        cat = datetime.strptime(date, "%a %b %d %H:%M:%S %z %Y")
        return cat.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        logutils.error(e)
    return None


def fileSizeConvert(size: int):
    result = ''
    try:
        if size < 1024:
            result = str(size) + "B"
        elif size > 1024:
            result = str(size / float(1024)) + "KB"
        elif size > 10240:
            result = str(size / float(1024) / float(1024)) + "MB"
        elif size > 102400:
            result = str(size / float(1024) / float(1024) / float(1024)) + "GB"
        return result
    except Exception as e:
        logutils.error(e)
    return None
