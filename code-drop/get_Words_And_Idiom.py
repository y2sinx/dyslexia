##2020-4-2#16-53
# 美国之音 > Voa English Learning > Words And Idiom;

minus={'VOA Standard English',
 'VOA Standard English Archives',
 'Technology Report',
 'This is America',
 'Science in the News',
 'Health Report',
 'Education Report',
 'Economics Report',
 'American Mosaic',
 'In the News',
 'American Stories',
 'Words And Their Stories',
 'Trending Today',
 'AS IT IS',
 'Everyday Grammar',
 'Ask a Teacher',
 'U.S. History',
 "America's National Parks",
 "America's Presidents",
 'Agriculture Report',
 'Explorations',
 'People in America',
 'Learning English Videos',
 'English in a Minute',
 'English @ the Movies',
 'News Words',
 'Everyday Grammar TV',
 'Bilingual News',
 'Learn A Word',
 'Words And Idioms',
 'English in a Minute',
 'How to Say it',
 'Business Etiquette',
 'American English Mosaic',
 'Popular American',
 'Sports English',
 'Go English',
 'Wordmaster',
 'American Cafe',
 'Intermediate American Enlish',
 'President Address'}

need=[]
for num in range(1,18):
    url="https://www.51voa.com/Words_And_Idioms_%d.html" % num
    need.append("## "+url+'\n')
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    for i in soup('li'):
        target=i.text.strip()
        if  target not in minus:
            need.append(target+'\n')
with open("Words_And_Idiom.txt",'a+',encoding="utf-8") as fp:
    fp.writelines(need)
print("Words_And_Idiom.txt")
