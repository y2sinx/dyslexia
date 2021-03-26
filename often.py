
import os,re
import codecs
from dyslexia.common import encoding_type

from dyslexia import NEEDED_PATH
from dyslexia.youdao import yd_dict 
from dyslexia.word_net import wn_dict
from dyslexia.english import WordSet, get_words_in_ht, my_tokenize, get_raw_string
from dyslexia.dt_magic import DysLexia_Ht,make_wl 

from dyslexia.ht import line_sorted, union

def pattern_rename(root, head, pat="S\d{2}E\d{2}"):
    """文件名批量命名"""
    root = os.path.abspath(root)
    for old_name in os.listdir(root):
        try:
            mid = re.findall(pat, old_name, re.IGNORECASE)[0]

            end = old_name.split(".")[-1]
            new_name = head + " - " + mid + "." + end
            os.rename(root + "/" + old_name, root + "/" + new_name)
        except:
            print(old_name)

def _utf_8(fn):
    """将文件fn修正为utf-8编码"""
    old = encoding_type(fn)["encoding"]
    if old=="GB2312": old="gbk"

    if old.lower() != "utf-8":
        with codecs.open(fn, mode="r", encoding=old) as f_in:
            content = f_in.read()
            f_out = codecs.open(fn, "w", "utf-8")
            f_out.write(content)
            f_out.close

def utf_8(root):
    """将目录root下的所有文件修正为utf-8编码"""
    for root, _, files in os.walk(root):
        for file in files:
            path = os.path.join(root, file)
            try:
                _utf_8(path)
            except:
                print("X: " + file)

def token_clean(tokens):
    """排除不合适的单词"""
    bad=[]
    for i in tokens:
        if len(i) < 2:
            bad.append(i)             
        elif not i[0].isalpha(): # 非常必要,否则会出现"\202dlike"等字符,导致unf_words无法排除单词like,make_wl不会在Dys词典中查like.
            bad.append(i)             
        elif i[0]=="-" or i[0]=="\\":
            bad.append(i)             
        elif i[-1]=="-" or i[-1]=="⋅":
            bad.append(i)             
        elif i[-2:]=="\\n":
            bad.append(i)             
        else:
            pass
    
    return sorted(set(tokens).difference(set(bad)))

def unf_words(root, words_familiar="words_familiar.txt", words_none="words_none.txt"):
    """打印一目录下所有文章中不熟悉的单词"""
    
    if os.path.isfile(root):
        raw=get_raw_string(root)
    
    else: 
        raw=""
        for root, _, files in os.walk(root):
            for file in files:
                path = os.path.join(root, file)
                try:
                    raw = raw + " " + get_raw_string(path)
                except:
                    print("X: " + file)        
    
    
    tokens=[word.lower() for word in my_tokenize(raw)]
    wd = WordSet(token_clean(tokens))

    wd.discard(get_words_in_ht(NEEDED_PATH[words_familiar]))
    wd.discard(get_words_in_ht(NEEDED_PATH[words_none]))
    
    return sorted(wd.t)


