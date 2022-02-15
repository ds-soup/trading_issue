from pybithumb import Bithumb
import websockets


#dataset
import json

# Crolling Modules
import requests
from bs4 import BeautifulSoup

import pymysql
import pandas as pd


# Get API Keys
def Load_Key() : 
    con_key = ''
    sec_key = ''
    with open('key.txt', 'r') as f :
        for i in range(0, 2) :
            try :
                line = f.readline()
                if not line :
                    raise KeyNotFoundError
                if 'con' in line :
                    con_key = line.split(':')[1]
                    con_key = con_key.replace('\n','')
                if 'sec' in line :
                    sec_key = line.split(':')[1]
                    sec_key = sec_key.replace('\n','')
            except KeyNotFoundError :
                print('API Key Not Found. return FALSE')
                return False,False
    return con_key, sec_key

# 카테고리 별 등락률 1H , 24H, 7D
# 22.01.28 기준 70가지 Category
def Rate_of_ups_downs_by_Section(url, Sector_Name, Ups_Down_Per_1H, Ups_Down_Per_24H, Ups_Down_Per_7D) :
    
    attr = {
        'class':'coin-name'
    }
    
    r = requests.get(url)
    r.raise_for_status()
    
    soup = BeautifulSoup(r.text, 'html.parser')
    Sector_Names = soup.find_all('td', attr)
    
    for idx, Sector in enumerate(Sector_Names) :
        if(idx % 8 == 0) :
            Sector_Name.append(Sector.attrs['data-sort'])
        if(idx % 8 == 2) :
            Ups_Down_Per_1H.append(Sector.attrs['data-sort'])
        if(idx % 8 == 3) :
            Ups_Down_Per_24H.append(Sector.attrs['data-sort'])
        if(idx % 8 == 4) :
            Ups_Down_Per_7D.append(Sector.attrs['data-sort'])
            
def Clear_Rate_of_ups_downs(*args) :
    for arg in args :
        arg.clear()

# Top3 Sector 구하기
def Top3_Rank_Figure(Figure_per, Sector_Name) :
    
    Max = -99.0 
    Second = -99.0 
    Third = -99.0 

    for index, Figure in enumerate(Figure_per) :
        if(Max < float(Figure)) :
            Max = float(Figure)
            First_index = index
            
        elif(Second < float(Figure) and (float(Figure) < Max)) :
            Second = float(Figure)
            Second_index = index
        elif(Third < float(Figure) and float(Figure) < Second) :
            Thrid = float(Figure)
            Third_index = index
    
    First_Sector = Sector_Name[First_index]
    Second_Sector = Sector_Name[Second_index]
    Thrid_Sector = Sector_Name[Third_index]
    
    return (First_Sector, Second_Sector, Thrid_Sector)
    

# 섹터의 코인들 중 Bithumb에 상장되어 있는 코인 리스트
# 반환 값은 pandas의 DataFrame 타입
def Load_Sector_CoinList(Sector) :
    Sector_Name = Sector.replace(' ','_').replace('(','').replace(')','').replace('.','_').replace('-','_').replace('/','_').replace(' / ','_')
    
    #select b.name from Smart_Contract_Platform as S, bithumbcoin as b where S.name=b.name group by b.name;
    sql = "select b.name from "+ Sector_Name +" as S, bithumbcoin as b where S.name=b.name group by b.name"
    
    conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='test',
    charset='utf8')
    
    column = ['name']
        
    
    curs = conn.cursor()
    curs.execute(sql)
    result = curs.fetchall()
    result = pd.DataFrame(result,columns=column)
    
    curs.close()
    conn.commit()
    conn.close()
    
    
    return result['name']


