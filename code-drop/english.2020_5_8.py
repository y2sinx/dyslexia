# -*- coding: utf-8 -*-
import re, os, json, requests, difflib, pyperclip
from bs4 import BeautifulSoup
from fnmatch import fnmatchcase
from nltk.corpus import words,wordnet
from moviepy.editor import VideoFileClip
from ddpie import common
import pickle
from ddpie import fix

######################################################################################
# 普通常量
######################################################################################
# 字符串常量
import string
PUNCTUATION = list(' '+string.punctuation) #把空格也当成一个标点
PUNCTUATION_IN_WORD="_-'" #可以在单词中存在的标点
PUNCTUATION_NOT_IN_WORD =[p for p in PUNCTUATION if p not in PUNCTUATION_IN_WORD]#不可以在单词当中存在的标点
ENGLISH_LETTERS=list(string.ascii_letters)


OLD_NEW=[('复数/', 'pl/'),
         ('过去式/', 'pt/'),
         ('过去分词/', 'pp/'),
         ('现在分词/', 'pr/'),
         ('第三人称单数/', 's3/'),
         ('比较级/', 'er/'),
         ('最高级/', 'est/'),
         (' n. ', '[n]'),
         (' v. ', '[v]'),
         (' vt. ', '[vt]'),
         (' vi. ', '[vi]'),
         (' adj. ', '[a]'),
         (' adv. ', '[ad]'),
         (' pron. ', '[pron]'),
         (' prep. ', '[prep]'),
         (' abbr. ', '[abbr]'),
         (' conj. ', '[conj]'),
         (' det. ', '[det]'),
         (' phr. ', '[phr]'),
         (' int. ', '[int]'),]

PAIRS_DICT_TO_LINE={
    ( "': ['" ,    "]" ), #标签及其值的连接处: ': ['
    ( "'], '"  ,  "; [" ),#上个标签的值与下一个标签的连接处: ], '
    ( "', '"  ,    ";" ), #标签内部各个值的连接处: ', '
    ("{'"    ,     "["),  #整个字典的头: {'
    ( "']}"       , ";") #整个字典的尾; ']}
                        }

def sequence_replace(line,pairs):
    """替换行中的一系列元素"""
    try:
        for pair in pairs: 
            line=line.replace(pair[0],pair[1])
    except: 
        print("Check `pairs` again!")
    return line

def synset_fz(word='synonym', num=2):
    """wordnet: 查看单词的同义词集,定义,例句,反义词;"""
    groups=wordnet.synsets(word)
    if len(groups)==0: return 0
    for i, group in enumerate(groups):
        if i < num:
            Def=group.definition()
            ex=group.examples()
            synonyms=group.lemma_names()
            #############################           
            antonyms=[]
            for lm in group.lemmas():
                if lm.antonyms():
                    for l in lm.antonyms():
                        antonyms.append(l.name())
            #############################           
            print("#{}<{}>".format(i+1,group.name()))
            print("-"*32)
            print("<words>: {}".format(",".join(synonyms))) 
            print("<def>: {}".format(Def)) 
            print("<ex>: {}".format('; '.join(ex))) 
            print("<antonyms>: {}".format(",".join(antonyms)))
            print()

from googletrans import Translator
def ggtrans(raw, en2zh=True):
    """使用googletrans将英文翻译成中文或者将中文翻译成英文(en2zh=False)"""
    translator=Translator(service_urls=["translate.google.cn"])
    if en2zh: text=translator.translate(raw,src="en",dest="zh-cn").text
    else: text=translator.translate(raw,src="zh-cn",dest="en").text
    return common.punctuator(text)

#####################################################################
# 为word_new添加音标
import datetime
def get_word_accent(tt,flag_soup=False,sep='%'):
    """获取单词的音标;"""
    if tt=="": return "不能为空串!"
    
    url_yd='http://dict.youdao.com/w/eng/%s/#keyfrom=dict2.index' % tt
    r = requests.get(url=url_yd)
    soup = BeautifulSoup(r.text, "lxml")        

    try:            
        a=soup.find(class_="phonetic").string #第一个标签是英文的
        a='[-]'+sequence_replace(a,[('[','/'),(']','/')])
    except Exception as e:
        a='[-]#'
    
    accent = "{};".format(a)
    return accent

# with open('F:/Git/bigtan/word.ht','r',encoding='utf-8') as fp:
#     lines=fp.readlines()
    
# needs=[ line for line in lines if "[-]" not in line]#需要添加音标的行
## 保存
def ht_plus_accent(needs,file):
    """将需要更给的行,修改后放到文件file.
        needs: 需要更改的行."""
    with open(file,'w',encoding='utf-8') as fp:
        for i,line in enumerate(needs):
            word,tail=split_line(line)
            acc=get_word_accent(word)
            line=word+' % '+acc+' '+tail
            progress_bar(i+1,56460,word,trigger=100)        
            fp.write(line+'\n')
    return file


def find_repeated_heads(file,sep='%'):
    """找出有重复head"""
    heads=[]
    with open(file,'r',encoding='utf-8') as fp:
        for line in fp:
            head=split_line(line,sep=sep)[0]
            heads.append(head)
    dn=defaultdict(int)
    for head in heads:
        dn[head]=dn[head]+1
    out=[]
    for k,v in dn.items():
        if v>1:
            out.append((k,v))  
    return sorted(out)
    
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


def yd_dict(tt,flag_soup=False,sep='%'):
    """可在jupyter中工作的简易有道词典;"""
    if tt=="": return "不能为空串!"
    
    url_yd='http://dict.youdao.com/w/eng/%s/#keyfrom=dict2.index' % tt
    r = requests.get(url=url_yd)
    soup = BeautifulSoup(r.text, "lxml")        

    if flag_soup:
        file="{}.html".format(tt)
        common.print_save(soup,file)
        print(file)
    
    try:            
        a=soup.find(class_="phonetic").string #第一个标签是英文的
        a='[-]'+sequence_replace(a,[('[','/'),(']','/')])
    except Exception as e:
        a='[-]#ERROR#'
    
    try:
        basic=soup.find(class_='trans-container').find('ul')
        basic="; ".join([string for string in basic.stripped_strings])
        basic=" "+common.punctuator(basic)
        basic = sequence_replace(basic,[('[','<'),(']','>')]) #将科目标签[]变为<>
        basic=sequence_replace(basic,OLD_NEW) #n.-> [n]等
    except Exception as e:
        basic='[x]#ERROR#'
        
    try:
        plus = soup.find(class_="additional").string
        plus=plus.replace(' ','')
        plus=plus[2:-2]
        add=plus.split('\n')
        plus = '[+]'
        for i,j in zip(add[0::2],add[1::2]): 
            plus = plus+i+'/'+j+','
        if plus[-1]==',': plus=plus[:-1]
        plus=sequence_replace(plus,OLD_NEW)
    except Exception as e:
        plus='[+]#ERROR#'        

    line = "{} {} {}; {}; {}; {}".format(tt,sep,a,basic,plus,'[^]yd;')
    return line  #查询失败时的输出: 'sinx: [-]#ERROR#; [x]#ERROR#; [+]#ERROR#; [^]yd;'

def make_wordlist_from_youdao(words,file,trigger=10):
    """使用yd_dict创建单词表;bigtan中单词的主要由来;"""
    length=len(words)
    words=sorted(words)
    with open(file,'w',encoding='utf-8') as fp:
        for i,word in enumerate(words):
            line=yd_dict(word)
            line=line+'\n'
            fp.write(line)
            common.progress_bar(i+1,len(words),word,trigger=trigger)
    return file

def have_repeated_tags(line):
    """如果词性标记相同,给出警告信息!"""
    fa=re.findall("\[\w+\]",line)
    length=len(fa)
    length_set=len(set(fa))
    if length_set!=length:
        head,_=split_line(line)
        print("Warning: {} have repeated tags.".format(head))
        return True
    else:
        return False

def is_ht_line(line,sep='%'):
    """判断该行是不是以sep为分隔符的HT条目行."""
    return line.strip()!="" and line[0].isalnum() and sep in line
    
def ht_line_to_dict(line,sep='%'):
    """将ht条目行转化为字典;"""
    outer = {} #外层字典: `head: tail`
    iner={} #内层字典: ``key:values`对
    if is_ht_line(line,sep=sep): # ht条目行
        head,tail=split_line(line,sep=sep)
        if '[' in tail: #tail中有'词性标签'
            tails=tail.split('[')
            
            tails_0=tails[0].strip()
            if tails_0 !="": #判断第一个`[`前是否有字符串,防止其丢失;
                iner['x']=[tails_0]
            
            for tag_values in tails[1:]: # tag1]:values;tag2]:values
                # if  ']' in tag_values: #一定有]
                idx = tag_values.find(']') # tag结束的位置
                tag = tag_values[:idx] # 得到tag名
                values = tag_values[idx+1:].strip().split(';') #tag的值列表:`值1;值2;`=>[值1,值2]
                
                if tag not in iner.keys(): #tail中含有两个相同的tag时,将后面tag的值添加到前面而不是直接取代前面;
                    iner[tag]=values #往第二层字典中添加元素
                else: 
                    for value in values:
                        if value not in iner[tag]:
                            iner[tag].append(value) #一个值一个值的添加
                
                while "" in iner[tag]: #删除tag的值列表中的所有空串
                    iner[tag].remove("")    
            outer[head] = iner 

        else: outer[head] = {'x': [tail]}
    else: #注释行(空白行也是注释行)
        outer[line.strip('\n').strip()]={'#': ["I'm a comment line!"]} #保证内层字典的值为列表
    return outer

def ht_txt_to_dict(file,sep='%'):
    """将文本文件转化为字典"""
    dn={}
    with open(file,'r',encoding='utf-8') as fp:
        for line in fp: 
            dn.update(ht_line_to_dict(line,sep=sep)) #若有重复单词,添加的是后面的含义
    return dn

def sort_lines_in_txt(file):
    """将单词本中的词条按字母顺序排序."""
    common.backup(file,"sort")
    with open(file,'r',encoding='utf-8') as f:
        lines = f.readlines()
        sorted_lines =  sorted(set(lines))
    with open(file,'w',encoding='utf-8') as f2:
        for line in sorted_lines:
            if line[0].isalnum():
                f2.write(line)
    return file

def print_ht_line(line,order=0,sep='%'):
    """分行显示一个HT条目.
    order: 可以表示行号."""
    head,tail=split_line(line,sep)
    head='#'+head+' '+sep+'\n'+'-'*fix.MARK_WIDTH
    # tail=tail+" [l]{:d};".format(order) #加上行号;
    tail=tail.replace('[','\n[').replace(']',']: ')
    line=head+tail
    print(line)
    print()

def origin(ptn,dir_path):
    """查看一个子串(ptn)在某个目录中(dir_path)的来源文件;查看某个单词(ptn)的来源词表(basic);"""
    files=[]
    for file in os.listdir(dir_path):
        filename = dir_path + '/' + file
        with open(filename,'r',encoding='utf-8') as fp:
            lines = fp.readlines()
        for line in lines:
            if re.findall(ptn,line)!=[]:
                files.append(filename)
                break #中断该次循环
    return files

# def modify(wanted_heads,file):
#     """修改头部列表中每一个头部所对应的尾部;
#     file: 待修改的文件."""
    
#     tt=HtDict().load(file)  
#     if str(wanted_heads)[0]!='[': wanted_heads=[wanted_heads] #wanted_heads为一个单词的时候
#     for i, word in enumerate(wanted_heads):
#         line=tt.to_line(word)
        
#         print("#{}".format(word))
#         print('-'*32)
        
#         print("<Old> {}".format(line))
#         cmd=input("p/[c]: ") #pass,change
#         while cmd not in ['p','c','']: cmd=input("p/[c]: ")
#         if cmd=="p":  continue  #跳过接下来的语句,转到下一个单词的操作
#         if cmd=="c" or cmd=="":
#             pyperclip.copy(line)  #弹出input输入框后,使用Ctrl+V粘贴原行
#             new=input("<New> ")  #粘贴原行后对其修改; spyder-input异常??用鼠标复制之后,无法回车;

#             if new=="exit": #从<new>退出
#                 print("Write file: {}..".format(file))
#                 tt.to_txt(file,mod='w')
#                 return "保存前面单词的修改,并在当前单词的弹出对话框中退出!"
            
#             while have_repeated_tags(new) or len(new)<=16: #避免含有相同的标签,避免New为空(或残缺);
#                 new=input("<RE-New> ")
#                 if new=="exit": #从<new>退出
#                     print("Write file: {}..".format(file))
#                     tt.to_txt(file,mod='w') ############太慢 #中断后丢失内容
#                     return "保存前面单词的修改,并在当前单词的弹出对话框中退出!"

#         word,_=split_line(new)
#         tt.edt[word]=ht_line_to_dict(new)[word]
#         print()
        
#     print("Write file: {}..".format(file))
#     tt.to_txt(file,mod='w')
#     return "完成所有单词的修改后退出!"

def similarity(s1,s2):
    """计算两个字符串的相似度"""
    return difflib.SequenceMatcher(None,s1,s2).quick_ratio()

def not_include():
    print("Not Include This Word!")

def split_line(line,sep='%'):
    """将line按第一个sep分割成两部分"""
    if sep!='\n': line=line.strip('\n') # 需要换行符的时候自己添加
    else: pass
    idx=line.find(sep)
    head=line[:idx].strip()
    tail=line[idx+1:].strip()
    return (head,tail)

def remove_repeated_ht_line(file):
    """去掉某个词表中重复的词条;"""
    common.backup(file,'_去重_')
    dt=HtDict().load(file)
    dt.to_txt(file)
    return file

# ####################################################################################
# #使用正则表达式修改文件, 如何批量修改文件的内容
# def substitute(pairs,file="F:/Git2/English/bigtan/bigtan.txt"):
#     """更改文件中的一些元素"""
#     common.backup(file,info="substitute")
#     with open(file,'r',encoding='utf-8') as fp:
#         fstring=fp.read()  
#     fstring=sequence_replace(fstring,pairs=OLD_NEW)
#     with open(file,'w',encoding='utf-8') as fp2:
#         fp2.write(fstring)  
#     return file

# def change_subject_label(line,pat="\[\w+\]"):
#     """将一行中的科目标签改为`<>`的形式"""
#     subs = re.findall(pat,line)
#     for old in subs:
#         new="<"+old[1:len(old)-1]+">"
#         line=line.replace(old,new)
#     return line
    
# def change_labels_in_txt(fpath):
#     """修改文本文件中的科目标签<科>"""
#     pat="\[[\u4e00-\u9fa5]{1,}\]"
#     with open(fpath,'r',encoding='utf-8') as fp:
#         string=fp.read()
#         subject=re.findall(pat,string)
#     for old in subject:
#         new="<"+old[1:len(old)-1]+">"
#         string=string.replace(old,new)
#     fpath2=fpath+".sub"
#     with open(fpath2,'w',encoding='utf-8') as fp2:
#         fp2.write(string)
#     print(fpath2.replace('/','\\'))

####################################################################################
####################################################################################

# def find_one_line(word,file):
#     """匹配文件中的某一行并返回"""
#     with open(file,'r',encoding='utf-8') as fp:
#         lines = fp.readlines()
#     for line in lines:
#         head,tail=split_line(line)
#         if word==head:
#             return line
#     return 0

# def add_one_line(word,active,new_line):
#     """添加行"""
#     if find_one_line(word,active)!=0:
#         print("#{}; have `{}`:; Not necessary!".format(active,word))
#     else: 
#         common.backup(active)
#         with open(active,'a+',encoding='utf-8') as fp:
#             fp.write(new_line)
#             omit=new_line[:10] + ' ... ' + new_line[-10:]
#             print("#{}; (+){}".format(active,omit.strip('\n')))
            
# def add_and_delete(word,active,source):
#     """添加一行并删除源行"""
#     new_line=find_one_line(word,source)
#     add_one_line(word,active,new_line)
#     delete_one_line(word,source)        

# def replace_one_line(word,file,new_line=None):
#     """`new_line=空白字符: 删除原始文件中的一行;
#         new_line=非空字符串: 用新行替换原始文件中的对应行;"""        
#     if new_line==None: 
#         print("new_line不能为None")
#         return 
    
#     old=find_one_line(word,file)
#     if old==0: 
#         print( "#{}; Can't find `{}`! Do Nothing!".format(file,word) )
#         return 
    
#     else: 
#         common.backup(file) #备份原始文件
#         with open(file,'r',encoding='utf-8') as fp:
#             strings=fp.read()
#         with open(file,'w',encoding='utf-8') as fp2:
#             strings=strings.replace(old,new_line)
#             fp2.write(strings)
            
#             old_omit=old[:10] + ' ... ' + old[-10:]
#             new_omit=new_line[:10] + ' ... ' + new_line[-10:]
            
#             if new_line=="": #删除了行    
#                 print( "#{}; (-){}".format(file,old_omit.strip('\n')))
#             else: #用new_line替换了文件
#                 print( "#{}; (t+){}=>{}".format(file,old_omit.strip('\n'),new_omit.strip('\n')))
# def delete_one_line(word,file):
#     """删除文件file包含word:的的一行"""
#     replace_one_line(word,file,new_line="")

# def replace_and_delete(word,active,source):
#     """"用source文件中的一行,替换掉当前文件的对应行,并把source文件中的那一行删除;"""
#     new_line=find_one_line(word,source)
#     replace_one_line(word,active,new_line=new_line) #active需要替换为新行
#     delete_one_line(word,source) #source文件需要删除改行
#########################################################################################
#########################################################################################
def print_ht_comments(file,sep='%'):
    """打印ht文件中的所有注释."""
    with open(file,'r',encoding='utf-8') as f:
        for line in f:
            if not is_ht_line(line,sep):
                print(line.strip('\n'))

def ht_union(file1,file2,overwrite=False):
    """将第二个文件合并到第一个;
    overwrite=False: 忽略file2中有重复头部的行.
    overwrite=True: 用file2中的行替换f2中的行.
    不要使用<合并HtDict字典后导出:主要用于整理格式>的方式: 太慢."""
    with open(file1,'r',encoding='utf-8') as f1:
        lines1=f1.readlines()
    with open(file2,'r',encoding='utf-8') as f2:
        lines2=f2.readlines()
    lines=[]
    dn1={}
    dn2={}
    for line in lines1:
        head,tail=split_line(line)
        dn1[head]=line
    for line in lines2:
        head,tail=split_line(line)
        dn2[head]=line
    head1=dn1.keys()
    head2=dn2.keys()
    heads=set(sorted(head1)+sorted(head2))
    for head in sorted(heads):
        if overwrite:
            if head in head2:
                lines.append(dn2[head])
            else:
                lines.append(dn1[head])
                
        else:
            if head in head1:
                lines.append(dn1[head])
            else:
                lines.append(dn2[head])
    common.backup(file1,'plus_file2')
    with open(file1,'w',encoding='utf-8') as f1:
        f1.writelines(sorted(lines))#自动添加'\n'?
    return file1
#####################################################################
# HtDict类
# 如何导入纯词表(如nltk的en)?
# 在每个单词后面添加一个%,然后导入; 单词的值为{'x': ['']};
# 不添加%,把其当做注释导入的; 单词的值为{'#': ["I'm a comment line!"]}
#####################################################################
class HtDict():
    """提供HT文本文件与Python字典之间的接口."""
    def __init__(self,file=None,sep='%'):
        """初始化一个空白字典."""
        self._base = {}
        if file==None: pass #必须加下划线        
        else: self._base=self.load(file,sep)._base

    def load(self,file,sep='%'):  
        """往核心字典_base中载入一个词表."""
        dn=ht_txt_to_dict(file,sep=sep)
        print("<HtDict><{}><{}>".format(file,len(dn)))
        self._base.update(dn)
        return self #可以返回自己,如此便可以使用`HtDict().load()``

    def loads(self,dir_path,level=2): 
        """载入目录(dir_path)下级别<=level的词表;一个个的载入;"""
        files = sorted(os.listdir(dir_path)[:level],reverse=True)
        for file in files:
            self = self.load(file=dir_path+file)
        return self 

    def loads_basic(self,dir_path): 
        """一次性载入目录下的所有词表;"""
        print("<HtDict><{}>".format(dir_path),end="")
        for file in sorted(os.listdir(dir_path),reverse=True):
            self._base.update(ht_txt_to_dict(dir_path+file))
        print("<{}>".format(len(self.wds)))
        return self 

    def clear(self):
        """清空字典."""
        self._base = {}
        print("当前词典中的单词个数已被清零!")

    def get_words_set(self):
        """获取单词集合."""
        return set(self._base.keys())
    wdset  = property(get_words_set)

    def get_words(self):
        """获取单词列表."""
        return list(self._base.keys())
    wds = property(get_words)
    
    def get_dict(self):
        """获取词典."""
        return self._base
    edt = property(get_dict)

    def get_length(self):
        """获取单词列表的长度"""
        return len(self._base)
    length=property(get_length)

    def similar(self,wrong_word,ratio=0.9,flag_print=False):
        """如果拼写错误,查找其近似词汇的含义;
        flag:是否返回相似词汇列表;
        ratio: 近似程度;
        """
        similar_words=[word for word in self.wds if similarity(wrong_word,word) >= ratio]
        if flag_print and len(similar_words)>0:
                for i,word in enumerate(similar_words):
                    print_ht_line(self.lookup_fz(word,i)) #此处不再使用有道
        return similar_words

    def lookup(self,word):
        """只在bigtan中查找单词的含义;"""
        if self.is_include(word):
            line = self.to_line(word)
        else: 
            line="NOT INCLUDE!"
        return line
     
    def lookup_fz(self,word):
        """在字典中查找单词的含义;若无是由有道查;"""
        if self.is_include(word):
            line = self.to_line(word)
        else: 
            line = yd_dict(word)
        return line
    
    def to_line(self,word,sep='%'):
        """将self._base的一个键值对转化为一个字符串;
        该版本竟然比to_line2块."""
        if self.have_tag('#',word): #注释行
            line=word #单词即是注释
        else: #单词行
            line = word + ' ' + sep
            for key,values in self._base[word].items():
                line = line + ' [' + key + ']'
                if values==[]: line=line+';'                
                else:# 把下面改成字符串处理,不循环的 或加个flag,加快以后的处理
                    for value in values:  #先去掉再添加;所有的项都有';'结尾,并且不会出现';;'
                        line = line + value.strip(';') + ';' 
                # else: #比上面的还慢
                #     values=";".join(values)
                #     line=line+values+';'

        return line
    
    ## to_txt对于大文件特别慢 7w/15min
    def to_txt(self,file,words=None,trigger=10,sep='%',mod='w'):
        """将字典保存为文本文件"""
        if words==None: words=self.wds
        else: words=words
        with open(file,mod,encoding='utf-8') as fp:
            for i, word in enumerate(words):
                line = self.to_line(word,sep)
                fp.write(line+'\n')
                common.progress_bar(i+1,len(words),word,trigger=trigger)
        return file
        
    def to_josn(self,file):
        """将词典保存为Json文件"""
        with open(file,'w',encoding='utf-8') as fp:
            json.dump(self._base,fp,ensure_ascii=False,indent=2)
        return file

    def load_json(self,file):
        """将Json文件导入到词典,其处理速度比Txt文件更快."""
        dn=common.json_to_dict(file) #并不是十分有效,有时json文件并不是一个字典??
        print("<HtDict><{}><{}>".format(file,len(dn)))
        self._base.update(dn)
        return self 
    
    def to_pickle(self,file):
        """将词典保存为pickle文件"""
        with open(file,'wb') as fp:
            dt = self.edt
            st = WdSet(dt.keys())
            tp = (dt,st)
            pickle.dump(tp,fp) #将字典保存为pkl文件
        return file
    
# 看看
    # def find_words_by_cn(self,cn):
    #     """在字典中查找中文对应的单词"""
    #     for word,word_value in self._base.items():
    #         for POS, meanings in word_value.items():
    #             if  cn in meanings:
    #                 line = self.to_line(word) 
    #                 print(line)
        
    def is_include(self,word):
        """查看词典是否收录该单词"""
        if word in self.wds: return True
        else: return False    
        
    def tags(self,word):
        """查看该单词有哪些标签."""
        if self.is_include(word):
            return list(self._base[word].keys())
        else: return []
    
    def have_tag(self,tag,word):
        """判断某个单词是否有某个tag."""
        tgs=self.tags(word)
        return tag in tgs

    ## 对于大文件特别慢????
    def get_comments(self):
        """输出字典中的所有注释(目录).
        条件: <1w的条目"""
        return [word for word in self.wds if self.have_tag('#',word)]

    def match(self,pat):
        """使用shell通配符匹配字典中的单词;
        `*`, `?`, `[seq]`, `[!seq]`"""
        return [e for e in self.elem if fnmatchcase(e,pat)]
    
    def make_wordlist(self,words,file='my_wdlt.txt'):
        """使用bigtan创建单词表;"""
        with open(file,'w',encoding='utf-8') as fp:
            for i,word in enumerate(words):
                common.progress_bar(i+1,len(words),word,trigger=10)
                line=self.lookup_fz(word)
                fp.write(line+'\n')
        return file
    
    
    ######################## test
    # def to_alter_txt(self,file):
    #     """整理文本文件的标记"""
    #     dn = ht_txt_to_dict(file)
    #     file2 = file[:-4]+'-alter'+file[-4:]        
    #     with open(file,'r',encoding='utf-8') as fp1:
    #         with open(file2,'w',encoding='utf-8') as fp2:
    #             for line in fp1:
    #                 if line[0].isalpha and line.count('%')==1: 
    #                     word =line.split('%')[0].strip()
    #                     line = self.to_line(word)
    #                     fp2.write(line+'\n')
    #                 else:
    #                      fp2.write(line)
    #     print(file2)    
            
    # def add_words(self,dn):
    #     """往字典中添加单词,含义不得重复;
    #     dn的长度不得大于6000,否则时间花费太多"""
    #     count = 0
    #     if len(dn)>6000:
    #         return "单词个数超过6000, 请使用: update(dn)"
            
    #     for word,value in dn.items():
    #         count += 1 
    #         if word in self.wds and value != self._base[word]:
    #             for POS,meanings in value.items():
    #                 if POS in self.POS(word) and meanings != self._base[word][POS]:
    #                     for meaning in meanings:
    #                         if meaning not in self._base[word][POS]: 
    #                             self._base[word][POS].append(meaning)
    #                 else: self._base[word][POS] = meanings
    #         else: self._base[word]=value
    def need():
        """比较两个文件有哪些共同词;"""
        pass


#####################################################################
# 词集分析器
#####################################################################
import nltk.corpus as corpus
def get_raw_string(file):
    """获取文件的原始字符串."""
    with open(file,'r',encoding='utf-8') as f:
        raw=f.read()
    return common.punctuator(raw)

def my_tokenize(file):
    """输出字幕文件中的所有有效单词."""
    raw=get_raw_string(file)
    raw=re.sub(u'[\u4e00-\u9fa5]+',' ',raw) #删除所有中文字符
    raw=re.sub(u'[0-9]+',' ',raw) #删除所有的数字
    raw=re.sub(u'[!"#$%&\()*+,./:;<=>?@[\\]^`{|}~]',' ',raw) #替换所有的非词内标点(非_-及单引号)
    tokens=re.split(r'\s+', raw)
    tokens=list(set(tokens))    
    _=[tokens.remove(i) for i in tokens if len(i)<2] #去除空串,字母,或单标点??['',"_",'-',"'"]
    return tokens

from collections import defaultdict
class WdSet():
    """单词短语分析器."""
    def __init__(self,words=None):
        """初始化一个集合用于保存单词."""
        self._base={}
        if words==None: pass
        else: self._base=self.load(words)._base 

    def load(self,words):
        """往结构中继续添加单词."""
        if type(words)==str: raise TypeError("words can't be a string!")
        self._base=set(list(self._base)+list(words)) #添加列表,元组,字典的键
        # print("<WdSet><words><TOT:{}>".format(self.length))
        warning=self.punctuation_warning()
        if warning!= None: 
            print(warning)
            print()
        return self    

    def get_set(self):
        "转化为词列表."
        return self._base
    core=property(get_set)    
    
    def get_length(self):
        """获取总数."""
        return len(self._base)
    length=property(get_length)    
        
    def get_list(self):
        "转化为词列表."
        return sorted(self._base)
    elem=property(get_list)    
    
    def punctuation_warning(self,puncts=PUNCTUATION_NOT_IN_WORD):
        """返回词集中第一个单词不该包含的标点."""
        for word in self._base:
            if word.isalpha()==True:
                for c in word:
                    if c in puncts:
                        return "##PUNCTUATION-WARNING##: {} ##".format(repr(word))
    
    def load_ht(self,file,sep='\n'):
        """从纯单词文本中导入."""
        # 通过`set(HtDict().load(file))`可以得到单词列表
        # 这里从split_line处开始操作
        words=[]
        with open(file,'r',encoding='utf-8') as fp:
            for line in fp:
                head,_=split_line(line,sep=sep)
                if head.strip()!="" and head[0].isalpha():
                    words.append(head.strip())

        self._base=set(list(self._base)+words)
        if "" in self._base: self._base.remove("")
        # print("<WdSet><{}><TOT:{}>".format(file,self.length))        
        warning=self.punctuation_warning()
        if warning!= None: 
            print(warning)
            print()
        return self 

    def load_article(self,file):
        """使用 从文章中获取单词字典."""
        words=my_tokenize(file)
        self._base=set(list(self._base)+words)
        # print("<WdSet><{}><TOT:{}>".format(file,self.length))          
        warning=self.punctuation_warning()
        if warning!= None: 
            print(warning)
            print()
        return self

    def to_ht(self,file='my_words.txt'):
        """写入一个纯单词文本"""
        lines=[ wd+'\n' for wd in self.elem] 
        with open(file,'w',encoding='utf-8') as fp:
            fp.writelines(lines)
        return file
    
    def clear(self):
        """清空集合"""
        self._base={}

    def delete(self,words):
        """删除集合中的的元素."""
        for word in words: 
            self._base.discard(word)

    def pick_by_width(self,width): 
        """根据单词的长度进行选词."""
        return sorted([wd for wd in self.elem if len(wd)==width])

    def get_width_dict(self):
        """获取字长字典."""
        out={}
        dn=defaultdict(list)    
        for wd in self.elem: dn[len(wd)].append(wd)
        keys=sorted(dn.keys(),key=lambda x: int(x))
        for k in keys: out[k]=dn[k]
        return out
#     width_dict=property(get_width_dict)
    
    def pick_by_initial(self,initial='a',include_upper=False):
        """根据首字母选词."""
        if include_upper: 
            out=[wd for wd in self.elem  if wd[0].upper()==initial.upper() ]
        else: 
            out=[wd for wd in self.elem if wd[0]==initial]
        return out 

    def get_initial_dict(self):
        """获取首字母字典"""
        dn=defaultdict(list)
        for wd in self.elem:
            dn[wd[0]].append(wd)
        return dict(dn)

    def capitalize(self,initial_only=True):
        """首字母或全字母大写化."""
        if initial_only:
            out=[wd[0].upper()+wd[1:] for wd in self.elem]
        else: 
            out=[wd.upper() for wd in self.elem]
        return out

    def have_element(self,elem):
        """判断是否有某个元素."""
        return True if elem in self._base else False

    def match(self,pat):
        """使用shell通配符匹配字典中的单词; `*`, `?`, `[seq]`, `[!seq]`"""
        return [e for e in self.elem if fnmatchcase(e,pat)]

    def pick_by_similar(self,wrong_word,ratio=0.9,flag_print=False):
        """查找某个单词的形似词,拼写错误也会有返回值. ratio:近似程度.
        """
        similar_words=[word for word in self.elem if similarity(wrong_word,word) >= ratio]
        if flag_print and len(similar_words)>0:
                for i,word in enumerate(similar_words):
                    print_ht_line(self.lookup_fz(word,i)) #此处不再使用有道
        return similar_words
    
    def pick_by_punctuation(self,p='-'):
        """根据标点选词."""
        out=[ wd for wd in self._base if not wd.isalpha() if p in wd]
        return out 

    def get_punctuation_dict(self,puncts=PUNCTUATION): 
        """获取标点字典."""
        dn=defaultdict(list)
        with_punct=[wd for wd in self._base if not wd.isalpha()]
        for wd in with_punct:
            for p in puncts:
                if p in wd: 
                    dn[p].append(wd)
        return dict(dn)

    def get_not_words(self,puncts=PUNCTUATION_NOT_IN_WORD):
        "获取集合中不是单词的元素."
        out=[]
        dn = self.get_punctuation_dict()
        for p in puncts:
            if p in dn.keys():
                out=out+dn[p]
        return sorted(set(out))

    def get_words(self):
        """获取单词"""
        return sorted(set(self._base).difference(set(self.get_not_words())))

    def get_phrase(self,puncts=[" ",".","(",")"]):
        "获取集合中的短语."
        out=[]
        dn = self.get_punctuation_dict()
        for p in puncts:
            if p in dn.keys():
                out=out+dn[p]
        return sorted(set(out))        

    # def get_words(self,puncts=["_","-","'"],):
    #     """获取集合中的单词."""
    #     out = [wd for wd in self._base if wd.isalpha()] #没有标点
    #     with_punct=
    #     for wd in with_punct:
    #         if wd in []
        
    #     dn = self.get_punctuation_dict()
    #     for p in puncts:
    #         if p in dn.keys() p not in puncts_phrase:
    #             out=out+dn[p]
        
    #     return sorted(set(out))

    def lemmatization(self,translator="morphy"):
        """使用某个翻译器对所有词进行词性还原."""
        pass
        #return out,pairs

    def morphy(self):
        """对每个单词进行wordnet.morphy处理.
        pairs: 还原对.
        out: 新的的词列表.
        """    
        out=[]; pairs=[]
        for wd in words:
            form=wd.lower() #首先将其小写化
            etymon = wordnet.morphy(form) 
            if etymon!=None and etymon!=form: 
                pairs.append((wd,etymon)) #有效对
            else: pass #不保存无效对            
            if etymon==None: out.append(wd)
            else: out.append(etymon) #有原形的大写单词同时被转换成了小写
    # pairs: 是morphy_fz查找出的有效转换对.out:按有效转换对原始词列表进行替换,此后可能出现多个单词对应同一个原形的情况
        return out,pairs 
    
        # 大文件拖慢加载函数    

#     familiar=get_familiar_words(level,upper_trans=True,extra_familiar=EXTRA_STOPWORDS,know_names=False,know_ogden=True,know_swadesh=True,know_stopwords=True)
#     dn['familiar']=sorted(set(words).intersection(set(familiar))) #文章中熟悉的词汇
#     dn['unfamiliar']=sorted(set(words).difference(set(dn['familiar']))) #文章中不熟悉的词汇,suoy
#     dn['_with_punctuation']=pickup_words_with_punctuation(unfamiliar) #unfamiliar当中带标点的词汇    
    
#     #对unfamiliar进行再处理: 使用morphy_fz或其他词干处理器?
#     wait,dn['_translator_pairs']=morphy_fz(unfamiliar)#查找到的可转换对
#     dn['_translator_familiar']=sorted(set(wait).intersection(set(familiar))) #不熟悉词经变换之后变成的熟悉词
#     dn['_translator_unfamiliar'=sorted(set(wait).difference(dn['_translator_familiar'])))
    
#     return dn

# def get_words_from_file(file,level=2,upper_trans=True,extra_familiar=EXTRA_STOPWORDS,exclude_names=False,exclude_ogden=True,exclude_swadesh=True,exclude_stopwords=True):
#     """从文章中获取熟悉单词和不熟悉的单词"""
#     dn={}
#     words=my_tokenize(file)
#     dn['words']=sorted(words) #文章中所有的单词

#     all_familiar=get_familiar_words(level,upper_trans=True,extra_familiar=EXTRA_STOPWORDS,exclude_names=False,exclude_ogden=True,exclude_swadesh=True,exclude_stopwords=True)
    
#     dn['familiar']=sorted(set(words).intersection(set(familiar))) #文章中熟悉的词汇
#     dn['unfamiliar']=sorted(set(words).difference(set(dn['familiar']))) #文章中不熟悉的词汇,suoy    
    
#     dn['familiar_with_punctuation']=pickup_words_with_punctuation(dn['familiar']) #unfamiliar当中带标点的词汇    
#     dn['familiar_without_punctuation']=sorted(set(words).difference(set(dn['familiar_with_punctuation'])))
    
#     dn['unfamiliar_with_punctuation']=pickup_words_with_punctuation(dn['unfamiliar']) #unfamiliar当中带标点的词汇    
#     dn['unfamiliar_without_punctuation']=sorted(set(dn['unfamiliar']).difference(set(dn['unfamiliar_with_punctuation'])))
    

#     return dn

# %%disable
# translator="morphy_fz"
# if upper_trans:
# #         dn['_translator_effective_pairs'] = sorted(set(new_words).intersection(set(familiar)).difference(set(words))) #实际用到的有效对
# #         try: 
# #             dn['_translator_effective_rate'] = np.round(len(dn['_translator_effective_pairs']) / len(dn['_translator_all_pairs']),2)
# #         except ZeroDivisionError: 
# #             dn['_translator_effective_rate']=0
#     #对unfamiliar进行再处理: 使用morphy_fz或其他词干处理器?
#     wait,dn['_translator_all_pairs']=morphy_fz(dn['unfamiliar'])#查找到的可转换对,translator的"总翻译库"
#     new_words= [new for old,new in dn['_translator_all_pairs']] #

#     dn['_translator_familiar']=sorted(set(wait).intersection(set(familiar))) #不熟悉词经变换之后变成的熟悉词
#     dn['_translator_unfamiliar']=sorted(set(wait).difference(dn['_translator_familiar']))



###########################################################################
###########################################################################

# import random
# def good_and_bad(file,initial_letter='',random_falg=False):
#     """将一个文件将文件进行二分类: good/bad;"""
#     good = file + '.good'
#     bad = file+'.bad'

#     dt=HtDict().load(file)
#     words = dt.words
    
#     if initial_letter!="": 
#         words=[word for word in words if word[0].lower()==initial_letter]
#         if len(words)==0: 
#             return "initial letter {} words is done.".format(initial_letter)
        
#     if random_falg:
#         random.shuffle(words)


#     for word in words:
#         print("="*64)
#         print_ht_line(dt.to_line(word))
#         print("-"*32)

#         cmd=input("use/bad['']: ") #默认将该单词条分类到哪个文件
#         if cmd=="exit": 
#             return "exit"
#         elif cmd=="": 
#             add_and_delete(word,bad,file) #默认回车时候(cmd为空),放到无用文件
#         else:
#             add_and_delete(word,good,file) #cmd非空,放到有用文件
# #####################################################################
# def omit_line(line):
#     """返回行的缩略形式;"""
#     head,tail=split_line(line)
    
#     string=head+": "
#     tags=re.findall(r"\[\w+\]",tail)
#     string=string+"".join(tags)
#     if '[^]' in tail:
#         or_=re.findall(r"\[or\](\w+);",tail)[0]
#         string=string+or_+';'
#     return string

# import random

# def classify_two(file,matcher="*",flag=False):
#     """将一个文件将文件进行二分类: good/bad;"""
#     common.backup(file)
#     file="F:/Git2/English/test/unix.txt"
#     bf = file+'.bad'
#     gf = file+'.good'

#     for file in [bf,gf]: #不存在的时候创建空白文件
#         if os.path.exists(file)==False:
#             with open(file,'w',encoding='utf-8') as fp: pass
#     bad = HtDict().load(bf)
#     good = HtDict().load(gf)

#     dt=HtDict().load(file) #待分裂的词典
#     words = dt.match(matcher)
#     if len(words)==0:  
#         return "模式<{}>未匹配到单词! 请重新设置!".format(matcher)
#     else: 
#         print("\n共匹配到单词: {}个!".format(len(words)))
    
#     if flag: random.shuffle(words) #是否对单词进行随机筛选
    
    
#     for word in words:
#         print("#"*64)
#         print_ht_line(dt.to_line(word))
        
#         cmd=input(">>>bad/good[!空]:") #默认将该单词条分类到哪个文件
        
#         ln=omit_line(dt.to_line(word)) #缩略行
        
#         if cmd=="exit" or cmd=="0":         
#             dt.to_txt(file,mod='w')
#             bad.to_txt(bf,mod='a+') #保存到文件才算完成这项工作,放到循环外
#             good.to_txt(gf,mod='w') #避免频繁的保存文件
#             return "Save and Exit!" #但是也要保证在程序自动退出之前,也必须要保存
        
#         elif cmd=="": 
#             bad.edt[word]=dt.edt[word] #cmd为空,放到无用文件
#             print("`{}`; (+){}".format(bf.split('/')[-1],ln))
#         else:
#             good.edt[word]=dt.edt[word] #cmd非空,放到有用文件
#             print("`{}`; (+){}".format(gf.split('/')[-1],ln))
            
#         del dt.edt[word] #删除原始文件中的词条
#         print("`{}`; (-){}".format(file.split('/')[-1],ln))
    
#     #所有单词遍历完之后也要保存
#     dt.to_txt(file,mod='w')
#     bad.to_txt(bf,mod='a+') #保存到文件才算完成这项工作,放到循环外
#     good.to_txt(gf,mod='a+') #避免频繁的保存文件
#     return "Done and Exit!" #但是也要保证在程序自动退出之前,也必须要保存

#####################################################################
# def update_words(words,active,source):
#     """从另一个词表中更新有关待查单词的词条: 字典版本"""
#     common.backup(active)
#     common.backup(source)
    
#     act=HtDict().load(active)
#     sou=HtDict().load(source)
    
#     dn={}
#     for word in words:
#         if word in sou.keys():
#             dn[word] = sou.edt[word]
#             del dt[word]
    
#     act.edt.update(dn)
#     act.to_txt(active+".update.txt")

def  is_cc(char):
    """判断一个字符否是汉字"""
    if len(char)!=1: return "请输入**一个**字符"    
    if '\u4e00' <= char < '\u9fff': return True
    else: return False 
# kk1

# def stem_tokens(tokens, stemmer=nltk.stem.SnowballStemmer('english')):
#     """stemmer: porterStemmer,snowballStemmer"""
#     stemmed = []
#     for token in tokens:
#         stemmed.append(stemmer.stem(token))
#     return stemmed


class TvShow():
    """整理文件名(字幕/视频);整理文件内容(字幕)"""
    
    def renames(self,path,head,pat=None):
        """文件名批量命名"""
        if pat==None:
            pat='S\d{2}E\d{2}'
        for old_name in os.listdir(path):
            mid = re.findall(pat,old_name)[0]
            end = old_name.split('.')[-1]
            new_name = head + '-' + mid + '.' + end
            os.rename(path+old_name,path+new_name)
        print("NumPat: {};\nPath: {};".format(pat,path))
    
    def to_tidy_txt(self,file):
        """去掉字幕文件的冗余信息"""
        with open(file,'r',encoding='utf-16') as fp:
            file2=file+'.tidy'
            with open(file2,'w',encoding='utf-8') as fp2:
                for line in fp:
                    if ',,' in line and is_cc(line.split(',,')[1][0]):
                        time = line[14:19]
                        en = re.findall(r'\}.*$',line)[0][1:]
                        cn = re.findall(r',,.*\\N',line)[0][2:].strip('\\N')
                        new_line = "{}  {} % {}".format(time,en,cn)+'\n'
                        fp2.write(new_line)
        print(file2)

    def to_audio_from_video(self,video_path='F:\Miranda\-S01E04.mp4',audio_ext='.mp3'):
        """将一个视频转化为音频"""
        idx = video_path.rfind('.')
        video = VideoFileClip(video_path)
        audio_path = video_path[:idx] + audio_ext
        video.audio.write_audiofile(audio_path)

##########################################################################
##########################################################################
# def youdaoapi(raw="bear", en2zh=True, sentence=True):
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
#     if en2zh == True:
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
