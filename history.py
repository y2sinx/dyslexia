from dyslexia.english import EnDict
from dyslexia import NEEDED_PATH

def uk_history(year,flag=True,file=None):
    """根据年份查看英国王朝;"""
    
    if file==None: file=NEEDED_PATH['uk_history.ht']
    else: file=file
    box=[]; keys=[]
    history = EnDict(file)
    print()
    xys=history.lt

    for xy in xys:
        try:
            x=int(xy.split('-')[0].split('.')[0])
            y=int(xy.split('-')[1].split('.')[0])
            box.append(x)
            box.append(y)    
            if x<=year<=y: keys.append(xy)
        except:
            pass

    if flag:
        for key in keys:
            print(history.to_line(key))
            print()
    return  keys

