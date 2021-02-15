# 根据所需单词列表(无释义), 在大库中提取出其词汇表(有释义);
needlist=English_Dictionary().load('a',flag='word')
biglist=English_Dictionary().load('a',flag='word-')
out_file = "uok.txt"

jiaoji = sorted(list(set(needlist.words).intersection(set(biglist.words))))
out=English_Dictionary()
for word in jiaoji:
    out._engdt[word]=biglist._engdt[word]
out.to_txt(out_file)
##################################################################
# 去除某个词表中与另一个词表中重复的单词
unix_ul=English_Dictionary().load("word-/66_unix_useless.txt")
jiaoji=sorted(list(inter.intersection(set(unix_ul.words))))
for word in jiaoji:
    del unix_ul._engdt[word]

unix_ul.to_txt("word-/66_unix_useless-useless.txt")