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

def assets_imgs(a_path):
    ass = os.listdir(a_path)
    as_imgs = []
    for asset in ass:
        tmp_path = a_path + '/' + asset
        if asset[asset.rfind('.') + 1:] == 'imageset': as_imgs.append(tmp_path)
        elif asset[0:1] == '.': continue
        elif os.path.isdir(tmp_path): as_imgs += assets_imgs(tmp_path)
    return as_imgs

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
        elif f_type in ('m', 'c', 'h', 'mm', 'plist', 'strings', 'strings'):               # 代码文件也需要保存
            codes.append(tmp_path)

def img_exists_in_code(img_path, cod):
    img_full_name = img_path[img_path.rfind('/') + 1:]
    cut_matches = re.match('(.+?)(@\\w+)?\\.(\\w+)', img_full_name)
    if cut_matches != None and len(cut_matches.groups()) == 3:
        img_scale_type = cut_matches.group(2) if cut_matches.group(2) != None else ''
        return re.search('"%s(%s)?(\\.%s)?"' % (cut_matches.group(1), cut_matches.group(2), cut_matches.group(3)), cod)
    return False

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
            try:
                with open(code_file, 'rb') as f:
                    if img_exists_in_code(img, f.read().decode('utf-8')):
                        break
            except Exception as e: print(e, code_file)
            if i == len(codes) - 1: unuse_imgs.append(img)
        sys.stdout.flush()
        sys.stdout.write('\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b')
        sys.stdout.write('--->> 正在处理 %d/%d' % (t + 1, len(imgs)))

    print('\n\n--------------------------\n\n以下%d张图片未在项目中找到用处：\n\n' % len(unuse_imgs))

    for im in unuse_imgs: print('unuse : ', im)

    print('\n\n以上内容仅供参考，请自行在项目中查找资源是否使用')

if __name__ == '__main__':
    args = sys.argv
    if len(args) >= 3:
        ecpt = args[2].split(',')
        imgCheck(args[1], ecpt)
    elif len(args) == 2:
        imgCheck(args[1], [])
