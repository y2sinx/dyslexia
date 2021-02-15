## 2020-3-18; 20:8:4;
import sqlite3

idfn='F:/英语/百词斩/id_book/284_bec_高级.baicizhan'
bookname = 'F:/Git2/English/test/bec3_bcz.txt'

idpd = pd.read_csv(idfn)
idlt = idpd.values[:,0].tolist()

db = sqlite3.connect('F:/英语/百词斩/lookup.db')
cur = db.cursor()
sql = "SELECT * FROM dict_bcz"
cur.execute(sql)
rows = cur.fetchall()

dt_bcz={} #所有单词构成的字典

for row in rows:
    topic_id = str(row[0])
    word = row[1]
    accend = row[2]
    mean_cn = common.biaodian(row[3])
    dt_bcz[topic_id]={word: {'x':[mean_cn],'acc':[accend]} }

word_book_bcz = {} #与某本书对应的单词字典
for key in idlt:
    word_book_bcz.update(dt_bcz[str(key)])

en=english.English_Dictionary()
en.edt.update(word_book_bcz)

en.to_txt(bookname)
print("单词表的长度: ",len(en.words))
## 2020-3-18; 20:10:17;
import sqlite3

idfn='F:/英语/百词斩/id_book/284_bec_高级.baicizhan'
bookname = 'F:/Git2/English/test/bec3_bcz.txt'

idpd = pd.read_csv(idfn)
idlt = idpd.values[:,0].tolist()

db = sqlite3.connect('F:/英语/百词斩/lookup.db')
cur = db.cursor()
sql = "SELECT * FROM dict_bcz"
cur.execute(sql)
rows = cur.fetchall()

dt_bcz={} #所有单词构成的字典

for row in rows:
    topic_id = str(row[0])
    word = row[1]
    accend = row[2]
    mean_cn = common.biaodian(row[3])
    dt_bcz[topic_id]={word: {'x':[mean_cn],'acc':[accend]} }

word_book_bcz = {} #与某本书对应的单词字典
for key in idlt:
    word_book_bcz.update(dt_bcz[str(key)])

en=english.English_Dictionary()
en.edt.update(word_book_bcz)

en.to_txt(bookname)
print("单词表的长度: ",len(en.words))
