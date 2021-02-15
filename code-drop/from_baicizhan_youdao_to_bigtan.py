## 2020-3-18; 17:3:28;
bcz=English_Dictionary().load("F:/Git2/English/bigtan/bcz_db.txt")
bigtan=English_Dictionary().load("F:/Git2/English/bigtan/bigtan.txt")


diff=set(bcz.words).difference(bigtan.words)
cant_find=set(English_Dictionary().load("F:/Git2/English/bigtan/cant_find.txt").words)
diff=diff.difference(cant_find)
diff=sorted(list(diff))

diff=diff[:1000]
need="F:/Git2/English/bigtan/need.txt" #保存地址

length=len(diff)
with open(need,'w',encoding='utf-8') as fp:
    for i,word in enumerate(diff):
        try:
            line=ydtrans(word)
            fp.write(line+'\n')
            print("{}/{}\t{}".format(i,length,word))
        except:
            line="## {}".format(word)
            fp.write(line+'\n')
print("\n结束!")
