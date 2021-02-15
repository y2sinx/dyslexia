## 2020-3-18; 21:8:42;
#筛选出百词斩中的词汇: word中有空格
all_words=English_Dictionary().load('baicizhan.txt')

phr=English_Dictionary()
wrd=English_Dictionary()

for word in all_words.words:
    if " " in word.strip():
        phr.edt[word]=all_words.edt[word]
    else:
        wrd.edt[word]=all_words.edt[word]

%P len(phr.edt); len(wrd.edt)

wrd.to_txt('wrd.txt')
