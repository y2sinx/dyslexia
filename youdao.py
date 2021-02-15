import requests
from bs4 import BeautifulSoup
from dyslexia import common

A_PAIRS = [
    ("[", "/"),
    ("]", "/"),
]

BASIC_PAIRS = [
    ("\n", " "),
    ("[", "<"),
    ("]", ">"),
    ("(", "<"),
    (")", ">"),  ##以上必须在上面
    (" n. ", "[n]"),
    (" v. ", "[v]"),
    (" vt. ", "[vt]"),
    (" vi. ", "[vi]"),
    (" adj. ", "[a]"),
    (" adv. ", "[ad]"),
    (" pron. ", "[pron]"),
    (" prep. ", "[prep]"),
    (" abbr. ", "[abbr]"),
    (" conj. ", "[conj]"),
    (" det. ", "[det]"),
    (" phr. ", "[phr]"),
    (" int. ", "[int]"),
    (" num. ", "[num]"),
    ("的复数", "的pl"),
    ("的过去式和过去分词", "的pt和pp"),
    ("的过去式", "的pt"),
    ("的过去分词", "的pp"),
    ("的现在分词", "的pr"),
    ("的第三人称单数", "的s3"),
    ("的单三形式","的s3"),
    ("的ing形式", "的pr"),
    ("的三单形式","的s3"),
    (" 的", "的"),
    ("......", "..."),
    ("> ", ">"),
    (";[", "; ["),
    ("<等于 ","<等于"),
    ("<非正式>",""),
]

PLUS_PAIRS = [
    ("复数/", "pl,"),
    ("过去式/", "pt,"),
    ("过去分词/", "pp,"),
    ("现在分词/", "pr,"),
    ("第三人称单数/", "s3,"),
    ("比较级/", "er,"),
    ("最高级/", "est,"),
]


def sequence_replace(line, pairs):
    """替换行中的一系列子串"""
    try:
        for pair in pairs:
            line = line.replace(pair[0], pair[1])
    except:
        print("Check `pairs` again!")
    return line


def yd_dict(target):
    """可在jupyter中工作的简易有道词典;"""

    url = "http://dict.youdao.com/w/eng/%s/#keyfrom=dict2.index" % target
    r = requests.get(url=url)
    soup = BeautifulSoup(r.text, "lxml")

    ah = "[-]"
    try:  ##音标
        a = soup.find(class_="phonetic").string  # 第一个标签是英文的
        a = ah + sequence_replace(a, A_PAIRS)
    except:
        a = ah + "None"

    bh = " "
    try:  ##基本释义
        basic = soup.find(class_="trans-container").find("ul")
        basic = "; ".join([string for string in basic.stripped_strings])
        basic = bh + common.punctuator(basic)
        basic = sequence_replace(basic, BASIC_PAIRS)  ##

        if "[" not in basic:  ##为了统一输出,basic必须含有'[]'
            basic = "[x]" + basic.strip()
    except:
        basic = "[x]None"

    try:  ##单词变形
        plus = soup.find(class_="additional").string
        plus = plus.replace(" ", "")
        plus = plus[2:-2]
        add = plus.split("\n")
        plus = "[+]"
        for i, j in zip(add[0::2], add[1::2]):
            plus = plus + i + "/" + j + ";"
        if plus[-1] == ";":
            plus = plus[:-1]
        plus = sequence_replace(plus, PLUS_PAIRS)

        if plus == "[+]":  ##将[+];变为[+]None
            plus = ""
    except:
        plus = ""
    if plus=="":
        line = "{} % {}; {};".format(target, a, basic)
    else:
        line = "{} % {}; {}; {};".format(target, a, basic, plus)
    return line


def make_ht(words, file=common.UNF_TXT, trigger=10):
    """使用yd_dict创建单词表;bigtan中单词的主要由来;"""
    words = sorted(words)

    with open(file, "w", encoding="utf-8") as fp:
        print()
        for i, word in enumerate(words):
            line = yd_dict(word) + "\n"
            fp.write(line)
            common.progress_bar(i + 1, len(words), word, trigger=trigger)
    return file

# 保不保留大写字母: 不保留,因为大小写含义有的会重复,保留,便于看出是否是专有名词
# 以..为基准,有道?
# 要包含多少词汇,

# # 为word_new添加音标
# def get_word_accent(target, flag_soup=False, sep='%'):
#     '''获取单词的音标;'''
#     if target == '':
#         return '不能为空串!'

#     url= 'http://dict.youdao.com/w/eng/%s/#keyfrom=dict2.index' % target
#     r = requests.get(url=url)
#     soup = BeautifulSoup(r.text, 'lxml')

#     try:
#         a = soup.find(class_='phonetic').string  # 第一个标签是英文的
#         a = '[-]' + sequence_replace(a, [('[', '/'), (']', '/')])
#     except:
#         a = '[-]#'

#     accent = '{};'.format(a)
#     return accent


# with open('F:/Git/bigtan/word.ht','r',encoding='utf-8') as fp:
#     lines=fp.readlines()

# needs=[ line for line in lines if '[-]' not in line]#需要添加音标的行
## 保存
# def ht_plus_accent(needs, file):
#     '''将需要更给的行,修改后放到文件file.
#         needs: 需要更改的行.'''
#     with open(file, 'w', encoding='utf-8') as fp:
#         for i, line in enumerate(needs):
#             word, tail = split_line(line)
#             acc = get_word_accent(word)
#             line = word + ' % ' + acc + ' ' + tail
#             progress_bar(i + 1, 56460, word, trigger=100)
#             fp.write(line + '\n')
#     return file


# def find_repeated_heads(file, sep='%'):
#     '''找出有重复head'''
#     heads = []
#     with open(file, 'r', encoding='utf-8') as fp:
#         for line in fp:
#             head = split_line(line, sep=sep)[0]
#             heads.append(head)
#     dn = defaultdict(int)
#     for head in heads:
#         dn[head] = dn[head] + 1
#     out = []
#     for k, v in dn.items():
#         if v > 1:
#             out.append((k, v))
#     return sorted(out)


# make_block_adding(needs[10000:20000],file='1-2w.add')

# 为某个文件中的单词添加音标
# with open('F:/Git/bigtan/word.ht','r',encoding='utf-8') as fp:
#     for i,line in enumerate(fp):
#         if i>=71750:
#             if '[-]' not in line:
#                 word,tail=split_line(line)
#                 acc=get_word_accent(word)
#                 line=word+' % '+acc+' '+tail
#                 lines.append(line)
#                 endtime = datetime.datetime.now()
#                 delta=endtime-starttime
#                 progress_bar(i+1,400000,word+'  '+str(delta.min),trigger=10)
#             else:
#                 lines.append(line.strip('\n'))

#         else:
#             lines.append(line.strip('\n'))
# with open('F:/Git/bigtan/words.add','w',encoding='utf-8') as fp:
#     for line in lines:
#         line=line+'\n'
#         fp.write(line)
#####################################################################

##########################################################################
# def youdaoapi(raw="bear", en2cn=True, sentence=True):
#     import urllib.parse
#     import http.client
#     import random
#     import hashlib

#     appKey = "7603a3147bc8dc8e"
#     secretKey = "XgYNddZy9Qk1IjpVf2oqV22XHTw5744g"
#     # appKey = '093265eac11c375b'
#     # secretKey = 'OC4Yy0dfOxEyeClZuYVFg9l3WDRojQWk'

#     httpClient = None
#     myurl = "/api"
#     q = raw
#     if en2cn == True:
#         fromLang = "EN"
#         toLang = "zh-CHS"
#     else:
#         fromLang = "zh-CHS"
#         toLang = "EN"
#     salt = random.randint(1, 65536)
#     sign = appKey + q + str(salt) + secretKey
#     m1 = hashlib.new("md5")
#     m1.update(sign.encode("utf-8"))
#     sign = m1.hexdigest()
#     myurl = (
#         myurl
#         + "?appKey="
#         + appKey
#         + "&q="
#         + urllib.parse.quote(q)
#         + "&from="
#         + fromLang
#         + "&to="
#         + toLang
#         + "&salt="
#         + str(salt)
#         + "&sign="
#         + sign
#     )

#     try:
#         httpClient = http.client.HTTPConnection("openapi.youdao.com")
#         httpClient.request("GET", myurl)
#         # response是HTTPResponse对象
#         response = httpClient.getresponse()
#         youdao_dict = eval(response.read().decode("utf-8"))
#         # 输出想要的信息
#         if sentence == True:
#             print(youdao_dict["translation"][0])
#         else:
#             print(" /%s/ ".center(45, "=") % youdao["basic"]["phonetic"])
#             for i in youdao_dict["basic"]["explains"]:
#                 print(punctuator(i))
#     except Exception as e:
#         print(e)
#     finally:
#         if httpClient:
#             httpClient.close()
# # 之前记得有过,难道是在实验室的电脑?

