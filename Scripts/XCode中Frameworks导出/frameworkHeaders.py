#coding:utf-8
#auth:JyHu

'''
将XCode中的各个平台的SDK导出到目标目录，可以导出为markdown文件和头文件
使用方法：
python 脚本文件名 保存地址
eg:
    python frameworkHeaders.py /Users/JyHu/Desktop/t
'''


import sys
import os
import shutil

# dest_path = '/Users/JyHu/Desktop'       # 要将SDK文件存到某处~
PLATFORM_PATH = '/Applications/Xcode.app/Contents/Developer/Platforms'  # XCode目录，应该都是在这里吧。

def create_dir(p):
    if not os.path.isdir(p):
        os.makedirs(p)
        return p

def revHeaders(dest_path):
    if os.path.isdir(PLATFORM_PATH):
        platforms = os.listdir(PLATFORM_PATH)
        if len(platforms) > 0:
            p_path = create_dir(dest_path + '/' + 'Platform_md')    # 存放md文件的目录
            h_path = create_dir(dest_path + '/' + 'Platform_H')     # 存放拷贝的头文件的目录
            for platform in platforms:
                pname = platform[:platform.find('.')]   # platform名字，去掉后面的名称
                dest_plt_path = create_dir(p_path + '/' + pname)    # 存放md的platform目录
                dest_h_path = create_dir(h_path + '/' + pname)      # 存放头文件的platform目录

                fw_path = PLATFORM_PATH + '/' + platform + '/Developer/SDKs/' + pname + '.sdk/System/Library/Frameworks'    # Frameworks目录
                if os.path.isdir(fw_path):              # 判断类库目录是否存在
                    frameworks = os.listdir(fw_path)    # 读取目录下的所有Framework
                    if len(frameworks) > 0:
                        for frmk in frameworks:             # 遍历Framework
                            headers_folder_path = fw_path + '/' + frmk + '/Headers'     # 每个Framework下头文件的地址
                            if os.path.isdir(headers_folder_path):                      # 判断头文件是否存在
                                dfpath = create_dir(dest_plt_path + '/' + frmk[:frmk.find('.')])    # 在目标目录为当前Framework创建一个目录
                                dhpath = create_dir(dest_h_path + '/' + frmk[:frmk.find('.')])
                                headers = os.listdir(headers_folder_path)           # 当前Framework下所有的头文件
                                if len(headers) > 0:
                                    for header in headers:                              # 遍历所有头文件
                                        if header[header.find('.'):] == '.h':           # 判断是否是.h头文件
                                            file_path = headers_folder_path + '/' + header  # 头文件的实际地址
                                            if os.path.isfile(file_path):
                                                shutil.copyfile(file_path, dhpath + '/' + header)   # 复制文件到目标地址
                                                file_name = header[:header.find('.')]       #头文件的名字
                                                df_file = dfpath + '/' + file_name + '.md'  # 要保存到的路径
                                                try:
                                                    with open(file_path, 'rb') as f:
                                                        with open(df_file, 'wb') as fn:
                                                            fn.write('```\n\n'.encode('utf-8') + f.read() + '\n\n```'.encode('utf-8'))  #读取Framework头文件内容，并加头尾转成md文档保存
                                                except Exception as e: print(e, header)
                                                else: print('> > > > > 文件操作成功', header)
                                            else: print('头文件地址不存在')
                                        else: print(header, '  不是.h的头文件')
                                    print('> > > framework操作结束', frmk)
                                else: print ('所要查找的Framework地址内没有头文件')
                            else: print('所要查找的Frameworks头文件地址不是一个目录')
                        print('> 平台操作结束', platform)
                    else: print('所要查找的地址下没有Framework库文件')
                else: print('所要查找的库文件地址不存在')
            print('所有操作完成。')
        else: print('不存在各平台信息，目标地址错误')
    else: print('平台地址错误，不是一个目录')

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        revHeaders(sys.argv[1])
    else:
        print('请选择保存地址')
