#!/usr/bin/env python3

# 将VOC格式转成YOLO格式

import xml.etree.ElementTree as ET
import sys
import image_folder_tree as folder
from pathlib import Path

classes = ["white", "black"]


def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def convert_annotation(annotation_path: Path, yolo_label_path: Path):
    in_file = annotation_path.open()
    out_file = yolo_label_path.open('w')

    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


def main(args: list):
    if len(args) > 1:
        data_folder_str = args[1]
    else:
        data_folder_str = folder.data_folder()
    voc_label_path = Path(__file__).parent.parent / data_folder_str / folder.annotation_folder()  # VOC格式标记的数据
    image_path = Path(__file__).parent.parent / data_folder_str / folder.img_folder()  # 图片数据
    image_sets_path = Path(__file__).parent.parent / data_folder_str / folder.split_folder()  # 训练集测试集分类数据
    yolo_labels_path = Path(__file__).parent.parent / data_folder_str / folder.yolo_labels_folder()  # YOLO格式标记的数据

    if not yolo_labels_path.exists():
        yolo_labels_path.mkdir()
    for name in ('train', 'test'):
        image_ids = \
            set((image_sets_path / f'{name}.txt').open('r').read().strip().split())  # [0001 0002 ...]
        list_file = (Path(__file__).parent.parent / f'darknet_{name}.txt').open('wb')
        # 给darknet查找图片用的，保存在当前目录
        # print(image_path.exists())
        # print(image_path)
        for image in image_path.iterdir():
            # print(image)
            # 图片是后缀名且文件名在对应标签里
            if image.suffix in ('.png', '.jpeg', '.jpg', '.gif', '.bmp') and image.stem in image_ids:
                list_file.write(bytes(image.absolute()))
                list_file.write(bytes('\n', 'utf-8'))

            convert_annotation(voc_label_path / f'{image.stem}.xml', yolo_labels_path / f'{image.stem}.txt')
        list_file.close()


if __name__ == "__main__":
    main(sys.argv)
