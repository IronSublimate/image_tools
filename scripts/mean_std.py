import cv2
import os
import sys
import numpy as np
from pathlib import Path
import image_folder_tree as folder


def compute(image_folder: str):
    # dirs = r'F:\Pycharm Professonal\CenterNet\CenterNet\data\food\images'  # 修改你自己的图片路径
    # img_file_names = os.listdir(image_folder)
    m_list, s_list = [], []
    for img_filename in Path(image_folder).iterdir():
        # print(img_filename)
        img = cv2.imread(str(img_filename))
        img = img / 255.0
        m, s = cv2.meanStdDev(img)
        m_list.append(m.reshape((3,)))
        s_list.append(s.reshape((3,)))
    m_array = np.array(m_list)
    s_array = np.array(s_list)
    m = m_array.mean(axis=0, keepdims=True)
    s = s_array.mean(axis=0, keepdims=True)
    # print("mean = ", m[0][::-1])
    # print("std = ", s[0][::-1])
    return m[0][::-1], s[0][::-1]


def main(args: list):
    if len(args) > 1:
        data_folder_str = args[1]
    else:
        data_folder_str = folder.data_folder()
    image_path = Path(__file__).parent.parent / data_folder_str / folder.img_folder()  # 图片数据
    mean, standard = compute(image_path)
    print("mean", mean)
    print("std", standard)


if __name__ == "__main__":
    main(sys.argv)
