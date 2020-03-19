#!/usr/bin/env python3

# 将没有标记的数据生成空VOC标记格式
# 目录如下

import sys
from pathlib import Path
from PIL import Image
import image_folder_tree as folder

xml_template = r'''<annotation>
    <folder>{folder}</folder>
    <filename>{filename}</filename>
    <path>{path}</path>
    <source>
        <database>Unknown</database>
    </source>
    <size>
        <width>{width}</width>
        <height>{height}</height>
        <depth>{depth}</depth>
    </size>
    <segmented>0</segmented>
</annotation>
'''


def create_xml(image_path: Path):
    img = Image.open(image_path)
    width = img.size[0]
    height = img.size[1]
    return xml_template.format(
        folder=image_path.parents[0].name,
        filename=image_path.name,
        path=image_path.absolute(),
        width=width,
        height=height,
        depth=3
    )


def main(args: list):
    if len(args) > 1:
        data_folder = Path(args[1])
    else:
        data_folder = Path(folder.data_folder())
    label_folder_path = Path(__file__).parent.parent / data_folder / folder.annotation_folder()  # 标记的数据
    image_folder_path = Path(__file__).parent.parent / data_folder / folder.img_folder()  # 图片数据
    # print(label_folder_path.exists())
    annotation_set = set(f.stem for f in label_folder_path.glob("*.xml"))
    # print(annotation_set)
    for img_path in image_folder_path.rglob(r".*\.png|.*\.jpg|.*\.jpeg"):
        if img_path.stem not in annotation_set:
            xml = create_xml(img_path)
            # print(xml)
            filename = f'{img_path.stem}.xml'
            # print(filename)
            with (label_folder_path / filename).open('w',newline='\n') as f:
                f.write(xml)


if __name__ == "__main__":
    main(sys.argv)
