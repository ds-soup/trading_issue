

## 시세 참고. 
https://coinmarketcap.com/ko/tokens/
https://www.coingecko.com/ko/categories/analytics?category_id=augmented-reality



## 3일차
    1. DB에 Bithumb 상장 코인들 리스트 등록
    2. 섹터별 코인들 DB에 등록
    3. 해당 섹터에서 Bithumb에 상장되어 있는 코인들 조회하는 로직


## 4,5일차
    1. 거래량, 호가창 관련 매수 / 매도 로직 구현
    2. 현재 잔고 상황에 따라 유동적으로 판단하는 로직 구현
### 코인 탐색 (AI_Explore_Coin)
    -유망 섹터를 판단해 코인을 찾는다.
    -해당 섹터에 있는 코인이 bithumb에 상장되어 있는지 비교한다.
    -해당 코인들에게 가중치 +1 을 부여한다.
    -해당 섹터의 코인 중 조건식에 부합하는 코인을 찾는다.
    -해당 코인들에게 가중치 +5 를 부여한다.
### 코인 매수(AI_BitCoin_Bidder)
    -현재 계좌의 남아있는 잔고를 확인한다.
    -잔고가 남아있다면 가중치를 부여한 코인을 구매할 수 있는지 조회한다
        구매할 수 없다면 해당 클래스는 종료된다.
    -해당 코인을 가중치를 적용하여 수량을 구매한다.
### 코인 매도(AI_BitCoin_Seller)
    -현재 매수된 코인을 모니터링하는 클래스를 만든다.
    -조건식에 부합하면 팔 수 있는 코인을 처분한다.
    -매도는 전량매도를 기본 원칙으로 구현한다.

## 6일차
    1. 클래스 구현은 완료.
    2. main 스트림 작업 




























