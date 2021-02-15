## 2020-3-18; 20:58:7;
#百词斩词库
import sqlite3

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
    mean_cn = common.biaodian(" "+row[3])
    mean_cn = mean_cn.replace('［','<').replace('］','>') #科目标签,[]改为<>
    mean_cn = sequence_replace(mean_cn,OLD_POS,NEW_POS)

    dt_bcz[topic_id]={word: {'acc':[accend], 'x':[mean_cn]} }

bcz_edt={}
for key in dt_bcz.keys():
    bcz_edt.update(dt_bcz[key])
#%P len(bcz_edt)

bcz=English_Dictionary()
bcz.edt.update(bcz_edt)
bcz.to_txt('F:/Git2/English/test/baicizhan.txt')
print("单词表的长度: ",len(bcz.words))
