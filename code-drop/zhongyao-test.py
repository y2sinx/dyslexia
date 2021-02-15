# -*- coding: utf-8 -*-
"""
Created on Fri May  8 15:37:09 2020

@author: tfliu
"""
    # 看看
    # def find_words_by_cn(self,cn):
    #     """在字典中查找中文对应的单词"""
    #     for word,word_value in self._base.items():
    #         for POS, meanings in word_value.items():
    #             if  cn in meanings:
    #                 line = self.to_line(word)
    #                 print(line)

#%%
    ######################## test
    # def to_alter_txt(self,file):
    #     """整理文本文件的标记"""
    #     dn = ht_ht_to_dict(file)
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

# def ht_plus_accent(needs,file):
#     """将需要更给的行,修改后放到文件file.
#         needs: 需要更改的行."""
#     with open(file,'w',encoding='utf-8') as fp:
#         for i,line in enumerate(needs):
#             word,tail=split_line(line)
#             acc=get_word_accent(word)
#             line=word+' % '+acc+' '+tail
#             progress_bar(i+1,56460,word,trigger=100)        
#             fp.write(line+'\n')
#     return file

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




# def get_words_from_file(file,level=2,upper_trans=True,EXTRA_FAMILIAR=EXTRA_STOPWORDS,EXCLUDE_NAMES=FALSE,EXCLUDE_OGDEN=TRUE,EXCLUDE_SWADESH=TRUE,EXCLUDE_STOPWORDS=TRUE):
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

# kk1

# def stem_tokens(tokens, stemmer=nltk.stem.SnowballStemmer('english')):
#     """stemmer: porterStemmer,snowballStemmer"""
#     stemmed = []
#     for token in tokens:
#         stemmed.append(stemmer.stem(token))
#     return stemmed




# def remove_repeated_line(file):
#     """去掉某个词表中重复的词条;"""
#     common.backup(file,'_去重_')
#     dt=HtDict().load(file)
#     dt.to_txt(file)
#     return file


