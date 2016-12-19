#coding:utf-8



"""

简单的提交图片到七牛

python 脚本地址 图片地址 [是否需要图片压缩]

eg：

python ~/Dropbox/useful_script/Scripts/md文件图片图床转换/pic_to_qiniu.py ~/Desktop/93.jpg 1

"""




import os
import sys
import time
import qiniu
import tinify
import random
import imghdr
from qiniu 	 import *
from hashlib import md5

ak = ''
sk = ''
domain = 'xxxxxxxxx.bkt.clouddn.com' # 上传域名
bucket = '' # 空间名称

tinify.key = '' # 设置tinipng的key

q = Auth(ak, sk)    # 七牛认证

def upload(img, need_zip):
	if os.path.exists(img) and os.path.isfile(img):
		if imghdr.what(img):
			if need_zip:
				try:
					o_img = img + '.ori'
					if not os.path.isfile(o_img) or not imghdr.what(o_img):     # 如果没有的话，那就需要进行压缩处理
						print('压缩图片 ：', img) 
						s_img = tinify.from_file(img)
						s_img.to_file(img + '.z')
						os.rename(img, img + '.ori')
						os.rename(img + '.z', img)
				except Exception as e:
					print('图片压缩错误')
			rstr = str(time.time())+''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 12))
			key = md5(rstr.encode('utf-8')).hexdigest()   # 上传到七牛后的图片名
			mime_type = 'image/%s' % img[img.rfind('.') + 1:]
			token = q.upload_token(bucket, key)
			ret, info = put_file(token, key, img, mime_type=mime_type, check_crc=True)
			if ret['key'] == key and ret['hash'] == etag(img): print('图片地址：' + 'http://' + domain + '/' +key)
			else :t('上传失败')

if __name__ == '__main__':
	if len(sys.argv) >= 2:
		need_zip = False
		if (len(sys.argv) >= 3):
			need_zip = sys.argv[2] == '1'
		upload(sys.argv[1], need_zip)