import re
import os
import json
import pickle
import difflib
from fnmatch import fnmatchcase
from dyslexia import common
from dyslexia.youdao import yd_dict
from dyslexia import ht
from collections import defaultdict


################################################################
# 普通常量
################################################################
import string

MARK_WIDTH = 32
PUNCTUATION = list(" " + string.punctuation)  ##把空格也当成一个标点
PUNCTUATION_IN_WORD = "_-'"  ##可以在单词中存在的标点
PUNCTUATION_NOT_IN_WORD = [
    p for p in PUNCTUATION if p not in PUNCTUATION_IN_WORD
]  ##不可以在单词当中存在的标点
ENGLISH_LETTERS = list(string.ascii_letters)  ##英文字母

################################################################
## EnDict
################################################################


def similarity(s1, s2):
    """计算两个字符串的相似度"""
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


class EnDict:
    """将ht文件转化为Python字典."""

    def __init__(self, file=None, sep="%", check_tag=False):
        """初始化."""
        self._base = {}
        if file != None:  ##导入文件中的单词
            self._base = self.load(file, sep)._base

    def update(self, dn):
        """通过字典载入."""
        self._base.update(dn)
        return self

    def load(self, file, sep="%", check_tag=False):
        """载入ht文件中的单词."""

        dn = ht.ht_to_dict(file, sep, check_tag)
        print("EnDict # {:4d} # {}!".format(len(dn), file))
        self.update(dn)

        return self  ##为了使用`EnDict().load()``

    def loads(self, dir_path, level=2):
        """载入目录(dir_path)下级别<=level的词表;"""
        files = sorted(os.listdir(dir_path)[:level], reverse=True)
        for file in files:
            self = self.load(file=dir_path + file)
        return self

    def clear(self):
        """清空字典."""
        self._base = {}
        print("当前词典已被清空!")

    def get_length(self):
        """获取单词列表的长度"""
        return len(self._base)

    def get_list(self):
        """获取单词列表."""
        return list(self._base.keys())

    def get_set(self):
        """获取单词集合."""
        return set(self._base.keys())

    def get_dict(self):
        """获取词典."""
        return self._base

    l = property(get_length)
    t = property(get_list)
    s = property(get_set)
    d = property(get_dict)

    def tags(self, word):
        """查看该单词有哪些标签."""
        return list(self._base[word].keys()) if self.is_included(word) else []

    def have_tag(self, word, tag):
        """判断某个单词是否有某个tag."""
        return tag in self.tags(word)

    ## 对于大文件特别慢????
    def get_comments(self):
        """获取字典中的所有注释(目录);字典的长度需小于1万"""
        out = []
        for wd in self.t:
            if self.have_tag(wd, "#"):
                out.append(wd)
        return out

    def match(self, matcher):
        """使用unix通配符(`*`, `?`, `[seq]`, `[!seq]`)匹配字典中的单词;"""
        return [wd for wd in self.t if fnmatchcase(wd, matcher)]

    def make_wordlist(self, words, file=common.UNF_TXT):
        """使用 dyslexia 创建单词表;"""
        with open(file, "w", encoding="utf-8") as fp:
            for i, word in enumerate(words):
                common.progress_bar(i + 1, len(words), word, trigger=10)
                line = self.lookup_fz(word)
                fp.write(line + "\n")
        return file

    def similar(self, word, ratio=0.9):
        """根据字符串的相似程度(ratio)查找近似单词;"""
        out = [wd for wd in self.t if similarity(wd, word) >= ratio]
        return out

    def is_included(self, word):
        """查看当前词典是否包含该单词"""

        return True if word in self.t else False

    def lookup(self, word):
        """只在当前词典中查找单词的含义;"""

        return self.to_line(word) if self.is_included(word) else "NOT INCLUDE!"

    def lookup_fz(self, word):
        """在字典中查找单词的含义;若无是由有道查; 添加一个缓存文件"""
        
        if self.is_included(word):
            out = self.to_line(word)
        else:
            out = yd_dict(word) + " $$->BF"
        return out

    def to_line(self, word, sep="%"):
        """将self._base的一个键值对转化为一个字符串;"""

        if self.have_tag("#", word) or self.have_tag("0", word):
            line = word + "\n"  ##注释行或纯单词行
        else:  ##需分裂重组的单词行
            line = "{} {} ".format(word, sep)
            for tag in self.d[word].keys():
                values_string = ";".join(self.d[word][tag])
                line = line + "[{}]{}; ".format(tag, values_string)
            line = line.strip() + "\n"  ##末尾的空格
        return line

    def to_ht(self, file, words=None, trigger=1000, sep="%"):
        """将字典保存为文本文件"""
        if self.l > 10000:
            return "字典长度超过10000,请使用`to_ht_big()`."

        if words == None:
            words = self.t

        l = len(words)
        with open(file, "w", encoding="utf-8") as fp:
            for i, word in enumerate(words):
                fp.write(self.to_line(word, sep))
                common.progress_bar(i + 1, l, word, trigger)

        return file

    def get_sub_en(self, words):
        """根据子字典的键(sk)截取子字典."""
        en = EnDict()
        dn = dict([(wd, self.d[wd]) for wd in words])
        en.d.update(dn)
        return en

    def to_ht_big(self, file, words=None, chunk=1000, trigger=1, sep="%"):
        """将字典保存为文本文件"""

        if words == None:
            words = self.t
        chunksize = self.l // chunk
        with open(file, "w", encoding="utf-8"):
            pass

        for i in range(chunk + 1):
            wds = words[i * chunksize : (i + 1) * chunksize]
            en = self.get_sub_en(wds)
            file2 = file + ".mid"
            en.to_ht(file2, trigger=0)
            union(file, file2, overwrite=True)
            common.progress_bar(i + 1, chunk + 1, file, trigger)

    def to_josn(self, file):
        """将词典保存为Json文件"""
        with open(file, "w", encoding="utf-8") as fp:
            json.dump(self._base, fp, ensure_ascii=False, indent=2)
        return file

    def load_json(self, file):
        """将Json文件导入到词典,其处理速度比Txt文件更快."""
        dn = common.json_to_dict(file)  # 并不是十分有效,有时json文件并不是一个字典??
        print("EnDict # {:4d} # {}!".format(len(dn), file))
        self.update(dn)
        return self

    def to_pickle(self, file):
        """将词典保存为pickle文件"""
        with open(file, "wb") as fp:
            pickle.dump(self, fp)  # 将字典保存为pkl文件
        return file


########################################################################
## 以下用于分析单词
########################################################################


def get_raw_string(file):
    """获取文件的原始字符串."""
    with open(file, "r", encoding="utf-8") as f:
        raw = f.read()
    return common.punctuator(raw)

def my_tokenize(raw):
    """输出字符串中的所有有效单词."""

    raw = re.sub("[\u4e00-\u9fa5]+", " ", raw)  # 删除所有中文字符
    raw = re.sub("[0-9]+", " ", raw)  # 删除所有的数字
    raw = re.sub("-{2,}"," ",raw) ## "a--b" -> "a b"
    raw = re.sub('[!"#$%&\()*+,./:;<=>?@[\\]^`{|}~—\'\n⋅]', ' ', raw)  ## 待替换的标点要放在[]内

    tokens = set( re.split("\s+", raw) )
    return list(tokens)

from collections import defaultdict
from dyslexia.english import similarity
from dyslexia import ht


def get_words_in_ht(file, sep="%"):
    """获取ht文件中的单词."""
    words = []
    with open(file, "r", encoding="utf-8") as fp:
        for line in fp:
            head, _ = ht.split_line(line, sep=sep)
            if head.strip() != "" and head[0].isalpha():
                words.append(head.strip())
    return words


########################################################################
## 需要舍弃的单词(基本的)
########################################################################
def capitalize(words, initial_only=True):
    """首字母或全字母大写化."""
    return (
        [string.capwords(wd) for wd in words]
        if initial_only
        else [wd.upper() for wd in words]
    )


from nltk.corpus import stopwords, swadesh, words

DISCARD_WORDS = (
    stopwords.words("english")
    + swadesh.words("en")
    + words.words("en-basic")
    + ["bark", "know"]
)

PUNCTUATION = list(" " + string.punctuation)  ##把空格也当成一个标点
PUNCTUATION_IN_WORD = "_-'"  ##可以在单词中存在的标点
PUNCTUATION_NOT_IN_WORD = [
    p for p in PUNCTUATION if p not in PUNCTUATION_IN_WORD
]  ##不可以在单词当中存在的标点
ENGLISH_LETTERS = list(string.ascii_letters)  ##英文字母


class WordSet:
    """词集分析器"""

    def punctuation_warning(self, puncts=PUNCTUATION_NOT_IN_WORD):
        """返回词集中第一个单词不该包含的标点."""
        for word in self._base:
            if word.isalpha() == True:
                for c in word:
                    if c in puncts:
                        return "##PUNCTUATION-WARNING##: {} ##".format(repr(word))

    def __init__(self, words):
        """往结构中继续添加单词."""
        self._base = set(words)  # 将单词列表表示为集合
        warning = self.punctuation_warning()
        if warning != None:
            print(warning + "\n")

    def update(self, words):
        """往结构中添加单词."""
        self._base.update(words)
        print(self.l)

    def clear(self):
        """清空集合."""
        self._base = set()
        print("当前集合已被清空!")

    def get_length(self):
        """获取单词列表的长度"""
        return len(self._base)

    def get_list(self):
        """获取单词列表."""
        return list(self._base)

    def get_set(self):
        """获取单词集合."""
        return set(self._base)

    l = property(get_length)
    t = property(get_list)
    s = property(get_set)

    def discard(self, words=DISCARD_WORDS):
        """删除集合中的的元素."""
        words = words + capitalize(words)
        for word in words:
            self._base.discard(word)
        return self.t

    def pick_by_width(self, width):
        """根据单词的长度进行选词."""
        return sorted([wd for wd in self.t if len(wd) == width])

    def get_width_dict(self):
        """获取字长字典."""
        out = {}
        dn = defaultdict(list)
        for wd in self.t:
            dn[len(wd)].append(wd)
        keys = sorted(dn.keys(), key=lambda x: int(x))
        for k in keys:
            out[k] = dn[k]
        return out

    #     width_dict=property(get_width_dict)

    def pick_by_initial(self, initial="a", include_upper=False):
        """根据首字母选词."""
        if include_upper:
            out = [wd for wd in self.t if wd[0].upper() == initial.upper()]
        else:
            out = [wd for wd in self.t if wd[0] == initial]
        return out

    def get_initial_dict(self):
        """获取首字母字典"""
        dn = defaultdict(list)
        for wd in self.t:
            dn[wd[0]].append(wd)
        return dict(dn)

    def have_element(self, elem):
        """判断是否有某个元素."""
        return True if elem in self._base else False

    def pick_by_similar(self, wrong_word, ratio=0.9):
        """查找某个单词的形似词,拼写错误也会有返回值. ratio:近似程度.
        """
        similar_words = [
            word for word in self.t if similarity(wrong_word, word) >= ratio
        ]
        if len(similar_words) > 0:
            return similar_words
        else:
            return []

    def pick_by_punctuation(self, p="-"):
        """根据标点选词."""
        out = [wd for wd in self._base if not wd.isalpha() if p in wd]
        return out

    def get_punctuation_dict(self, puncts=PUNCTUATION):
        """获取标点字典."""
        dn = defaultdict(list)
        with_punct = [wd for wd in self._base if not wd.isalpha()]
        for wd in with_punct:
            for p in puncts:
                if p in wd:
                    dn[p].append(wd)
        return dict(dn)

    def get_not_words(self, puncts=PUNCTUATION_NOT_IN_WORD):
        "获取集合中不是单词的元素."
        out = []
        dn = self.get_punctuation_dict()
        for p in puncts:
            if p in dn.keys():
                out = out + dn[p]
        return sorted(set(out))

    def to_ht(self, file="my_words.txt"):
        """写入一个纯单词文本"""
        lines = sorted([wd + "\n" for wd in self.t])
        with open(file, "w", encoding="utf-8") as fp:
            fp.writelines(lines)
        return file


####################################################################
# 如何区分单词和短语
####################################################################

#     def get_words2(self):
#         """获取单词"""
#         return sorted(set(self._base).difference(set(self.get_not_words())))

#     # def get_words(self,puncts=["_","-","'"],):
#     #     """获取集合中的单词."""
#     #     out = [wd for wd in self._base if wd.isalpha()] #没有标点
#     #     with_punct=
#     #     for wd in with_punct:
#     #         if wd in []

#     #     dn = self.get_punctuation_dict()
#     #     for p in puncts:
#     #         if p in dn.keys() p not in puncts_phrase:
#     #             out=out+dn[p]

#     #     return sorted(set(out))

#     def get_phrase(self, puncts=[" ", ".", "(", ")"]):
#         "获取集合中的短语."
#         out = []
#         dn = self.get_punctuation_dict()
#         for p in puncts:
#             if p in dn.keys():
#                 out = out + dn[p]
#         return sorted(set(out))

####################################################################
# 词形变化
####################################################################

#     def lemmatization(self, translator="morphy"):
#         """使用某个翻译器对所有词进行词性还原."""
#         pass
#         # return out,pairs

#     def morphy(self):
#         """对每个单词进行wordnet.morphy处理.
#         pairs: 还原对.
#         out: 新的的词列表.
#         """
#         out = []
#         pairs = []
#         for wd in words:
#             form = wd.lower()  # 首先将其小写化
#             etymon = wordnet.morphy(form)
#             if etymon != None and etymon != form:
#                 pairs.append((wd, etymon))  # 有效对
#             else:
#                 pass  # 不保存无效对
#             if etymon == None:
#                 out.append(wd)
#             else:
#                 out.append(etymon)  # 有原形的大写单词同时被转换成了小写
#         # pairs: 是morphy_fz查找出的有效转换对.out:按有效转换对原始词列表进行替换,此后可能出现多个单词对应同一个原形的情况
#         return out, pairs


#################################################################
# 语音识别库Sphinx: https://www.cnblogs.com/zhe-hello/p/13273523.html
#################################################################

# # $you_get SOME_URL
# # from ddpie.dyslexia import english
# # tv=english.TvShow()
# # tv.to_audio_from_video("Y:/Git/BIGTAN-U/brave_new_world.mp4",'.wav')

# import speech_recognition as sr
# def wav_to_txt(path):
#     """将宣传片中的语音转化为字幕(wav)."""
#     r = sr.Recognizer() ##创建一个识别实例
#     audio=sr.AudioFile(path) ##创建一个音频实例

#     with audio as source:  ##提取音频中的目标片段
#         data = r.record(source)

# #     out=r.recognize_houndify(data,
# #                              client_id="wSrGiCLOkMh8b-yisOTkiQ==",
# #                              client_key="htIasxejUP5kwfxgHGU6NqSsJbaKuZ2Ro_N61aNYtpD6lB78VoZzLmgLRwgWpIJ6bZIsLEt4qQUaumRPCVCFpA==")
#     out=r.recognize_sphinx(data)
#     return out

# wav_to_txt("Y:/Git/BIGTAN-U/brave_new_world.wav")


from dyslexia.ht import union
from dyslexia import NEEDED_PATH

if __name__ == "__main__":
    en = EnDict()
    # en=EnDict(NEEDED_PATH['01_zhongkao_bcz.ht']).loads("F:/Git/data/basic/")
    # en=en.loads('Y:/Git/dyslexia/basic/',level=5)
    ## en.load(NEEDED_PATH['dt_words.ht'])
    # en.to_ht_big('test.ht')
    ## 与词典的大小有关而与单词列表的长度无关
