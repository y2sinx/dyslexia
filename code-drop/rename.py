import os
import re
import sys

def rename(workdir='F:/英语/Miranda/TXT/',pat='s[0-9]{2}e[0-9]{2}',head='Miranda_',ext='.txt',):
    """批量重命名:newname=head+pat+ext"""
    olddir = os.getcwd()
    os.chdir(workdir)
    paths = os.listdir(workdir)
    for path in paths:
        mid = re.findall(pat,path)
        if mid!=[]:
            newname = head+mid[0]+ext
            os.rename(path, newname)
            print(path+' -> '+newname)
    os.chdir(olddir)
def review():
    """批量修改文件的内容"""
    pass

# 1. 将单集字幕复制到notebook  
# 1. 在notebook中设置分段  
# 1. 在音频或者视频中设置循环点 
# 1. 扫荡所有的陌生词汇或者表达  
