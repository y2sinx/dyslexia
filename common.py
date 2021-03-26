# -*- coding: utf-8 -*-
import re, os, time
from dyslexia import NEEDED_PATH

import numpy as np

MARK_WIDTH=32
UNF_TXT = NEEDED_PATH['unf.txt']

##############################################################################
# # 所有的半角字符: unicode编码从33-126,外加22号半角空格'A B'
# HALF_ANGLE_CHARACTER=[' '] + get_unicode_chars(33,126,n_col=1).ravel().tolist()
# # 所有的全角字符: unicode编码从65281-65374, 外加12288号全角空格'A　B'
# FULL_ANGLE_CHARACTER=['　'] + get_unicode_chars(65281,65374,n_col=1).ravel().tolist()

FULL_HALF_PAIRS = [
    ("\u3000", " "),
    ("！", "!"),
    ("＂", '"'),
    ("＃", "#"),
    ("＄", "$"),
    ("％", "%"),
    ("＆", "&"),
    ("＇", "'"),
    ("（", "("),
    ("）", ")"),
    ("＊", "*"),
    ("＋", "+"),
    ("，", ","),
    ("－", "-"),
    ("．", "."),
    ("／", "/"),
    ("０", "0"),
    ("１", "1"),
    ("２", "2"),
    ("３", "3"),
    ("４", "4"),
    ("５", "5"),
    ("６", "6"),
    ("７", "7"),
    ("８", "8"),
    ("９", "9"),
    ("：", ":"),
    ("；", ";"),
    ("＜", "<"),
    ("＝", "="),
    ("＞", ">"),
    ("？", "?"),
    ("＠", "@"),
    ("Ａ", "A"),
    ("Ｂ", "B"),
    ("Ｃ", "C"),
    ("Ｄ", "D"),
    ("Ｅ", "E"),
    ("Ｆ", "F"),
    ("Ｇ", "G"),
    ("Ｈ", "H"),
    ("Ｉ", "I"),
    ("Ｊ", "J"),
    ("Ｋ", "K"),
    ("Ｌ", "L"),
    ("Ｍ", "M"),
    ("Ｎ", "N"),
    ("Ｏ", "O"),
    ("Ｐ", "P"),
    ("Ｑ", "Q"),
    ("Ｒ", "R"),
    ("Ｓ", "S"),
    ("Ｔ", "T"),
    ("Ｕ", "U"),
    ("Ｖ", "V"),
    ("Ｗ", "W"),
    ("Ｘ", "X"),
    ("Ｙ", "Y"),
    ("Ｚ", "Z"),
    ("［", "["),
    ("＼", "\\"),
    ("］", "]"),
    ("＾", "^"),
    ("＿", "_"),
    ("｀", "`"),
    ("ａ", "a"),
    ("ｂ", "b"),
    ("ｃ", "c"),
    ("ｄ", "d"),
    ("ｅ", "e"),
    ("ｆ", "f"),
    ("ｇ", "g"),
    ("ｈ", "h"),
    ("ｉ", "i"),
    ("ｊ", "j"),
    ("ｋ", "k"),
    ("ｌ", "l"),
    ("ｍ", "m"),
    ("ｎ", "n"),
    ("ｏ", "o"),
    ("ｐ", "p"),
    ("ｑ", "q"),
    ("ｒ", "r"),
    ("ｓ", "s"),
    ("ｔ", "t"),
    ("ｕ", "u"),
    ("ｖ", "v"),
    ("ｗ", "w"),
    ("ｘ", "x"),
    ("ｙ", "y"),
    ("ｚ", "z"),
    ("｛", "{"),
    ("｜", "|"),
    ("｝", "}"),
    ("～", "~"),
]

# 中文标点转英文标点
CH_EN_PAIRS = [
    ("。", "."),  ##句号
    ("？", "?"),  ##问号
    ("！", "!"),  ##叹号
    ("，", ","),  ##逗号
    ("、", ","),  ##顿号
    ("；", ";"),  ##分号
    ("：", ":"),  ##冒号
    ("“", '"'),  ##引号
    ("”", '"'),
    ("‘", "'"),
    ("’", "'"),
    ("「", "'"),  ##直角引号
    ("」", "'"),
    ("『", "'"),
    ("』", "'"),
    ("（", "("),  ##圆括号
    ("）", ")"),
    ("〔", "["),
    ("〕", "]"),
    ("【", "["),  ##方头括号
    ("】", "]"),
    #    ('—', '—'), ##连接号,不要替换英文破折号
    #     ('…', '…'), ##省略号,实则两个(6个点)
    ("～", "~"),  ##浪纹线
    ("·", "⋅"),  ##间隔号
    ("《", "<"),  ##书名号
    ("》", ">"),
    ("〈", "<"),
    ("〉", ">"),
]

# 英文标点转中文标点
EN_CH_PAIRS = [
    (".", "。"),
    ("?", "？"),
    ("!", "！"),
    (",", "，"),
    (";", "；"),
    (":", "："),
    ('"', "“"),
    ("'", "‘"),
    ("'", "』"),
    ("(", "（"),
    (")", "）"),
]  ## 自己处理顿号
##############################################################################


class Bunch(dict):
    """使用`.`运算符获取字典的键值;"""

    def __init__(self, *args, **kwargs):
        super(Bunch, self).__init__(*args, **kwargs)
        self.__dict__ = self


def progress_bar(i, total, info="", trigger=1000):
    """打印一行进度条. 
    i: 当前序号,从1开始计数; length:总长度;
    trigger: i变动多少次? 才能触发print."""
    if trigger != 0:
        if i == 1:
            print("Total:{}.".format(total))
            print("-" * 32)
        if i % trigger == 0:
            print("{}/{}: {}".format(i, total, info))


def present_time():
    """当前时间;"""
    now = time.localtime(time.time())
    time_now = "{:4d}_{:02d}_{:02d}_{:02d}_{:02d}_{:02d}".format(
        now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec
    )
    return time_now


def backup(fn, info=None):
    """备份文件并添加备注信息;"""
    if info == None:
        info = present_time()
    bkp = fn + "." + info + ".bk"
    if os.path.exists(bkp) == False:
        with open(fn, "r", encoding="utf-8") as fp:
            strings = fp.read()
        with open(bkp, "w", encoding="utf-8") as bp:
            bp.write(strings)
    _, bkp = os.path.split(bkp)
    print("Backup: {}!".format(bkp))


# 将其改为魔法命令
def module_location(module_name):
    """打印模块所在的目录位置"""
    module_dir = os.path.dirname(os.path.abspath(module_name.__file__))
    print(module_dir)


def punctuator(raw, ch_to_en=True):
    """标点转换器,默认将中文标点(全角)转化为英文标点(半角);"""
    if ch_to_en:
        table = {ord(f): ord(t) for f, t in set(CH_EN_PAIRS + FULL_HALF_PAIRS)}
        raw = raw.replace("…", "...")
    else:  ##测试
        table = {ord(f): ord(t) for f, t in EN_CH_PAIRS}
    return raw.translate(table)


from fnmatch import fnmatchcase


def dir_fz(target, matcher=None, exclued_upper=True):
    """dir的增进版(further);target是包或模块时,返回包或模块的属性列表(包含函数,变量等);target是某个类的实例时,返回实例所拥有的方法列表;
    多个if并列的过程类似于一个管道,满足参数条件就要执行一次筛选;"""

    out = [i for i in dir(target) if i[0] != "_"]
    if exclued_upper:
        out = [i for i in out if i[0].islower()]
    if matcher != None:
        out = [one for one in out if fnmatchcase(one, matcher)]
    return out


def show_file(file, head=0, tail=0, lns=[]):
    """在控制台中显示文件片段. 
    lns:指定显示行的行标;可迭代序列;
    head:显示文件的头几行;
    tail:显示文件的尾几行;
    三个参数只能设置一个不为`0`, 否则打印所有行"""

    with open(file, "r", encoding="utf-8") as fp:
        lines = fp.readlines()
        l = len(lines)  ##文件总行数

        for i, line in enumerate(lines):
            if head != 0:  ##打印文件头
                if i + 1 <= head:
                    print("{:3d}: {:s}".format(i + 1, line), end="")
            elif tail != 0:  ##打印文件尾
                if i >= l - tail:  ## i+1 >= l+1-tail
                    print("{:3d}: {:s}".format(i + 1, line), end="")
            elif len(lns) != 0:  ##打印文件指定行
                if i + 1 in lns:
                    print("{:3d}: {:s}".format(i + 1, line), end="")
            else:  ##打印所有行
                if i + 1 <= 999:  ##最多只查看999行
                    print("{:3d}: {:s}".format(i + 1, line), end="")
                else:
                    print("... ...")
                    return


def search(ptn, file_or_key, flag_print=True, emphasize=u"\u2705"):
    """按指定的正则表达式(ptn)搜索指定文件(file)的行(flag_print表示是否打印改行); 
    l: 搜索非`head:tail`文件时添加; 此时将文件的行号作为head;
    emphasize可选值: ✅,'♬','⚡','😏','🐷'..."""
    # file_or_key
    try:
        file = NEEDED_PATH[file_or_key]
    except:
        file = file_or_key

    with open(file, "r", encoding="utf-8") as fp:
        lines = fp.readlines()

    line_numbers = []
    for i, line in enumerate(lines):
        fa = re.findall(ptn, line)
        if fa != []:
            string = fa[0]
            line_numbers.append(i)
            line = line.replace(
                string, "{}{}{}".format(emphasize, string, emphasize), 1
            )
            line = "#" + str(i + 1) + ":" + "\n" + "-" * MARK_WIDTH + "\n" + line
            if flag_print:
                print(line)  # line中一般包含了一个换行符,因此打印出来的行之间有一个空白行
    if not flag_print:
        return sorted(set(line_numbers))


def search_needed(ptn):
    """全目录搜索: 查看一个子串(ptn)在某个目录中(dir_path)的来源文件;查看某个单词(ptn)的来源词表(basic);"""
    paths = []
    for file, path in NEEDED_PATH.items():
        try:
            with open(path, "r", encoding="utf-8") as fp:
                lines = fp.readlines()
            for line in lines:
                if re.findall(ptn, line) != []:
                    paths.append(file)
                    break  # 中断该次循环
        except:
            pass
    return paths


# def search_all_files(ptn,dir_path,flag_print=False,ln=False):
#     """搜索目录下的所有文件"""
#     heads=set()
#     root,name=os.path.split(dir_path)
#     for file in os.listdir(dir_path):
#         wordf=search(ptn,root+'/'+file,flag_print,ln)
#         if flag_print:
#             print(file.center(24,'='))


#         heads.update(wordf)
#     return list(heads)


from tabulate import tabulate
from IPython.display import Markdown, display_markdown


def number_base_conversion(sequence=range(32, 126), fmt="simple"):
    """将任意多个任意进制的数字或者字符,表示为所有进制+Unicode的形式."""
    lines = []
    if type(sequence) == int:
        sequence = [sequence]  # 接收单个数字
    for one in sequence:
        if isinstance(one, str):
            one = ord(one)  # 如果one是个字符而不是数字
        line = [bin(one), oct(one), int(one), hex(one), chr(one)]
        lines.append(line)
    head = ["bin", "oct", "int", "hex", "chr"]

    if fmt == "md":  # 在jupyter上可以显示markdown格式的表格
        table_md = tabulate(lines, headers=head, tablefmt="pipe")  # pipe: markdown形式
        display_markdown(Markdown(table_md))  # 创建markdown对象然后显示
    else:  # 在ipython上必须显示非markdown形式
        table_md = tabulate(
            lines, headers=head, numalign="right", stralign="right", tablefmt=fmt
        )  # pipe: markdown形式
        print(table_md)


def get_unicode_chars(start, end, n_col=4, occupy="$"):
    """打印指定范围内的unicode字符."""
    if type(start) == str:
        start = ord(start)
    if type(end) == str:
        end = ord(end)
    if start > end:
        return "start>end"

    seq = range(start, end + 1)  # 包含末尾
    lt = [chr(i) for i in seq]

    n_raw = int(np.ceil(len(lt) / n_col))  # 向上取整
    delta = n_raw * n_col - (end - start + 1)
    lt = lt + [occupy] * delta
    out = np.array(lt).reshape(n_raw, n_col)
    return out


from datetime import date


def calculate_age(year_birth=1, month_birth=1, day_birth=1):
    """计算目标物的年龄;从0开始计算;"""
    bornday = date(year_birth, month_birth, day_birth)  # date(1993,11,10)
    today = date.today()  # (2018, 10, 30)
    try:
        # 将今年的年份替换掉生日中的年份, 今年的生日时间
        birthday = bornday.replace(year=today.year)  # (2018, 11, 10)
    except ValueError:
        # 如果生日是2/29, 今年的时间中可能没有其生日, 提前一天过生日
        birthday = bornday.replace(year=today.year, day=bornday.day - 1)
    # 出生的那天定义为0岁
    if birthday > today:
        age = today.year - bornday.year - 1  # 未过当年生日, 岁数为年差减1
    else:
        age = today.year - bornday.year  # 已过当年生日, 岁数就是年差
    print(">>目标物当前 {} 岁;".format(age))


def doc(obj, flag_print=True, flag_return=False):
    """返回对象的参考文档;"""
    raw = obj.__doc__
    if flag_print:
        print(raw)
    if flag_return:
        return raw


from IPython.core.interactiveshell import InteractiveShell

sh = InteractiveShell.instance()


def doc_to_txt(root_obj):
    """查看对象及其子对象的参考文档;root_obj若果是模块,需要是模块的全称;"""
    out_file = root_obj.__name__ + ".txt"
    f = open(out_file, "w", encoding="utf-8")
    f.write(doc(root_obj, flag_print=False, flag_return=True) + "\n\n")
    for obj in dir_fz(root_obj):
        try:
            obj = root_obj.__name__ + "." + obj
            raw = doc(sh.ev(obj), flag_print=False, flag_return=True)
            marker = "=" * 80 + "\n" + obj + "\n"
            f.write(marker + raw + "\n\n")
        except:
            pass
    f.close()
    return out_file


import pickle
from Crypto import Random
from Crypto.Cipher import AES


def encrypt_aes(fn, key=b"12345678" * 2):
    """使用AES算法加密文本文件;密码必须为16位的字节串."""
    with open(fn, "r", encoding="utf-8") as origin:
        mingw = origin.read()  # 待加密的明文字符串
    mingw = mingw.encode()  # 将明文字符串表示为字节
    iv = Random.new().read(AES.block_size)  # iv: 随机的秘钥向量
    aes = AES.new(key, AES.MODE_CFB, iv)  # 使用key,iv,MODE_CFB模式,初始化AES对象
    ## 加密的明文长度必须为16的倍数. 算法自动补足?
    miw = iv + aes.encrypt(mingw)  # 将iv加添加到密文的开头

    idx = fn.find(".")
    ext = fn[idx:]
    fn2 = fn.replace(ext, "_miw" + ext)  # 将`origin.txt>origin_miw.pkl`
    with open(fn2, "wb") as fp:
        pickle.dump(miw, fp)
    print("Adding file: {}!".format(fn2))


def decrypt_aes(fn, key=b"12345678" * 2):
    """使用AES算法解密密文文件;密文文件更改后则无法解密;"""
    with open(fn, "rb") as fp:
        miw = pickle.load(fp)  # 带解密的密文字节串
    iv = miw[:16]
    aes = AES.new(key, AES.MODE_CFB, iv)  # 获取与与加密时相同的AES对象
    mingw = aes.decrypt(miw[16:])  # 对密文进行解密
    mingw = mingw.decode()  # 解码为可读形式: utf-8

    idx = fn.find(".")
    ext = fn[idx:]
    fn2 = fn.replace(ext, "_mingw" + ext)  # 将`origin_miw.pkl>origin_miw_mingw.txt`
    with open(fn2, "w", encoding="utf-8") as fp2:
        fp2.write(mingw)
    print("Adding file: {}!".format(fn2))


def reverse_string(raw="abcd"):
    """更改字符串的头尾顺序;"""
    order = []
    for i in raw:
        order.append(i)
    order.reverse()
    return "".join(order)


import chardet


def encoding_type(fn):
    """查看文件的编码类型;"""
    f = open(fn, "rb")
    data = f.read()
    return chardet.detect(data)


def dot_to_graph(dot_path):
    """将dot文件绘制成图;"""
    import graphviz

    with open(dot_path, "r", encoding="utf-8") as f:
        dot_graph = f.read()
    return graphviz.Source(dot_graph)


def print_save(obj, filename="obj.txt", mode="w"):
    """将对象的可打印内容打印到文件."""
    f = open(filename, mode, encoding="utf-8")
    print(obj, file=f)
    f.close()
    return filename


import json


def json_to_dict(fn):
    """将Json文件转化为字典;"""
    with open(fn, "r", encoding="utf-8") as fp:
        dn = json.load(fp)
    return dn


import html2text
from urllib.request import urlopen


def get_md_in_web(url, filename=UNF_TXT):
    """使用模块`html2text`将网页转化为Markdown文件;"""
    html = urlopen(url).read().decode("utf-8")
    text = html2text.html2text(html)
    text = punctuator(text)
    return print_save(text, mode="w", filename=filename)


import requests
from bs4 import BeautifulSoup


def get_main_text_in_web(url):
    """获取沪江英语中的口语文本;"""
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")

    en = []
    for line in soup.find_all(class_="langs_en"):
        line = line.get_text()
        en.append(line)

    cn = []
    for line in soup.find_all(class_="langs_cn"):
        line = line.get_text()
        cn.append(line)

    for i, j in zip(en, cn):
        print(punctuator(i) + " % " + punctuator(j))

import pyperclip
def return_copy(out):
    """复制一个return的返回字符串."""
    pyperclip.copy(str(out))
    print("Ctrl+V.")




from dyslexia import ROOT

Russian="""啊 波 屋 割 的   
耶 妖 日  - 一    
一 科 了 摸 呢   
窝 泼 嘞 丝 特  
巫 夫 喝 此 池  
施 西 哀 尤 牙"""

# 整理单词的固定文本
wx = "https://github.com/y2sinx/xi-mu-pu/blob/master/Menu/image/qrcode_wx.jpg?raw=true"

# 数字常量
MARK_WIDTH = 32
SPECIAL_PUNCT = {
'pzh': "—",
'dot': "⋅",
}

######################################################################################
# tips
######################################################################################
# 正则
RE_TIPS = {
    "汉字": r"[\u4e00-\u9fa5]+ 或 [一-龥]+",
    "其后不得含有": r"子串1(?!子串2)",
    "不包含子串的行": r"^((?!子串).)*$",
    "去掉单词释义中的人名串": r"\[n\][<A-z].+人名",
}

PYTHON_TIPS = {
    "Hex_to_Unicode_Char": r"u'\u0021'",
}


######################################################################################
# 词汇
######################################################################################
# wordnet.morphy中奇怪词干可能对应的单词
MORPHY = {
    "wa": ["was"],
    "ha": ["has"],
    "doe": ["does"],
    "le": ["less"],
    "discus": ["discuss"],
}

######################################################################################
# 标签
######################################################################################
TAGS = {
    "-": "accent;音标;",
    "a": "adjective;形容词;",
    "ad": "adverb;副词;",
    "art": "article;冠词;",
    "conj": "conjunction;连词;",
    "int": "interjection;感叹词;",
    "n": "noun;名词;",
    "num": "numeral;数词;",
    "prep": "preposition;介词;",
    "pron": "pronoun;代词;",
    "v": "verb;动词;",
    "vi": "intransitive verb;不及物动词;",
    "vt": "transitive verb;及物动词;",
    "auxv": "Auxiliary Verb;助动词,情态动词;",
    "syn": "synonym;近义词;",
    "ex": "example;例句,短语;",
    "sw": "similar words;形近词;",
    "def": "definition;定义,解释;",
    "+": "additional;单词形态变化;",
    "pl": "plural;名词复数;",
    "s3": "third person singular;第三人称单数;",
    "pr": "present participle;现在分词;",
    "pt": "past tense;过去式;",
    "pp": "past participle;过去分词;",
    "er": "comparative;比较级;",
    "est": "superlative;最高级;",
}
######################################################################################
# 音标
######################################################################################

# IPA: International_Phonetic_Alphabet
IPA_Fu_Hao = ["æ", "ð", "ŋ", "ɑ", "ɔ", "ə", "ʃ", "ʌ", "ʒ", "θ", "ɛ?"]
IPA_Yuan_Yin = [
    "i:",
    "i",
    "ə:",
    "ə",
    "ɔ:",
    "ɔ",
    "u:",
    "u",
    "ɑ:",
    "ʌ",
    "æ",
    "e",
    "ei",
    "ai",
    "ɔi",
    "au",
    "əu",
    "iə",
    "eə",
    "uə",
]
IPA_Fu_Yin = [
    "p",
    "b",
    "t",
    "d",
    "k",
    "ɡ",
    "s",
    "z",
    "ʃ",
    "ʒ",
    "tʃ",
    "dʒ",
    "f",
    "v",
    "θ",
    "ð",
    "ts",
    "dz",
    "tr",
    "dr",
    "h",
    "r",
    "l",
    "m",
    "n",
    "ŋ",
    "w",
    "j",
]
IPA_Qing_Fu_Yin = ["p", "t", "k", "f", "s", "θ", "ʃ", "h", "tʃ", "tr", "ts"]
IPA_Zhuo_Fu_Yin = [
    "b",
    "d",
    "dr",
    "dz",
    "dʒ",
    "j",
    "l",
    "m",
    "n",
    "r",
    "v",
    "w",
    "z",
    "ð",
    "ŋ",
    "ɡ",
    "ʒ",
]
IPA = {
    "i:": "嘴唇微微张开,舌尖抵下齿,嘴角向两边张开,露出微笑的表情,与字母E的发音相同;",
    "i": "嘴唇微微张开,舌尖抵下齿,舌前部抬高,嘴形扁平;",
    "ə:": "嘴形扁平,上下齿微开,舍身平放,舌中部稍稍抬高;",
    "ə": "嘴唇微微张开,舌身放平,舌中部微微抬起,口腔自然放松发声;",
    "ɔ:": "双唇收得小而圆,并向前突出,舌身往后缩;",
    "ɔ": "口腔打开,嘴张大,舌头向后缩,双唇稍收圆;",
    "u:": "嘴形小而圆,微微外突,舌头尽量后缩;",
    "u": "嘴唇张开略向前突出,嘴形稍收圆并放松些,舌头后缩;",
    "ɑ:": "口腔打开,嘴张大,舌身放平,舌尖不抵下齿,下巴放低,放松发音;",
    "ʌ": "嘴唇微微张开,伸向两边,舌尖轻触下齿,舌后部稍稍抬起;",
    "æ": "嘴张大,嘴角尽量拉向两边,成扁平形,舌尖抵下齿;",
    "e": "嘴形扁平,舌尖抵下齿,舌前部稍抬起;",
    "ei": "/e/重读,/i/轻读,口形由半开到合,字母A就发这个音;",
    "ai": "/a/重读,/i/轻读,口形由开到合,与字母I的发音相同;",
    "ɔi": "/ɔ/重读,/i/轻读,口形由圆到扁,由开到合;",
    "au": "/a/重读,/u/轻读,口型由大到小;",
    "əu": "/ə/重读,/u/轻读,口形由半开到小,与字母O的发音相同;",
    "iə": "/i/重读,/ə/轻读,双唇始终半开;",
    "eə": "/e/重读,/ə/轻读,舌端抵下齿,双唇半开;",
    "uə": "/u/重读,/ə/轻读,双唇由收圆到半开;",
    "p": "坡;紧闭双唇,然后让气流突然冲出,吹动嘴前纸片;双唇紧闭,然后快速张开,让气流冲出口腔,发出爆破音,但声带不振动;",
    "b": "波;发音动作与清辅音/p/类似,但是声带要震动,不得吹动嘴前纸片;双唇紧闭,然后快速张开,让气流冲出口腔,发出爆破音,但声带需振动;",
    "t": "特;舌端放于上齿龈,然后让气流突然冲出,吹动嘴前纸片;舌尖抵上齿龈,憋住气,然后突然弹开舌尖,让气流从口腔喷出,但声带不振动;",
    "d": "的;发音动作与清辅音/t/类似,但是声带要震动,不得吹动嘴前纸片;舌尖抵上齿龈,憋住气,然后弹开舌尖,让气流从口腔中喷出,但声带需振动;",
    "k": "科;舌根紧贴软腭,然后让气流突然冲出,吹动嘴前纸片;在/s/音后读其对应的浊辅音/g/;舌后部抵住软腭,憋住气,然后突然间离开,将气送出来,想咳嗽一样,但声带不震动;",
    "ɡ": "割;舌后部抵住软腭,憋住气,然后突然间离开,将气送出来,但声带需振动;",
    "s": "丝;舌尖靠近上齿龈(不得接触),然后将气流从舌尖和上齿龈之间泄出;双唇微微张开,舌头自然放松,气流从上下齿隙间送出,但声带不振动;",
    "z": "双唇微微张开,舌头自然放松,气流从上下齿隙间送出,但声带需振动;",
    "ʃ": "狮;舌身抬起靠近硬腭,舌端靠近上齿龈,形成狭长通道,然后双唇稍微收圆并突出,最后让气流通过;双唇收圆并稍微突出,舌尖接近上齿龈,送气,声带不振动;",
    "ʒ": "/ʒə/,/-热/;双唇收圆并稍微突出,舌头稍微上卷,舌尖接近上齿龈,送气,但声带需振动;",
    "tʃ": "吃;舌端贴住上齿龈,然后让口形略成方形,最后让气流摩擦成音;双唇略微张开突出,舌尖抵住上齿龈,用力吐气,声带不振动;",
    "dʒ": "枝,/dʒ/,/遮/;双唇略微张开突出,舌尖抵住上齿龈,用力吐气,但声带需振动;",
    "f": "夫;上齿轻触下唇,然后将气流从唇齿之间的空隙吹出,引起摩擦成音,但声带不振动;",
    "v": "上齿轻轻接触下唇,然后吹气,让气流从唇齿间通过,形成摩擦,但声带需振动;",
    "θ": "丝-咬舌;舌尖轻触上齿背部,然后让气流从舌齿间的缝隙送出;舌尖微微伸出,上下齿轻轻咬住舌尖,送气,但声带不振动;",
    "ð": "上下齿轻轻咬住舌尖,送气,但声带需振动;",
    "ts": "刺;舌尖先抵住上齿,堵住气流,使气流从舌尖和齿龈间送出,声带不振动;",
    "dz": "舌尖先抵住上齿,堵住气流,使气流从舌尖和齿龈间送出;",
    "tr": "戳;双唇收圆向前突出,舌尖上翘抵住上齿龈,采取伐/r/的姿势,声带不振动;",
    "dr": "双唇收圆向前突出,舌尖上翘抵住上齿龈,采取伐/r/的姿势,但声带振动;",
    "h": "呵;口微微张开,然后让气流不受阻塞的流出;嘴唇自然张开,自然呵气,声带不振动;",
    "r": "舌尖向上卷起,舌头不要接触任何部位,双唇稍微突出,声带振动;",
    "l": "舌尖抵住上齿龈,舌尖轻微用力弯曲,气流从舌的旁边送出;",
    "m": "双唇紧闭,舌头平放,气流从鼻腔送出,声带振动;",
    "n": "双唇微开,舌尖抵上齿龈,气流从鼻孔里出来,声带振动;",
    "ŋ": "双唇张开,舌尖抵上齿龈,气流从鼻腔送出,声带振动;",
    "w": "双唇缩小并向前突出,舌后部抬起,嘴慢慢向两边滑开;",
    "j": "嘴形成微笑状,舌尖抵住下齿,舌面贴住上颚,声带需振动;",
}

#####################################################################################
#####################################################################################

# Number=[str(i) for i in range(10)]
# Alphabet=[chr(i) for i in range(ord('A'), ord('Z') + 1)]
# Number_Alphabet = Number + Alphabet


# def kpuz(symbols):
#     """一个或多个36进制符号与其索引之间的转化;36以内,索引值等于进制符所对应的十进制数字."""
#     symbols2=[]
#     for i in symbols.split(' '):
#         try:    symbols2.append(Number_Alphabet[int(i)])
#         except: symbols2.append(str(Number_Alphabet.index(i.upper())))

#     return " ".join(symbols2)

# # url
# # https://apps.timwhitlock.info/emoji/tables/unicode

# args_kwargs(0,1,2,3,k1=4,k2=5)

#

