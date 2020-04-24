#!/usr/bin/env python3

# 需要生成train.txt,test.txt,val.txt,data/coco.names,cfg/coco.data文件

from argparse import ArgumentParser, Namespace
import json
from pathlib import Path
from pycocotools.coco import COCO
import sys

DATASET_TYPES = ("train", "val", "test")

cat_map = dict()


def parse() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--year", default="2017",
                        help="使用哪一年的数据集")
    parser.add_argument("--name", default="coco", type=Path, help="name of folder")
    parser.add_argument("--src", default=".", type=Path, help="path to coco dir")
    parser.add_argument("--dst", default="../coco2017", type=Path, help="where to save")

    opts = parser.parse_args()

    print(opts)
    return opts


# 产生图片的链接，把coco的train2017链接到JPEGImages下
def gen_symbol_link(img_path: Path, save_dir: Path):
    link_path = save_dir / "JPEGImages"
    print(link_path)
    print(img_path)
    link_path = link_path.resolve()
    # if not link_path.exists():
    try:
        link_path.symlink_to(img_path.resolve(), True)
    except Exception as e:
        sys.stderr.write("cannot create symlink to coco images\n")
        e.with_traceback(None)
    # link_path.touch()


# 将coco的id映射为连续值，生成字典
def gen_cat_map(coco: COCO):
    global cat_map
    for index, cat_id in enumerate(coco.cats):
        cat_map[cat_id] = index


# 将coco的id映射为连续值
def get_map_id(coco: COCO, cat_id):
    global cat_map
    if len(cat_map) == 0:
        gen_cat_map(coco)
    return cat_map[cat_id]


# 生成图像路径数据，返回生成的txt的路径
def gen_img_path_txt(dataset_type: str, year: str, coco: COCO, img_dir: Path, save_dir: Path) -> Path:
    # img_path = img_dir / (dataset_type + year)
    img_path = save_dir / "JPEGImages"
    txt_path = save_dir / f"coco{year}_{dataset_type}.txt"  # e.g.coco2017_val.txt
    with txt_path.open("w", newline='\n') as f:
        for id in coco.imgs:
            img = coco.loadImgs(id)[0]
            img_path_str = (img_path / img["file_name"]).absolute().as_posix()
            f.write(img_path_str)
            f.write('\n')
    return txt_path


# 生成标注数据，返回生成的txt的路径，保存中labels里
def gen_ann_txts(coco: COCO, save_dir: Path) -> Path:
    save_dir_label = save_dir / "labels"
    if not save_dir_label.exists():
        save_dir_label.mkdir()
    for img_id in coco.imgs:
        img = coco.loadImgs(img_id)[0]
        txt_name = img["file_name"].split(".")[0] + ".txt"
        img_h = img["height"]
        img_w = img["width"]
        with (save_dir_label / txt_name).open("w", newline='\n') as f:
            for ann in coco.imgToAnns[img_id]:
                # ann = coco.loadAnns(ann_id)[0]
                x, y, w, h = ann["bbox"]
                x += w / 2
                y += h / 2
                x /= img_w
                y /= img_h
                w /= img_w
                h /= img_h
                # yolo格式是中心点坐标，w,h，并归一化
                cat_id = get_map_id(coco, ann['category_id'])  # 下标从0开始
                f.write(f"{cat_id} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")
    return save_dir_label


# 生成data/coco.names，保存在data里
def gen_names(year: str, coco: COCO, save_dir: Path) -> Path:
    save_dir_data = save_dir / "data"
    if not save_dir_data.exists():
        save_dir_data.mkdir()
    save_name = save_dir_data / f"coco{year}.names"
    cats = coco.cats
    with save_name.open("w", newline='\n') as f:
        for cat_id in cats:
            cat_name = cats[cat_id]["name"]
            f.write(cat_name + "\n")
    return save_name


# 生成cfg/coco.data
def gen_data(year: str, coco: COCO, train_txt: Path, valid_txt: Path, names: Path, save_dir: Path,
             backup: str = "backup"):
    cfg_dir = save_dir / "cfg"
    if not cfg_dir.exists():
        cfg_dir.mkdir()
    classes = len(coco.cats)
    cfg_file = cfg_dir / f"coco{year}.data"
    with cfg_file.open("w", newline='\n') as f:
        f.write(f"classes={classes}\n")
        f.write(f"train={train_txt.as_posix()}\n")
        f.write(f"valid={valid_txt.as_posix()}\n")
        f.write(f"names={names.as_posix()}\n")
        f.write(f"backup={backup}")


def main():
    opts = parse()
    # opts.src = Path('G:/dataset/coco')
    ann_dir = opts.src / "annotations"
    img_dir = opts.src / "images"
    if not opts.dst.exists():
        opts.dst.mkdir()
    gen_symbol_link(img_dir / ("train" + opts.year), opts.dst.resolve())
    coco_dict = {}  # 保存train，test的coco
    img_path_dict = {}  # 保存train，test的图片路径文件的路径
    for data_type in ("train", "test"):
        if data_type == "test":
            if opts.year == "2014":
                ann_file = ann_dir / "image_info_test2014.json"
            elif opts.year == "2017":
                ann_file = ann_dir / "image_info_test-dev2017.json"
            else:
                nn_file = ann_dir / f"image_info_test{opts.year}.json"
        else:
            ann_file = ann_dir / f"instances_{data_type}{opts.year}.json"
        coco = COCO(ann_file)
        coco_dict[data_type] = coco

        ann_txt_path = gen_ann_txts(coco, opts.dst)
        img_txt_path = gen_img_path_txt(data_type, opts.year, coco, img_dir, opts.dst)
        print(data_type, " labels path   : ", ann_txt_path)
        print(data_type, " imgs txt path : ", img_txt_path)
        img_path_dict[data_type] = img_txt_path

    names_path = gen_names(opts.year, coco, opts.dst)
    gen_data(opts.year, coco, img_path_dict["train"].resolve(), img_path_dict["test"].resolve(),
             names_path.resolve(), opts.dst)
    sys.exit(0)


if __name__ == '__main__':
    main()
    # opts = parse()
    # ann_dir = opts.src / "annotations"
    # img_dir = opts.src / "images"
    # ann_file = ann_dir / f"instances_val{opts.year}.json"
    # coco = COCO(ann_file)
    # gen_img_path_txt("val", opts.year, coco, img_dir, opts.dst)
    # gen_ann_txts(coco, opts.dst)
    # gen_names(opts.year, coco, opts.dst)
    # if not opts.dst.exists():
    #     opts.dst.mkdir()
    #
