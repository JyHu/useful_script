# useful_script

个人写的一些自用的小脚本。
项目中的python脚本都是用的`Python3`环境，一般的Mac系统默认自带的都是`2.7`的，所以，如果发现运行不了的话，可以**[来这看看](http://www.auu.space/2016/10/13/升级Mac自带的python/)**升级一下`Python`版本。
# 注意

以下脚本如有在使用过程中出现任何问题，均与本人无关。

## [替换markdown文件中的图片到图床](https://github.com/JyHu/useful_script/tree/master/Scripts/md文件图片图床转换)

在写markdown文件的时候，如果有很多的图片引入，大家想到的多的应该是围脖图床等各种网上在线的插件或者网站，有的有限制，有的还比较麻烦，反正作为一个码农，感觉不能更人性化一点就是太不友好了。

所以在这用七牛做图床，python写脚本做了一个自动上传替换的脚本。

**[查看详细说明](https://github.com/JyHu/useful_script/tree/master/Scripts/md文件图片图床转换/note.md)**，现在就试用。。。

## [查找项目中废弃的图片](https://github.com/JyHu/useful_script/tree/master/Scripts/查找项目中废弃的图片)

主要是因为在开发的时候，有些图片放在XCode项目中，但是在版本迭代的时候，经常无法及时的删除无用的图片，所以，长时间的积累的话，肯定会造成项目的越来越臃肿。

脚本可以清理项目中的无用的图片，并将清理掉的内容写到缓存起来，以备查看。

测试了几个项目，效果还不错。

**[查看详细说明](https://github.com/JyHu/useful_script/blob/master/Scripts/查找项目中废弃的图片/Note.md)**

## [统计项目中代码的有效代码行数](https://github.com/JyHu/useful_script/tree/master/Scripts/统计项目中代码行数)

用来统计项目中有效代码的行数，即除掉注释、空行以外的代码，可以自己选择过滤的文件类型还有需要过滤掉的文件夹。

使用简单，**[详细请看这里>>>>](https://github.com/JyHu/useful_script/tree/master/Scripts/统计项目中代码行数/note.md)**

## [导出XCode中的Framework](https://github.com/JyHu/useful_script/tree/master/Scripts/XCode中Frameworks导出)

将XCode中的各个平台的SDK导出到目标目录，可以导出为markdown文件和头文件。

使用

python 脚本文件名 保存地址

例：
`python frameworkHeaders.py /Users/JyHu/Desktop/t`

***

当有新需求的时候会第一时间更新上来。。。
