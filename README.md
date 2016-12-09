# useful_script

个人写的一些自用的小脚本，如果有需要，请拿走。

## 查找项目中废弃的图片

主要是因为在开发的时候，有些图片放在XCode项目中，但是在版本迭代的时候，经常无法及时的删除无用的图片，所以，长时间的积累的话，肯定会造成项目的越来越臃肿。

### 使用
python 脚本路径 项目路径 [过滤目录,过滤目录...]
例：
`python unuse_img.py /Users/JyHu/Dropbox/Project/ios ThirdParts,Expression,GifFace`

***

## 导出XCode中的Framework

将XCode中的各个平台的SDK导出到目标目录，可以导出为markdown文件和头文件。

### 使用
python 脚本文件名 保存地址
例：
`python frameworkHeaders.py /Users/JyHu/Desktop/t`

***

当有新需求的时候会第一时间更新上来。。。