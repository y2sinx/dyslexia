

## 26个单词列表对应的单词 a,b,...,z
for alpha in Alphabet:
    unix_alpha='unix_'+alpha.lower()
    fn="F:/Git2/English/unix/{}.txt".format(alpha)
    wds = set(EngDict(fn).words)
    exec("{}={}".format(unix_alpha,'wds'))
print("="*32)

## 已知单词
know1 = set(EngDict('all').words)
know2 = set(EngDict('F:/Git2/English/unix/unix_meanings.txt').words)
know=know1.union(know2)
print("="*32)

#######################################################
## 选定待查的范围
unix_alpha = unix_x
fn_out='F:/Git2/English/test/{}.txt'.format('unix_test')
fn_out2=fn_out+'.nomeaning'
## 待查单词,排除已知含义的单词
lookuping = unix_alpha.difference(know) 
lookuping = list(lookuping)[:20]
#######################################################
len_lookuping=len(lookuping)
with open(fn_out,mode='w',encoding='utf-8') as fn1: 
    print("Writing: {}".format(fn_out))
    print("Writing: {}".format(fn_out2))
    with open(fn_out2,mode='w',encoding='utf-8') as fn2:  #with不要放进循环
        for i,word in enumerate(lookuping):
            line = unix_adding(word)
            if line==0: fn2.write(word+'\n')
            else: fn1.write(line+'\n')
            num=i+1
            print("{}/{}: {}".format(num,len_lookuping,word))

################################
