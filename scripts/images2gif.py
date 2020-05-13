#!/usr/bin/env python3
import os

import imageio
import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple
import xml.etree.ElementTree as ET


def create_gif(image_paths: List[str], gif_name: str):
    frames = []
    # 模拟用鼠标框住物体
    image_name = image_paths[0]
    xml_path = image_name.replace("JPEGImages", "Annotations").replace("png", "xml")
    image = imageio.imread(image_name)
    with open(xml_path, "r") as xml_file:
        tree = ET.parse(xml_file)
    root = tree.getroot()
    for obj in root.iter('object'):
        xmlbox = obj.find('bndbox')
        pt1 = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text))
        pt2 = (int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
    w = pt2[0] - pt1[0]
    h = pt2[1] - pt1[1]
    MAX_STEP_IN_CREATE_BOX = 10  # 用鼠标框有多少帧
    for i in range(1, MAX_STEP_IN_CREATE_BOX):
        image_temp = image.copy()
        pt3 = (pt1[0] + int(w / MAX_STEP_IN_CREATE_BOX * i), pt1[1] + int(h / MAX_STEP_IN_CREATE_BOX * i))
        cv2.rectangle(image_temp, pt1, pt3, (255, 255, 0), 6)
        image_temp = cv2.resize(image_temp, (960, 540))
        frames.append(image_temp)
        # cv2.imshow("im_temp", image_temp)
        # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # return
    # image_paths = image_paths[1:]

    # 模拟跟踪
    for image_name in image_paths:
        xml_path = image_name.replace("JPEGImages", "Annotations").replace("png", "xml")
        image = imageio.imread(image_name)
        with open(xml_path, "r") as xml_file:
            tree = ET.parse(xml_file)
        root = tree.getroot()
        for obj in root.iter('object'):
            xmlbox = obj.find('bndbox')
            pt1 = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text))
            pt2 = (int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))

            cv2.rectangle(image, pt1, pt2, (255, 0, 0), 6)
        # cv2.imshow("iamge", image)
        # cv2.waitKey(0)
        image = cv2.resize(image, (960, 540))
        frames.append(image)
    # Save them as frames into a gif
    # imageio.mimsave(gif_name, frames, 'GIF', duration=0.2)
    for index, img in enumerate(frames):
        imageio.imsave(f"./output/{index}.png", img)
    os.system('ffmpeg -threads 2 -y -r 5 -i "./output/%d.png" -s 960x480 output2.gif')
    # for img in frames:
    #     img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    #     cv2.imshow("img", img)
    #     cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # return


# def rectangle(image: np.ndarray,
#               pt1: Tuple[int, int],
#               pt2: Tuple[int, int],
#               color: Tuple[int, int, int, int]):
#     pass


# def draw_bbox(imageRGB: np.ndarray, bbox: Tuple[int]) -> np.ndarray:
#     cv2.rectangle(imageRGB, )


if __name__ == "__main__":
    image_paths = []
    for i in range(0, 30):
        path = f"./in2_car/JPEGImages/{1541 + i:05d}.png"
        image_paths.append(path)
    create_gif(image_paths, "./output.gif")
