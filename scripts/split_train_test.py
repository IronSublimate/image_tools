#!/usr/bin/env python3

# 将标记好的数据生成train.txt和test.txt
# 目录如下
#
# |-split_train_test.py
# |-VOC2007
#   |- Annotation (data)
#   |  |-1.xml
#   |  |-2.xml
#   |  |-...
#   |
#   |-ImageSets
#      |-Main
#         |-train.txt (will be created)
#         |-text.txt (will be created)
#
# usage:
# split_train_test.py <test_size=0.2>
#   test_size must be float which is <=1 and >=0

import sys
from pathlib import Path
import random
import image_folder_tree as folder


def split(full_list, shuffle=False, ratio=0.2):
    n_total = len(full_list)
    offset = int(n_total * ratio)
    if n_total == 0 or offset < 1:
        return [], full_list
    if shuffle:
        random.shuffle(full_list)
    sublist_1 = full_list[:offset]
    sublist_2 = full_list[offset:]
    return sublist_2, sublist_1


def main(args: list):
    if len(args) > 1:
        ratio = float(args[1])
    else:
        ratio = 0.2
    if len(args) > 2:
        data_folder = Path(args[2])
    else:
        data_folder = Path(folder.data_folder())
    label_path = Path(__file__).parent.parent / data_folder / folder.annotation_folder()  # 标记的数据
    name_path = Path(__file__).parent.parent / data_folder / folder.split_folder()  # 用于训练和测试样本的名字文件的路径
    list_path = list(f'{f.stem}\n' for f in label_path.glob("*.xml"))
    train_list, test_list = split(list_path, True, ratio)
    print(train_list)
    print(test_list)
    for name in ('train', 'test'):
        pth = name_path / f"{name}.txt"
        with pth.open('w', newline='\n') as f:
            f.writelines(eval(f"{name}_list"))


if __name__ == "__main__":
    random.seed(110)
    main(sys.argv)
