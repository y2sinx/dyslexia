#######################################################
### name: dt-magic
### change time: 2020-7-7
### From: y2sinx@126.com
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

import os
import pickle
import num2words
from ddpie import NEEDED_PATH
from ddpie.dyslexia.english import wn_dict, ggtrans, EnDict
from ddpie.dyslexia.ht import print_line, tan
from ddpie.dyslexia.youdao import yd_dict
import pyperclip

################################################################
## 若使用%dt魔法命令,必须将(dyslexia的)两个ht文件转化为pkl文件:
## 删掉旧的 dt_words.pkl 和 dt_phrases.pkl
## 在 https://github.com/y2sinx/dyslexia 下载 dt_words.rar 和 dt_phrases.rar
## 将其解压在 ROOT 内任意位置, 以便 get_needed_path() 会找到其位置.
## 执行 pkl_check(), 返回两个新的 pkl 文件
## 注意: pkl文件必须是通过 EnDict().to_pickle() 方式得到的, 否则在导入该模块时会出现莫名其妙的bug???
################################################################
def pkl_check():
    """若使用%dt魔法命令,必须将(dyslexia的)两个ht文件转化为pkl文件."""

    try:
        wp = NEEDED_PATH["dt_words.pkl"]
        pp = NEEDED_PATH["dt_phrases.pkl"]
        print("已找到文件: \n\t{},\n\t{}!\n若需使用新的文件,请将其删掉后重新执行!".format(wp, pp))
    except KeyError:
        print("未找到文件<dt_words.pkl>与<dt_phrases.pkl>!" "")

        try:
            wh = NEEDED_PATH["dt_words.ht"]
            ph = NEEDED_PATH["dt_phrases.ht"]
            print("已找到文件: \n\t{},\n\t{}!\n现开始转化:".format(wh, ph))

            words = EnDict(wh)
            phrases = EnDict(ph)

            wk = os.path.split(wh)[0] + "\\" + "dt_words.pkl"
            words.to_pickle(wk)

            pk = os.path.split(ph)[0] + "\\" + "dt_phrases.pkl"
            phrases.to_pickle(pk)

            return wk, pk

        except KeyError:
            print(
                "未找到文件<dt_words.ht>与<dt_phrases.ht>!\n请下载后重试: https://github.com/y2sinx/DigTan-English!"
                ""
            )


def pkl_to_en(file):
    """取出pkl文件中的EnDict实例.
    pkl文件必须是从EnDict().to_pickle()方式得到的,否则会出现莫名其妙的bug???"""
    with open(file, "rb") as fp:
        en = pickle.load(fp)
    print("DigTan # {} # {}!".format(en.l, file))
    return en


################################################################
## 判断是否载入词典,只有载入词典,才能使用 %dt_* 命令
################################################################
# cmd = input("Load DigTan-English(n/[y])? ")
# if cmd == "" or cmd == "y":  # 确认是否载入词典
EN_WORDS = pkl_to_en(NEEDED_PATH["dt_words.pkl"])  ##用于匹配单词
EN_PHRASES = pkl_to_en(NEEDED_PATH["dt_phrases.pkl"])  ##用于匹配短语
EN = EnDict().update(EN_WORDS.d).update(EN_PHRASES.d)  ##将单词和词组合在一起后一起搜索
make_wl = EN_WORDS.make_wordlist

################################################################
## 与dyslexia相关的魔法命令
################################################################
@magics_class
class DtMagic(Magics):
    """从内嵌类Magics,定义自己的类DtMagic"""

    @line_magic("dt")
    def _dt(self, line):
        """查看单词或短语的含义,输出多行."""

        if line.strip() == "":
            return "格式: %dt 单词或短语"
        line = EN.lookup_fz(line.strip())
        if line != None:
            print_line(line)

    @line_magic("match_words")
    def _match_words(self, line):
        """使用Unix通配符匹配单词."""

        if line.strip() == "":
            return "格式: %dw word_matcher"
        matcher = line.strip()
        return EN_WORDS.match(matcher)

    @line_magic("match_phrases")
    def _match_phrases(self, line):
        """使用Unix通配符匹配短语."""

        if line.strip() == "":
            return "格式: %dp phrase_matcher"
        matcher = line.strip()
        return EN_PHRASES.match(matcher)

    @line_magic("dtl")
    def _dt_line(self, line):
        """查看单词或短语的含义,输出单行."""
        if line.strip() == "":
            return "格式: %dt word_or_phrase"
        line = EN.lookup_fz(line.strip())
        if line != None:
            return line

    @line_magic("n2w")
    def _number_to_word(self, line):
        items = line.split(" ")
        while " " in items:
            items = items.remove(" ")
        if len(items) == 1:
            print(num2words.num2words(items[0]))
        else:  # opt=='-o'或任意  #序数词
            print(num2words.num2words(items[1], to="ordinal"))

    @line_magic("tan")
    def _tan(self, line):
        """tan(ptn,file_or_key,flag_print_ht=True)的魔法命令: 按正则表达式的模式搜索文件的匹配项.
        格式: %tan [-r] ptn file.
        1)搜索单词: `%tan ^commons. dt_words.ht`
        2)搜索短语: `%tan a.little dt_phrase.ht`, 注意,由于cell行取参时使用空格,将ptn中的空格暂用.代替.
        3)搜索中文: `%tan 能量 dt_words.d`
        4)-r选项: `%tan -r 能量 dt_words.d`, 表示只返回头部,而不显示整行.
        """
        if line.strip() == "":
            return "格式: %tan [-r] ptn file(不带引号)."
        pos = line.find(" ")
        opt = line[:pos].strip()
        line = line[pos + 1 :].strip()
        if opt == "-r":
            flag_print_ht = False
            pos2 = line.find(" ")
            ptn = line[:pos2].strip()
            file_or_key = line[pos2 + 1 :].strip()

        else:
            flag_print_ht = True  # 打印搜索到的行
            pos = line.find(" ")
            ptn = opt
            file_or_key = line

        if file_or_key == "w":  # 将单词文件简写为w
            file_or_key = "dt_words.ht"
        elif file_or_key == "p":
            file_or_key = "dt_phrases.ht"
        else:
            pass

        out = tan(ptn, file_or_key, flag_print_ht=flag_print_ht)  # 打印行
        if out != None:
            return out

    @line_magic("yd")
    def _youdao(self, line):
        """使用有道查单词的含义."""
        out = yd_dict(line.strip())
        print_line(out)

    @line_magic("wn")
    def _wordnet(self, line):
        """使用有道查单词的含义."""
        wn_dict(line.strip())

    @line_cell_magic("gg")
    def _ggtrans(self, line, cell):
        """使用谷歌翻译API翻译段落的魔法命令."""

        if line.strip() == "0" or line.strip() == "False":
            out = ggtrans(cell, en2cn=False)  ##中文转英文
        else:  ##英文转中文
            out = ggtrans(cell, en2cn=True)

        print(out)

        pyperclip.copy(out)  ##直接将译文复制到粘贴板


get_ipython().register_magics(DtMagic)

