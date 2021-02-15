## 2020-3-17; 19:54:4;
# from useless to ok
know=English_Dictionary().load('a')
useless_file="F:/Git2/English/test/33_unix_useless.txt"
ok_file="F:/Git2/English/word/31_unix_ok.txt"
useless=English_Dictionary().load(useless_file)
ok=English_Dictionary().load(ok_file)


# 将 useless 中需要知道含义的单词移动到 ok(如果ok没有这些单词的话);
#,如果ok中有这些单词,直接删除 useless 中的单词;
for word in set(useless.words).intersection(set(know.words)):
    if word in ok.words: 
        delete_one_line(word,useless_file)
    else: 
        add_and_delete(word,ok_file,useless_file)
