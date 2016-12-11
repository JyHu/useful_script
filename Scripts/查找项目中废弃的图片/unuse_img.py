#coding:utf-8
#auth:JyHu

'''
python3 查找项目中无用的图片。
python 脚本路径 项目路径 过滤目录,过滤目录...
eg：
python unuse_img.py /Users/JyHu/Dropbox/Project/ios ThirdParts,Expression,GifFace
'''

import sys
import os
import re
import shutil
import getpass
import imghdr

xcodeproj = ''
tempStorePath = ''

# 读取xassets管理的图片
def assets_imgs(a_path):
    ass = os.listdir(a_path)
    as_imgs = []    # 记录assets中的图片
    for asset in ass:
        tmp_path = a_path + '/' + asset         # 当前图片文档的地址
        if asset[asset.rfind('.') + 1:] == 'imageset': as_imgs.append(tmp_path) # 如果是imageset直接添加
        elif asset[0:1] == '.': continue                                        # 过滤掉隐藏目录
        elif os.path.isdir(tmp_path): as_imgs += assets_imgs(tmp_path)          # 递归添加
    return as_imgs

# 遍历图片还有文件
# c_path  字符串   当前要搜索的目录路径
# imgs    数组     找到的所有的图片
# codes   数组    找到的所有能够使用图片的文件，比如代码文件、plist文件等
# ecpt    元祖     需要跳过的目录名，这些将不被扫描
def file_classify(c_path, imgs, codes, ecpt_f):
    files = os.listdir(c_path)
    for file in files:
        if file[0:1] == '.': continue                         # 如果是隐藏文件，则不管他
        tmp_path = c_path + '/' + file      # 当前要判断的文件的地址
        f_loc = file.rfind('.')             # 在文件名中是否有 `.` ，用于截取
        f_name = file[:(f_loc if f_loc != -1 else len(file))]           # 文件名
        f_type = file[((f_loc + 1) if f_loc != -1 else len(file)):]     # 文件类型
        if f_type in ('lproj', 'bundle', 'framework', 'xcworkspace', '.a') or f_name in ('Podfile', 'Pods', '__temp_store_path') or file in ecpt_f:   # 这些文件、目录下的图片不做统计
            continue
        if f_type == 'xcodeproj':
            global xcodeproj
            xcodeproj = tmp_path
        elif f_type == 'xcassets':        # 是系统的Assets，只需要统计里面的图片即可。
            imgs += assets_imgs(tmp_path)
        elif os.path.isdir(tmp_path):                 # 如果是一个目录，则递归去寻找
            file_classify(tmp_path, imgs, codes, ecpt_f)
        elif f_type in ('m', 'c', 'h', 'mm', 'strings', 'strings'):               # 代码文件也需要保存，去掉plist文件的读取
            codes.append(tmp_path)
        elif imghdr.what(tmp_path):    # 如果是图片类型的，则直接添加
            imgs.append(tmp_path)


# 检查图片在代码中是否存在
# img_path 图片地址
# code     代码文件
def img_exists_in_code(img_path, c_f):
    if os.path.isfile(c_f):     # 如果当前文件存在才能继续执行
        img_full_name = img_path[img_path.rfind('/') + 1:]  # 图片包含类型的名称
        cut_matches = re.match('(.+?)(@\\w+)?\\.(\\w+)', img_full_name)     # 使用正则截取每一部分
        if cut_matches != None and len(cut_matches.groups()) == 3:
            img_scale_type = cut_matches.group(2) if cut_matches.group(2) != None else ''
            try:
                with open(c_f, 'rb') as f:
                    cod = re.sub('(/\\*([.\\s\\S]*?)\\*/)|(//.*)', '', f.read().decode('utf-8'))    # 清除所有注释
                    return re.search('"%s(%s)?(\\.%s)?"' % (cut_matches.group(1), cut_matches.group(2), cut_matches.group(3)), cod)     # 组装正则用来查找判断
            except Exception as e: print(e, c_f)
    return False

# 根据选择一张一张的删除图片
# 图片地址
def remove_img(img):
    if img[img.rfind('.') + 1:] == 'imageset': store_file(img)
    elif len(xcodeproj) > 0 and os.path.isfile(img):
        pth = xcodeproj + '/' + 'project.pbxproj'   # 工程文件
        with open(pth, 'r') as f:
            i_name = img[img.rfind('/') + 1:]   # 图片名字
            store_file(img)
            replfile(pth, [line for line in f.readlines() if line.find(i_name) == -1])  # 删除所有带有图片名字的行

# 替换工程文件，不然会在项目中爆红。
# 工程文件`project.pbxproj`地址
# lines 工程文件的内容
def replfile(fpth, lines):
    pth = fpth[:fpth.rfind('/')]
    temp = pth + '/' +'___tmp_file'  # 创建一个临时文件，保存修改后的工程文件
    with open(temp, 'a') as f:
        for line in lines: f.write(line)
    os.remove(fpth)             # 删除原来的工程文件
    shutil.move(temp, fpth)     # 使用新的工程文件替换原有的

'''
移除的无用图片，不删除，只是移动到一个缓存目录，并记录在日志文件
img 要移动的图片
'''
def store_file(img):
    try: shutil.move(img, tempStorePath)
    except Exception as e: os.system('rm %s' % img)     #如果文件已经存在了，则删除他
    with open(tempStorePath + '/' + '__store_log.txt', 'a') as f:   # 记录文件日志
            f.write(img)
            f.write('\n')
    print('移除无用图片成功  %s' % img)
'''
自动批量移除所有无用图片
imgs 要移除的图片数组
'''
def remove_imgs(imgs):
    if len(xcodeproj) > 0 and len(imgs) > 0:
        with open(xcodeproj + '/' + 'project.pbxproj', 'r') as f:
            lines = f.readlines()
            c_unuse_img = False
            for img in imgs:
                store_file(img)     # 缓存图片
                if img[img.rfind('.') + 1:] == 'imageset': continue     # 'imageset' 只需要删除本地文件即可，不需要清理工程文件
                lines = [line for line in lines if line.find(img[img.rfind('/') + 1:]) == -1]
            replfile(xcodeproj + '/' + 'project.pbxproj', lines)

# 程序的入口，检查图片是否被使用
# prj     项目地址
# ept_f   排除的文件夹
def imgCheck(prj, ept_f):
    if prj == None or len(prj) == 0 or not os.path.isdir(prj): return

# ------------------------ 初始化一些参数

    global tempStorePath
    tempStorePath = prj + '/' + '__temp_store_path'
    if not os.path.isdir(tempStorePath): os.mkdir(tempStorePath)

# ------------------------ 过滤归类文件

    imgs = []
    codes = []
    file_classify(prj, imgs, codes, ept_f)

# ------------------------ 筛选无用图片

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

# ------------------------ 处理无用图片及相关联内容

    if len(unuse_imgs) == 0:
        print('\n\n恭喜你，项目中没有无用的图片哦 ~ \n')
        return

    print('\n\n--------------------------\n\n以下图片未在项目中找到用处：\n\n')

    for im in unuse_imgs: print('未使用   : ', im)

    if len(unuse_imgs) > 0:
        print('\n\n')
        print('>>--------------------------------------------------------------')
        print('>|')
        print('>|    以上内容检查自代码文件中，仅供参考，请自行在项目中查找资源是否使用')
        print('>|    项目中图片共有:%d张' % len(imgs))
        print('>|    没有用过的图片有:%d张' % len(unuse_imgs))
        print('>|')
        print('>|')
        print('>|    请选择操作方式：')
        print('>|')
        print('>|    888 - 全部清除')
        print('>|    2   - 依次全部清除')
        print('>|    其他 - 退出')
        print('>|')
        print('>>--------------------------------------------------------------')
        print('\n')

        cmd = input('>> : ')
        if cmd == '888': remove_imgs(unuse_imgs)
        elif cmd == '2':
            for cur_img in unuse_imgs:
                print('\n-------------------------------------------------------\n\n当前项：', cur_img)
                cmd = input('-- > (y/Y删除)  : ')
                if cmd == 'q': break
                elif cmd == 'y' or cmd == 'Y': remove_img(cur_img)

        if len(os.listdir(tempStorePath)) > 0:
            try:
                dpath = '/Users/%s/Desktop/UnuseImgCheck' % getpass.getuser()
                rep = 1
                mv_path = dpath
                while os.path.isdir(mv_path):
                    mv_path = dpath + str(rep)
                    rep += 1
                os.mkdir(mv_path)
                shutil.move(tempStorePath, mv_path)
                os.system('open %s' % mv_path)
                print('\n移动缓存文件夹成功')
            except Exception as e: print('移动失败 ', e)
        else: print('\n\n操作结束 ~ \n')

if __name__ == '__main__':
    args = sys.argv
    if len(args) >= 3:
        ecpt = args[2].split(',')
        imgCheck(args[1], ecpt)
    elif len(args) == 2:
        imgCheck(args[1], [])
