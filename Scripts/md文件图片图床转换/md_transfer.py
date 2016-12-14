#coding:utf-8



"""

转换md文件中的图片

python 脚本地址 文件地址 [是否需要压缩]

eg：

python ~/Dropbox/useful_script/Scripts/md文件图片图床转换/md_transfer.py ~/Desktop/t.md 0

0 - 不需要图片压缩
1 - 需要图片压缩

"""




import re
import os
import sys
import time
import math
import imghdr
import shutil
import random
import string
import tinify
import urllib
import sqlite3
import operator
from hashlib import md5
from qiniu import Auth, put_file, etag


ak = ''
sk = ''
domain = '' # 上传域名
bucket = '' # 空间名称

tinify.key = '' # 设置tinipng的key

q = Auth(ak, sk)    # 七牛认证
md_loc = ''    # md地址
need_zip = True

def upload_file(upload_file_name):
    '''
    根据给定的图片名上传图片，并返回图片地址和一些上传信息
    '''
    rstr = str(time.time())+''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 12))
    key = md5(rstr.encode('utf-8')).hexdigest()   # 上传到七牛后的图片名
    mime_type = 'image/%s' % upload_file_name[upload_file_name.rfind('.') + 1:]
    token = q.upload_token(bucket, key)
    ret, info = put_file(token, key, upload_file_name, mime_type=mime_type, check_crc=True)
    if ret['key'] == key and ret['hash'] == etag(upload_file_name):
        return 'http://' + domain + '/' +key, info
    return None

def cached_img_url(img_loc_path):
    '''
    根据给定的本地图片绝对路径，转换成一个网上路径。
    如果本地缓存中有，则直接读取并返回，如果没有，则上传后返回。
    '''
    conn = sqlite3.connect(md_loc + '/img_hash_cache.db')
    cursor = conn.cursor()
    try:
        cursor.execute(''' 
            CREATE TABLE img_cache_table (
                img_hash TEXT,
                real_p TEXT,
                img_url TEXT,
                u_info TEXT
            )
            ''')
    except Exception as e: pass
    img_hash = md5(open(img_loc_path, 'rb').read()).hexdigest()     # 图片的hash值，用来确定图片的唯一性，避免多次上传，浪费流量
    cursor.execute("SELECT img_url FROM img_cache_table WHERE img_hash='%s'" % img_hash)    #根据图片的hash值来找缓存下来的图片网址
    select_res = [row for row in cursor]
    img_url = (select_res[0][0] if select_res and len(select_res) > 0 and select_res[0] and len(select_res[0]) > 0 else None)

    remote_exists = False
    if img_url:
        try: remote_exists = urllib.request.urlopen(img_url).code == 200
        except Exception as e: 
            print('网址不存在 ：', img_url)
            remote_exists = False
    if not img_url or not remote_exists:     # 如果没有查到图片的网址，或者网址失效
        print('上传图片 ：', img_loc_path)
        img_url, uinfo = upload_file(img_loc_path)  # 接取上传后的图片信息
        if not img_url:     # 如果图片地址为空，则说明上传失败
            print('上传失败')
            conn.close()
            return None
        else:
            if not remote_exists:  cursor.execute('INSERT INTO img_cache_table VALUES(?,?,?,?)', (img_hash, img_loc_path, img_url, str(uinfo))) # 如果上传成功，则直接缓存下来
            else :  cursor.execute("UPDATE img_cache_table SET img_url='%s', u_info='%s' WHERE img_hash='%s'" % (img_url, str(uinfo), img_hash))
            conn.commit()
    conn.close()

    return img_url

def md_img_find(md_file):
    '''
    将给定的markdown文件里的图片本地路径转换成网上路径
    '''
    post = None  # 用来存放markdown文件内容
    with open(md_file, 'r') as f:
        post = f.read()
        matches = re.compile('!\\[.*?\\]\\((.*?)\\)').findall(post)     # 匹配md文件中的图片
        if matches and len(matches) > 0:
            for match in matches:   # 遍历去修改每个图片
                if not re.match('((http(s?))|(ftp))://.*', match):  # 判断是不是已经是一个图片的网址
                    loc_p = match
                    if not os.path.exists(loc_p) or not os.path.isfile(loc_p):  # 如果文件不存在，则可能这是用的一个相对路径，需要转成绝对路径
                        loc_p = md_file[:md_file.rfind('/')+1] + match
                    if os.path.exists(loc_p) and os.path.isfile(loc_p):
                        if imghdr.what(loc_p):  # 如果是一个图片的话，才要上传，否则的话，不用管
                            if need_zip:
                                o_img = loc_p + '.ori'  # 原始未压缩的图片
                                if not os.path.isfile(o_img) or not imghdr.what(o_img):     # 如果没有的话，那就需要进行压缩处理
                                    print('压缩图片 ：', loc_p) 
                                    s_img = tinify.from_file(loc_p)
                                    s_img.to_file(loc_p + '.z')
                                    os.rename(loc_p, loc_p + '.ori')
                                    os.rename(loc_p + '.z', loc_p)
                            file_url = cached_img_url(loc_p)    # 获取上传后的图片地址
                            if file_url:    # 在图片地址存在的情况下进行替换
                                print('图片地址是 ： ', file_url)
                                post = post.replace(match, file_url)    # 替换md文件中的地址
                        else:
                            print('不是一个图片文件 ：', loc_p)
                            continue
                    else: print('文件不存在 ：', loc_p)
                else: print('markdown文件中的图片用的是网址 ：', match)
    if post: open(md_file, 'w').write(post) #如果有内容的话，就直接覆盖写入当前的markdown文件

def find_md(folder):
    '''
    在给定的目录下寻找md文件  
    '''
    if len(folder) > 3: 
        if folder[folder.rfind('.') + 1:] == 'md': md_img_find(folder) # 判断是否是一个md文件，如果是的话，直接开始转换
    elif os.path.isdir(folder):
        files = os.listdir(folder)
        # 读取目录下的文件
        for file in files:
            curp = folder + '/' + file
            if os.path.isdir(curp): find_md(curp) # 递归读取
            elif file[file.rfind('.') + 1:] == 'md': md_img_find(curp)

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        if len(sys.argv) >= 3:
            need_zip = sys.argv[2] == '1'
        c_p = sys.argv[0]
        md_loc = c_p[:c_p.rfind('/') + 1]
        find_md(sys.argv[1])
