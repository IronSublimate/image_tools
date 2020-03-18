#
# Author : Hou Yuxuan
# 图片标注数据集的存储路径的描述
#
import json
from pathlib import Path

__json_path = Path(__file__).parent / "image_folder_tree.json"
__tree = json.load(__json_path.open("r"))


# print(tree)


def data_folder():  # 数据集的父目录
    return __tree["data_folder"]


def img_folder():
    return __tree["img_folder"]


def annotation_folder():
    return __tree["annotation_folder"]


def split_folder():
    return __tree["split_folder"]


def yolo_labels_folder():
    return __tree["yolo_labels_folder"]
