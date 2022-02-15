'''
# 섹터 별 코인 DB 등록
import requests
from bs4 import BeautifulSoup
import pymysql

import time

full_name = []
name = []

Rate_of_ups_downs_by_Section(Sector_URL, Sector_Name, Figure_Per_1H, Figure_Per_24H, Figure_Per_7D)

for i in range(0, 30) :
    del Sector_Name[0]

time.sleep(3)

conn = pymysql.connect(host='localhost', user='root', password='',db='test', charset='utf8')
curs = conn.cursor()

for Name in Sector_Name :
    Name_URL_fix = Name.replace(' ','-').replace('(','').replace(')','').replace('.','-').replace('/','-').replace(' / ','-')
    Name_URL_fix = Name_URL_fix.lower()
    Name_DB_fix = Name.replace(' ','_').replace('(','').replace(')','').replace('.','_').replace('-','_').replace('/','_').replace(' / ','_')
    sql = 'create table ' + Name_DB_fix + ' ( seq int not null auto_increment, fullname varchar(100), name varchar(30), primary key(seq))engine=myisam charset=utf8;'
    curs.execute(sql)
    for page in range(1,10) :
        URL ='https://www.coingecko.com/ko/categories/' + Name_URL_fix + '?page=' + str(page)
        r = requests.get(URL)
        soup = BeautifulSoup(r.text, 'html.parser')
        if '코인을 찾을 수 없습니다...' in soup :
            break
        elif 'No Coins Found' in soup :
            break
        
        SectorLists = soup.select('div.tw-items-center > a') # 1번쨰는 <  #2번째는 div.tw-items-center > a 이경우 pop(0)을 안해줘도됨
        if SectorLists :
            del SectorLists[0]
            del SectorLists[0]
        else :
            SectorLists = soup.select('div.center > a')
            SectorLists.pop()
            SectorLists.pop()
            SectorLists.pop()
        
        
        for i, SectorList in enumerate(SectorLists) :
            if(i%2 == 0) :
                full_name.append(SectorList.text.replace('\n',''))
            else :
                name.append(SectorList.text.replace('\n',''))
                
        for i in range(0, len(name)) :
            sql2 = "insert into " + Name_DB_fix + "(fullname, name) values ('" + full_name[i] + "','" + name[i] +"')"
            curs.execute(sql2)
        
        print(str(Name) + 'of ' + str(page) + 'page Sucess')
        full_name.clear()
        name.clear()
        
    
                
        
        
        #sql2 = "insert into " + Name_DB_fix + "(fullname, name) values ('" + full_name + "','" + name +"')"
        #curs.execute(sql2)
        
        

#bitcoin DB의 bithumbcoin table에 코인리스트 등록 확인.
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='',db='bitcoin', charset='utf8')
curs = conn.cursor()

Bithumb_Coin = CheckBithumbCoins()

for coin in Bithumb_Coin :
    name = coin.split('/')[0]
    market = coin.split('/')[1]
    sql = "insert into bithumbcoin(name, market) values ('" + name + "','" + market +"')"
    curs.execute(sql)

'''
