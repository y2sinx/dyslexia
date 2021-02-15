#################################
#获取新英语900句: 生活篇        #
#################################
for num in range(1,61):
    
    url="http://www.unsv.com/material/english-speaking-900b/lesson%s/" % num #生活篇章
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    title=soup.find('title').text
    lines = soup.find(class_="fulltext")("p")

    string=""
    for line in lines:
        line=line.string
        if "生词解读" in line:
            break
        string=string+line+'\n'
    
    fp=open("new_english_900_life.txt","a+",encoding="utf-8") #生活篇章
    lesson= title + "\n" + string + "\n"
    fp.write(lesson)
    fp.close()
    print(num)
    
#################################
#获取新英语900句: 基础篇        #
#################################
for num in range(1,61):
    url="http://www.unsv.com/material/english-speaking-900a/lesson%s/" % num #基础
#     url="http://www.unsv.com/material/english-speaking-900b/lesson%s/" % num #生活篇章
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    
    title=soup.find('title').text    
    lines = soup.find(class_="fulltext")("p")
    
    string=""
    for line in lines:
        line=line.string      
        
        try:
            if "生词解读" in line: break
            string=string+line+'\n'
        except: pass
        

    fp=open("new_english_900_basic.txt","a+",encoding="utf-8") #基础篇章
    lesson= title + "\n" + string + "\n"
    fp.write(lesson)
    fp.close()
    print(num)