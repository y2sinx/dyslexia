# F:/Git2/English/test/names_add.py
import requests
from bs4 import BeautifulSoup
def names_adding(word):    
    try:
        url_yd = "http://dict.youdao.com/w/%s/#keyfrom=dict2.top" % word
        r = requests.get(url=url_yd)

        # 利用BeautifulSoup将获取到的文本解析成HTML
        soup = BeautifulSoup(r.text, "lxml")
        # 获取字典的标签内容
        s = soup.find(class_="trans-container")("ul")[0]("li")
        additional = soup.find(class_="additional").get_text()
        phonetic = soup.find(class_="phonetic").get_text()
        phonetic = '[a]'+'/'+phonetic[1:len(phonetic)-1]+'/;'
        meanings = ''
        for item in s:
            if item.text:
                meanings = meanings+biaodian(item.text)+'; '
        meanings = meanings.replace('n. ','[n]').replace('vt. ','[vt]').replace('adj. ','[a]').replace('adv. ','[ad]')
        return "{}: {} {}".format(word,phonetic,meanings)
    except Exception: return 0

#######################################################
male=EngDict("F:/Git2/English/names/male.txt").words
female=EngDict("F:/Git2/English/names/female.txt").words
family=EngDict("F:/Git2/English/names/family.txt").words
print('='*32)

names = male
# name = female
# name = family

fn_out = "F:/Git2/English/names/{}.yes".format('male')
fn_out2 = fn_out.replace('yes','no') 

len_names=len(names)
with open(fn_out,mode='w',encoding='utf-8') as fn1: 
    with open(fn_out2,mode='w',encoding='utf-8') as fn2: 
        print("Writing: {}".format(fn_out))
        print("Writing: {}".format(fn_out2))
        for i,word in enumerate(names):
            line = names_adding(word)
            if line==0: fn2.write(word+'\n')
            else: fn1.write(line+'\n')
            num=i+1
            print("{}/{}: {}".format(num,len_names,word))