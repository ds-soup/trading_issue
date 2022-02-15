import pandas as pd

# 자동거래 관련 클래스
from transaction import *

#비동기화 프로세싱
import asyncio
import time

#멀티쓰레딩
import threading

recommand = []
th_lock = threading.Lock()
Having_Coin = []
status = False 
# recommand renewal patch : True
# 



# 30분에 1번씩 실행
def Find_Coin() :
    global recommand, status
    Finder = AI_Explore_Coin()
    Finder.Get_Rank()
    th_lock.acquire()
    result = Finder.Compare_Bithumb_to_Sector()
    print(result)
    if(result is None) :
        status = True
        return
    
    recommand = result.values.tolist()
    print('{0} 입니다.'.format(recommand[0][0]))
    status = True
    th_lock.release()
    threading.Timer(1800,Find_Coin).start()

def Check_Recommand_Coin() :
    global recommand, status

    if not recommand :
        return
    for i in range(0,len(recommand)) :
        trader = AI_BitCoin_Bidder(recommand[i][0],'KRW')
        if( trader.Compare_Volume_Average(5) and trader.Check_Order_Book()) :
            # 코인 구매
            result = trader.order_coin()
            if result is not None :
                print('{0} 코인이 주문되었습니다.'.format(recommand[i][0]))
                Having_Coin.append(recommand[i][0])
                return
            else :
                print('{0}\t False'.format(recommand[i][0]))
                continue
    status = False
    recommand.clear()


def Check_ALL_Coin() :
    coins = Bithumb.get_tickers()
    for coin in coins :
        trader = AI_BitCoin_Bidder(coin, 'KRW')
        if(trader.Compare_Volume_Average(5) and trader.Check_Order_Book()) :
            # 코인 구매
            result = trader.order_coin()
            if result is not None :
                print(result)
                print('{0} 코인이 주문되었습니다.'.format(coin))
                Having_Coin.append(coin)
                return
            else :
                print('{0}\t False'.format(coin))
                continue
            

def Monitoring(coin) :
    trader = AI_BitCoin_Seller(coin, 'KRW')
    while True :
        time.sleep(1)
        if(trader.Check_Condition()) :
            # 코인을 판매하는 로직
            result = trader.Sell_Coin()
            if result is not None :
                print('{0} 코인이 판매되었습니다.'.format(coin))
                Having_Coin.remove(coin)
                break
            else :
                continue
            


        

#-------------------main-------------------------
if __name__ == '__main__' :
    Find_Coin()

while True :
    
    if( status is True and not Having_Coin) :
        Check_Recommand_Coin()
    elif(not Having_Coin) :
        print('조건에 맞는 코인을 찾아봅니다.')
        Check_ALL_Coin()
    elif(Having_Coin) :
        for coin in Having_Coin :
            print('{0} 코인에 대한 모니터링을 시작합니다.'.format(coin))
            Monitoring(coin)
    time.sleep(1)



