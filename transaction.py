from functions_file import Rate_of_ups_downs_by_Section
from functions_file import Top3_Rank_Figure
from functions_file import Clear_Rate_of_ups_downs as Clear
from functions_file import Load_Sector_CoinList

from market.pybithumb.client import Bithumb
from market.pybithumb.core import *
from functions_file import Load_Key

from xcoin_api_client import *
from pybithumb.core import *

import pandas as pd
import math

class AI_Explore_Coin :
    
    def __init__(self) :
        
        self.Sector_Name = []
        self.Figure_Per_1H = []
        self.Figure_Per_24H = []
        self.Figure_Per_7D = []
        self.Sector_URL = 'https://www.coingecko.com/ko/categories'
    
    def __del__(self) :
        
        print('Sector Ranking Found OK!')
        
    def Get_Rank(self) :
        
        Rate_of_ups_downs_by_Section(self.Sector_URL, self.Sector_Name, self.Figure_Per_1H, self.Figure_Per_24H, self.Figure_Per_7D)
        Ranking = Top3_Rank_Figure(self.Figure_Per_1H,self.Sector_Name)
        self.Ranking = Ranking
        print('Sector Found! ')
        print(Ranking)
        return Ranking
        
    # return; DataFrame
    def Compare_Bithumb_to_Sector(self) :
        df = pd.DataFrame()
        for sector in self.Ranking :
            result = Load_Sector_CoinList(sector)
            df = pd.concat([df,result])
        if (df.empty) :
            return 
        return df
       
class AI_Trader :
    '''Super Class'''
    def __init__(self, order_currency, payment_currency) :
        self.order_currency = order_currency
        self.payment_currency = payment_currency
        self.con_key, self.sec_key = Load_Key()
        self.api = XCoinAPI(self.con_key, self.sec_key)
        self.private_api = PrivateApi(self.con_key, self.sec_key)
        
    def Current_Price(self) :
    
        result = PublicApi.ticker(self.order_currency, payment_currency=self.payment_currency)
        return float(result['data']['closing_price'])
    
    def Average_Price(self) :
        
        chart = Bithumb.get_candlestick(self.order_currency,payment_currency=self.payment_currency,chart_intervals='1m')
        aver_chart = chart.iloc[-5:]
        open_aver = aver_chart['open'].sum() / 5
        close_aver = aver_chart['close'].sum() / 5
        average = (open_aver + close_aver) / 2
        return average
    
    def Check_Account(self) :
        bithumb = Bithumb(self.con_key, self.sec_key)
        balance = bithumb.get_balance(self.order_currency)
        return balance

    def Can_Buy_Coin_Quantity(self, account) :
        buy_quantity = (account[2] - account[3]) / float(self.Current_Price())
        return buy_quantity
    
    def Can_Sell_Coin_Quntity(self, account) :
        sell_quantity = (account[0] - account[1]) / float(self.Current_Price())
        return sell_quantity
        


class AI_BitCoin_Bidder(AI_Trader) :
    
    def __init__(self, order_currency, payment_currency) :
        super(AI_BitCoin_Bidder,self).__init__(order_currency, payment_currency)
    
    # stick ????????? ????????? ?????? ???????????? ??????
    # return : True , False
    def Compare_Volume_Average(self, stick) :
        chart = Bithumb.get_candlestick(self.order_currency, payment_currency=self.payment_currency,chart_intervals='1m')
        if(chart is None) :
            return False
        aver_chart = chart.iloc[(stick*-1)-1:-1]
        current_chart = chart.iloc[-1]
        sum = aver_chart['volume'].sum()
        average = sum / len(aver_chart.index)

        before_chart = chart.iloc[-2]

        if(before_chart['close'] - before_chart['open'] > 0) :
            if average * 5 < current_chart['volume'] :
                return True
            else :
                return False
        else :
            return False
    
    def Check_Order_Book(self) :
        order_book = Bithumb.get_orderbook(self.order_currency,payment_currency=self.payment_currency,limit=10)
        buys = order_book['bids']
        sells = order_book['asks']
        if self.Sum_Order_Book(buys) < self.Sum_Order_Book(sells) :
            return True
        return False
    
    def Sum_Order_Book(self, order_book) :
        sum = 0
        for order in order_book :
            sum += order['quantity']
        return sum
    
    # ?????? ?????? API ????????? buy_market_order ?????? ??? 
    # ????????? 100% ????????? ????????????. 
    # ????????? 70%??? ????????? ??? ????????? ????????? ????????? ??????. 
    def order_coin(self) :
        bithumb = Bithumb(self.con_key,self.sec_key)
        units = self.Can_Buy_Coin_Quantity(self.Check_Account())
        units = units * 0.7
        units =  round(units,4)
        order = bithumb.buy_market_order(self.order_currency, units)
        return order

class AI_BitCoin_Seller(AI_Trader) :
    
    def __init(self, order_currency, payment_currency) :
        super(AI_BitCoin_Seller,self).__init(order_currency,payment_currency)
        
        
    def Capture_Large_Increasement(self) :
        current = self.Current_Price()
        before = self.Before_Price()
        percentage_of_value_change = (current - before) / before * 100
        percentage_of_value_change = round(percentage_of_value_change, 2)
        if percentage_of_value_change > 5 :
            return True
        else :
            return False
            
    
    def Before_Price(self) :
        chart = Bithumb.get_candlestick(self.order_currency, payment_currency=self.payment_currency,chart_intervals='1m')
        before_close = chart.iloc[-1]['close']
        return before_close
    
    def Is_Volume_Loss(self) :
        chart = Bithumb.get_candlestick(self.order_currency, payment_currency=self.payment_currency,chart_intervals='1m')
        before = chart.iloc[-2]['volume']
        current = chart.iloc[-1]['volume']
        if (current * 5 < before) :
            return True
        else :
            return False
    
    def Check_Condition(self) :
        if(self.Capture_Large_Increasement()) :
            return True
        if(self.Is_Volume_Loss()) :
            return True
        current = self.Current_Price()
        aver = self.Average_Price()
        if((current - aver) / current < -3) :
           return True        
        return False
    
    def Sell_Coin(self) :
        bithumb = Bithumb(self.con_key, self.sec_key)
        units = bithumb.get_balance(self.order_currency)[0]
        order = bithumb.sell_market_order(order_currency=self.order_currency,payment_currency=self.payment_currency,unit=units)
        return order
        
    
        


'''
1??? ?????? -  0.0001
1~10  - 0.0001
10~100 - 0.01
100~1000 - 0.1
1000~ 5000 - 1
5000~10000 - 5
10000~50000 - 10
50000 ~ 100000 - 50
100000 ~ 500000 - 100
500000~1,000,000 - 500
1,000,000 ~ - 1000 


?????? ??????
??????0 : ?????? ????????? ?????? ?????? ?????? ??????
??????1 : 10??? ????????? ?????? x 400% < ?????? 1??? ????????? (O)
??????2 : 1??? ????????? ????????? ?????? ??? (O)
??????3 : ?????? ????????? ?????? ???????????? ?????? ??? (O)
?????? ??????
??????3 : ?????? ??? ?????? 1?????? 5% ?????? ???????????? ?????? ??? ?????? (O)
??????4 : ??????????????? 1??? ?????? ???????????? ?????? ???????????? ?????? ???. (?????? ???????????? 1??? ??? ???????????? 50%?????? ??????) (O), ???????????????
??????5 : ?????? ?????? 1?????? ???????????? ?????? ?????? 5?????? ?????? ?????? ????????? ??????, ????????? ?????? ?????? ??????(3%) ?????? ??? ?????? (O)
'''

      
      
      