# -*- coding: utf-8 -*-

import pyperclip
def revise_lines(ptn="*",fn="F:/Git2/English/test/bigtan.txt"):
    """修订词条"""
    dt=English_Dictionary().load(fn) #导入词表
    with open(fn,'r',encoding='utf-8') as fp:
        flines = fp.readlines()

    need_change = [line for line in flines if re.findall(ptn,line)!=[]]
    num=len(need_change)
    print("共查询到:{}个.".format(num))
    cmd = input("proceed[#num]:".format(num))
    if cmd==str(num):
        new_flines=[]
        while cmd!="exit":
            for line in flines:
                if line in need_change:
                    pyperclip.copy(line) #将未修改行添加到粘贴板
                    print("[old:]{}".format(line))
                    new=input("[new line]").strip()
                    if len(new)<=5: 
                        new=input("[new]:").strip()                    
                    new_flines.append(new)
                    print("(t+){}>>{}".format(omit_line(line),omit_line(new)))
                    cmd=input("proceed[enter]:")
                else:
                    new_flines.append(line)
        with open(fn+'.new.txt','w',encoding='utf-8') as fp2:
            fp2.writelines(new_flines)
            return "Done!"
    else:
        return "要修改的行个数太多,过程不能中断;"