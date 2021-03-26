#######################################################
### Name: dt-magic
### Time: 2021-02-15
### User: y2sinx@126.com
#######################################################
# -*- coding: utf-8 -*-
from IPython.core.magic import (
    Magics,
    magics_class,
    line_magic,
    cell_magic,
    line_cell_magic,
)
from IPython.core.getipython import get_ipython

import os, pickle
import num2words
from dyslexia import NEEDED_PATH
from dyslexia.english import EnDict
from dyslexia.word_net import wn_dict
# from dyslexia.google_trans import gg_trans
from dyslexia.ht import print_line, tan
from dyslexia.youdao import yd_dict
import pyperclip
from googletrans import Translator

## 使用 dyslexia.ht -> .pkl
def pkl_check():
    """将 dyslexia.ht 转化为 pkl 文件 可加快导入速度."""

    try:
        wp = NEEDED_PATH["dyslexia.pkl"]
        print("已找到文件: {}. \n若需使用新的文件,请将其删掉后重新执行!".format(wp))
    except KeyError:
        print("未找到文件<dyslexia.pkl>!" "")

        try:
            wh = NEEDED_PATH["dyslexia.ht"]
            print("已找到文件: {}!. \n现开始转化:".format(wh))

            words = EnDict(wh)

            wk = os.path.split(wh)[0] + "\\" + "dyslexia.pkl"
            words.to_pickle(wk)

            return wk

        except KeyError:
            print(
                "未找到文件<dyslexia.ht>. 请下载后重试: https://github.com/y2sinx/dyslexia-data!"
                ""
            )
            
def pkl_to_en(file):
    """取出pkl文件中的EnDict实例.
    pkl文件必须是从EnDict().to_pickle()方式得到的,否则会出现莫名其妙的bug???"""
    with open(file, "rb") as fp:
        en = pickle.load(fp)
    print("DigTan # {} # {}!".format(en.l, file))
    return en

pkl_check()