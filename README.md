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



