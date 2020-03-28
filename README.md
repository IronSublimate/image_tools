# 图片预处理工具集
> 作者： 侯宇轩

----

## 概述
1. 脚本均放在scripts中
2. 根目录为当前目录

## 图像文件目录结构
```
├─<data-folder1> 
│  ├─Annotations  
│  │  ├─1.xml
│  │  ├─2.xml
│  │  └─...
│  ├─Images  
│  │  ├─1.png 
│  │  ├─2.png
│  │  └─...
│  └─ImageSets  
│     └─Main
│       ├─train.txt
│       └─text.txt 
├─<data-folder2> 
├─...
└─scripts  
```
## 文件介绍

### image_folder_tree.json
图片，标注，训练集和测试集划分的保存路径

# 训练过程
## 准备数据
1. 标注
2. 使用generate_empty_annotations.py生成空标签
3. 使用split_train_text.py划分训练集测试集
4. 修改image_folder_tree.json更改对应的路径位置

## Darknet
1. 使用voc_lable.py生成对应的train、test
2. 修改cfg/voc.data
3. 修改data/voc.names
4. Create file `yolo-obj.cfg` with the same content as in `yolov3.cfg` (or copy `yolov3.cfg` to `yolo-obj.cfg)` and:

  * change line batch to [`batch=64`](https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L3)
  * change line subdivisions to [`subdivisions=16`](https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L4)
  * change line max_batches to (`classes*2000` but not less than `4000`), f.e. [`max_batches=6000`](https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L20) if you train for 3 classes
  * change line steps to 80% and 90% of max_batches, f.e. [`steps=4800,5400`](https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L22)
  * set network size `width=416 height=416` or any value multiple of 32: https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L8-L9
  * change line `classes=80` to your number of objects in each of 3 `[yolo]`-layers:
      * https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L610
      * https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L696
      * https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L783
  * change [`filters=255`] to filters=(classes + 5)x3 in the 3 `[convolutional]` before each `[yolo]` layer, keep in mind that it only has to be the last `[convolutional]` before each of the `[yolo]` layers.
      * https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L603
      * https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L689
      * https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L776
  * when using [`[Gaussian_yolo]`](https://github.com/AlexeyAB/darknet/blob/6e5bdf1282ad6b06ed0e962c3f5be67cf63d96dc/cfg/Gaussian_yolov3_BDD.cfg#L608)  layers, change [`filters=57`] filters=(classes + 9)x3 in the 3 `[convolutional]` before each `[Gaussian_yolo]` layer
      * https://github.com/AlexeyAB/darknet/blob/6e5bdf1282ad6b06ed0e962c3f5be67cf63d96dc/cfg/Gaussian_yolov3_BDD.cfg#L604
      * https://github.com/AlexeyAB/darknet/blob/6e5bdf1282ad6b06ed0e962c3f5be67cf63d96dc/cfg/Gaussian_yolov3_BDD.cfg#L696
      * https://github.com/AlexeyAB/darknet/blob/6e5bdf1282ad6b06ed0e962c3f5be67cf63d96dc/cfg/Gaussian_yolov3_BDD.cfg#L789
      
  So if `classes=1` then should be `filters=18`. If `classes=2` then write `filters=21`.
  
  **(Do not write in the cfg-file: filters=(classes + 5)x3)**
  
  (Generally `filters` depends on the `classes`, `coords` and number of `mask`s, i.e. filters=`(classes + coords + 1)*<number of mask>`, where `mask` is indices of anchors. If `mask` is absence, then filters=`(classes + coords + 1)*num`)

  So for example, for 2 objects, your file `yolo-obj.cfg` should differ from `yolov3.cfg` in such lines in each of **3** [yolo]-layers:

  ```
  [convolutional]
  filters=21

  [region]
  classes=2
  ```

## CenterNet
1. 使用voc2coco.py生成coco的json文件
2. 使用mean_std.py计算均值和标准差，
3. src/lib/datasets/dataset写一个数据类  
> （1）第14行的类名改为自己的类型名，这里定义为Food；  
> （2）第15行的num_class改为自己数据集的类别数；  
> （3）第16行的default_resolution为默认的分辨率，这里按原作者给出的[512, 512]，如果觉得自己的硬件设备跟不上，可以适当的改小，注意上面所计算出来的整个数据集的均值和标准差也要同步；  
> （4）第17-20行的均值和方差填上去；  
> （5）第23行super类的继承改为你自己定义的类名称；  
> （6）修改读取json文件的路径；  
> （7）修改类别名字和id；  
> （8）self._valid_ids


