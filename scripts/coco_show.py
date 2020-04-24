from pathlib import Path

from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
from typing import Tuple
from argparse import ArgumentParser, Namespace
import os
import json
import time
import matplotlib.pyplot as plt
from imageio import imread


def parse() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--coco_json", help="where is coco test json")
    parser.add_argument("--coco_image", help="where is image folder")
    parser.add_argument("--results", help="where is detection result json file")

    opts = parser.parse_args()
    assert os.path.exists(opts.coco_json), "coco_json is not exist"
    assert os.path.exists(opts.coco_image), "coco_image is not exist"
    assert os.path.exists(opts.results), "results json is not exist"

    return opts


def show_result(coco: COCO, img_dir: str, results_dir: str):
    coco_dt = coco.loadRes(results_dir)
    for img_id in coco_dt.imgs:
        img_path = os.path.join(img_dir, coco_dt.imgs[img_id]["file_name"])
        ann_ids = coco_dt.getAnnIds(img_id)
        img = imread(img_path)
        plt.imshow(img)
        plt.axis("off")
        anns = coco_dt.loadAnns(ann_ids)
        coco_dt.showAnns(anns, True)
        plt.show()


if __name__ == "__main__":
    args = parse()
    coco_gt = COCO(args.coco_json)
    show_result(coco_gt, args.coco_image, args.results)
