## 2020-3-18; 21:45:16;
# 将百词斩单词更新到bigtan
bcz=English_Dictionary().load('18_baicizhan.txt')
bigtan=English_Dictionary().load('bigtan.txt')
bcz.edt.update(bigtan.edt)
bcz.to_txt('new_bigtan.txt')

%P len(bcz.edt)
