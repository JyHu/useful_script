#coding:utf-8
#auth:JyHu

import sys
import os
import re
import imghdr

origin_type = ('bundle', 'framework', 'xcworkspace', 'xcodeproj', 'a', 'plist', 'xcassets', 'storyboard', 'xib', 'nib', 'entitlements', 'ttf', 'json', 'swf', 'avi', 'mp4', 'mov')
origin_folder = ('Podfile', 'Pods')
file_count_key = '文件数(表示的仅是统计的文件的个数)'

'''
递归的去统计所有的代码文件

prj   工程目录
res   统计结果
et    忽略掉的类型
ef    忽略的目录
'''
def classify_count(prj, res, et, ef):
    if os.path.isdir(prj):      # 检查项目地址是否存在
        files = os.listdir(prj)
        for file in files:
            if file.find('.') == 0: continue    # 过滤隐藏文件
            loc = file.rfind('.')               # 用来分割文件类型
            fname = file[:(loc if loc != -1 else len(file))]        # 文件名
            ftype = file[(loc + 1 if loc != -1 else len(file)):]    # 文件类型
            curp = prj + '/' + file                                 # 当前文件的完整路径
            if fname in origin_folder or ftype in origin_type or ftype in et or fname in ef: continue   # 过滤一些不需要的东西
            if os.path.isdir(curp): classify_count(curp, res, et, ef)       # 如果是目录的话，就递归的去统计
            elif imghdr.what(curp): continue        # 如果是图片则过滤掉，继续统计
            else:
                try:
                    with open(curp, 'r') as f:
                        words = re.sub('\\s+(/\\*([.\\s\\S]*?)\\*/)|(//.*)', '', f.read())          # 使用正则替换掉代码中所有的注释行
                        codelines = [line for line in words.split('\n') if len(line.strip()) > 0]   # 将代码分割成一行行的，然后再次过滤空行
                        if not ftype in res.keys(): res[ftype] = 0      # 计入统计
                        res[ftype] += len(codelines)
                        if not file_count_key in res.keys() : res[file_count_key] = 1
                        res[file_count_key] += 1
                        print('%5d  %s' % (len(codelines), curp))
                except Exception as e: print(curp, e)

'''
启动统计
'''
def start_with_args(args):
    if len(args) == 1:
        print('没有选择统计目录')
        return
    res = {}
    if len(args) == 2: classify_count(args[1], res, [], [])
    else:
        et = []
        ef = []
        for i in range(2,len(args)):
            carg = args[i]
            if len(carg) >= 4:
                if carg[:3] == 'ef=': ef = (carg[3:]).split(',')
                if carg[:3] == 'et=': et = (carg[3:]).split(',')
        classify_count(args[1], res, et, ef)
    if len(res) > 0:
        print('\n\n')
        print('>|-----------------------------------------\n>|')
        print('>|\n>|    以下是统计结果\n>|\n>|')
        print('>|     行数 | 类型')
        print('>|    --------------')
        for key in res.keys(): print('>|  %7d | %s' % (res[key], key))
        print('>|\n>|')
        print('>|-----------------------------------------\n\n')
if __name__ == '__main__':
    start_with_args(sys.argv)
