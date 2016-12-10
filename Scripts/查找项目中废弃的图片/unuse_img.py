#coding:utf-8

'''
python3 查找项目中无用的图片。
python 脚本路径 项目路径 过滤目录,过滤目录...
eg：
python unuse_img.py /Users/JyHu/Dropbox/Project/ios ThirdParts,Expression,GifFace
'''

import sys
import os
import re

# 读取xassets管理的图片
def assets_imgs(a_path):
    ass = os.listdir(a_path)
    as_imgs = []    # 记录assets中的图片
    for asset in ass:
        tmp_path = a_path + '/' + asset
        if asset[asset.rfind('.') + 1:] == 'imageset': as_imgs.append(tmp_path)
        elif asset[0:1] == '.': continue
        elif os.path.isdir(tmp_path): as_imgs += assets_imgs(tmp_path)
    return as_imgs

# 遍历图片还有文件
# c_path  字符串   当前要搜索的目录路径
# imgs    数组     找到的所有的图片
# codes   数组    找到的所有能够使用图片的文件，比如代码文件、plist文件等
# ecpt    元祖     需要跳过的目录名，这些将不被扫描
def file_classify(c_path, imgs, codes, ecpt_f):
    files = os.listdir(c_path)
    for file in files:
        tmp_path = c_path + '/' + file
        f_name = file[:file.rfind('.')]
        f_type = file[file.rfind('.') + 1:]
        if f_type in ('xcworkspace', 'xcodeproj', 'lproj', 'bundle', 'framework') or f_name in ('Podfile', 'Pods'):   # 这些文件、目录下的图片不做统计
            continue
        if f_type == 'xcassets':        # 是系统的Assets，只需要统计里面的图片即可。
            imgs += assets_imgs(tmp_path)
        elif os.path.isdir(tmp_path) and file not in ecpt_f:                 # 如果是一个目录，则递归去寻找
            file_classify(tmp_path, imgs, codes, ecpt_f)
        elif file[0:1] == '.':                      # 如果是隐藏文件，则不管他
            continue
        elif f_type in ('png', 'jpg', 'jpeg', 'bmp', 'gif'):    # 如果是图片类型的，则直接添加
            imgs.append(tmp_path)
        elif f_type in ('m', 'c', 'h', 'mm', 'strings', 'strings'):               # 代码文件也需要保存，去掉plist文件的读取
            codes.append(tmp_path)

# 检查图片在代码中是否存在
# img_path 图片地址
# code     代码文件
def img_exists_in_code(img_path, c_f):
    if os.path.isfile(c_f):
        img_full_name = img_path[img_path.rfind('/') + 1:]
        cut_matches = re.match('(.+?)(@\\w+)?\\.(\\w+)', img_full_name)
        if cut_matches != None and len(cut_matches.groups()) == 3:
            img_scale_type = cut_matches.group(2) if cut_matches.group(2) != None else ''
            try:
                with open(c_f, 'rb') as f:
                    cod = re.sub('(/\\*([.\\s\\S]*?)\\*/)|(//.*)', '', f.read().decode('utf-8'))
                    return re.search('"%s(%s)?(\\.%s)?"' % (cut_matches.group(1), cut_matches.group(2), cut_matches.group(3)), cod)
            except Exception as e:
                print(e, c_f)
    return False

# 程序的入口，检查图片是否被使用
# prj     项目地址
# ept_f   排除的文件夹
def imgCheck(prj, ept_f):
    if prj == None or len(prj) == 0 or not os.path.isdir(prj): return
    imgs = []
    codes = []
    file_classify(prj, imgs, codes, ept_f)
    unuse_imgs = []
    for t in range(len(imgs)):
        img = imgs[t]
        for i in range(len(codes)):
            code_file = codes[i]
            if img_exists_in_code(img, code_file): break
            if i == len(codes) - 1: unuse_imgs.append(img)
        sys.stdout.flush()
        sys.stdout.write('\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b')
        sys.stdout.write('--->> 正在处理 %d/%d' % (t + 1, len(imgs)))

    print('\n\n--------------------------\n\n以下图片未在项目中找到用处：\n\n')

    for im in unuse_imgs: print('未使用   : ', im)

    print('\n\n')
    print('以上内容检查自代码文件中，仅供参考，请自行在项目中查找资源是否使用')
    print('项目中图片共有:%d张' % len(imgs))
    print('没有用过的图片有:%d张' % len(unuse_imgs))


if __name__ == '__main__':
    args = sys.argv
    if len(args) >= 3:
        ecpt = args[2].split(',')
        imgCheck(args[1], ecpt)
    elif len(args) == 2:
        imgCheck(args[1], [])
