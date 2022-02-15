from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import time

from bs4 import BeautifulSoup

# Bithumb에 상장되어 있는 코인 리스트
# selenium으로 수정 완료. 
#CheckBithumbCoins() > LoadDataset.py 

def CheckBithumbCoins() :
    Bithumb_Coin = []
    
    url = 'https://www.coingecko.com/ko/%EA%B1%B0%EB%9E%98%EC%86%8C/bithumb'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    path = '/workspace/trading_issue/ChromeDriver/chromedriver'
    driver = webdriver.Chrome(executable_path=path,chrome_options=chrome_options)
    driver.get(url) 
    
    show_more = driver.find_element_by_css_selector('div.center > a')
    print(show_more.text)
    for i in range(0,5) :
        show_more.click()
        time.sleep(2)
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    attr = {
        'class':'mr-1',
        'rel':'nofollow noopener'
    }
    Bithumb_Coins = soup.find_all('a',attr)

    for Bithumb in Bithumb_Coins :
        tmp = str(Bithumb.string).replace('\n','')
        if 'None' in tmp :
            continue
        Bithumb_Coin.append(tmp)
    
    return Bithumb_Coin

