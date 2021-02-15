%%to_file F:/Git/ddpie/test/

%%disable 词典>>.ht

pairs={
#     ('"', ''        ),
#     (',', ';'  ),
#     ('\\\\n', ''  ),
#     ('"',''),

#     (' n. ', '[n]'   ),
#     (' v. ', '[v]'          ),
#     (' vt. ', '[vt]'      ),
#     (' vi. ', ''   '[vi]'       ),
#     (' interj. ', '[int]'          ),
#     (' a. ', '[a]'          ),
#     (' adj. ', '[a]'          ),
#     (' adv. ', '[ad]'          ),
#     (' un. ', '[un]'          ),
#     (' suf. ', '[suf]'          ),
    
    (' abbr. ', '[abr]'          ),
    (' prep. ', '[prep]'          ),}
#     ('] ', ']'          )}

for file in os.listdir():
    lines=[]
    with open(file,'r',encoding='utf-8') as f:
        for line in f:
            line=re.sub(u':',' % ',line,count=1)
            line=sequence_replace(line,pairs)
            line=punctuator(line)
            lines.append(line.strip()+'\n')
    new=os.path.splitext(file)[0]+'.ht'
    with open(new,'w',encoding='utf-8') as f2:
        f2.writelines(lines)
    
    print(new)
    
%%disable # 整理标签
for file in os.listdir():
    ht=HtDict(file)
    ws=WdSet(ht.wds)

    phr=ws.get_not_words()
    wrd=ws.get_words()
    
    print(file)
    ht.to_txt(file+'.phr',phr,trigger=5000)
    ht.to_txt(file+'.wrd',wrd,trigger=5000)