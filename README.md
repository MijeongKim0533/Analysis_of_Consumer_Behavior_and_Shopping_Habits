소비자 행동 및 쇼핑 습관 분석 
=====

### 1. 프로젝트 주제
2024년 봄 시즌 쇼핑몰 매출 증대를 위한 프로모션 구상 및 프로모션 상품 선정
### 2. 분석 목적
1. 개요:  매출 증대를 위해 3가지 형태의 프로모션 방향성을 고려, 가장 효과적인 프로모션을 선정하기 위해 데이터 분석 진행
    -  전체 고객 구매량 강화 프로모션
    -  신규 고객 유입 강화 프로모션
    -  충성 고객 락인(Lock-in) 프로모션
   
2. 목표: 소비자 행동 및 습관 데이터 분석을 기반으로 매출을 효과적으로 상승시킬 프로모션과 상품 도출

### 3. Requirements
```
* Python 3.9+
```

### 4. Installation
```
pip install pandas
pip install matplotlib
pip install plotly
```
### 4. EDA
4.1 패키지 불러오기
```
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
```
4.2 데이터 확인
1) 데이터 소스 : <https://www.kaggle.com/datasets/zeesolver/consumer-behavior-and-shopping-habits-dataset>  
  
2) 데이터 정보 : 총 18 columns, 3900 rows
    ```Customer ID: 고객 아이디
    Age: 고객 나이
    Gender: 고객 성별
    Item Purchased: 구매 상품
    Category: 상품 카테고리
    Purchase Amount (USD): 구매 금액
    Location: 고객 거주 지역
    Size: 상품 사이즈
    Color: 상품 색상
    Season: 구매 시즌
    Review Rating: 리뷰 점수
    Subscription Status: 구독 여부
    Shipping Type: 상품 배송 타입
    Discount Applied: 할인 여부
    Promo Code Used: 프로모션 코드(할인코드) 사용 여부
    Previous Purchased: 고객의 이전 구매 횟수
    Payment Method: 지불 방법
    Frequency of Purchases: 구매 빈도
    ```  
    <br/>
4.3 Null 확인 : Null이나 Null 대신 대체값으로 채워진 행 없음
   
  <img width="400" alt="스크린샷 2024-03-25 오전 10 09 42" src="https://github.com/MijeongKim0533/PJ_Funnel_Analysis/assets/152786534/cc9fd251-6a57-4375-8572-a2ed714b0157"><br/><br/>



4.4 이상치 확인 : 수치형 컬럼 중 이상치 없음
      ![newplot](https://github.com/MijeongKim0533/PJ_Funnel_Analysis/assets/152786534/b29e3da2-a504-4639-8bc6-a880c502a5b2)
  
4.5 상관관계 확인
- 수치형 컬럼 생성 : 상관관계를 보기 위해 범주형 컬럼을 수치형으로 변경하여 컬럼 생성
  ```
  def frequency_to_num(frequency_of_purchases):
    
      if frequency_of_purchases == 'Weekly':
        return 5
      elif frequency_of_purchases in ['Fortnightly', 'Bi-Weekly']:
        return 4
      elif frequency_of_purchases == 'Monthly':
        return 3
      elif frequency_of_purchases in ['Every 3 Months', 'Quarterly']:
        return 2
      else:
        return 1
  ```
  ```
  df['frequency_of_purchases'] = df['Frequency of Purchases'].apply(frequency_to_num)
  ```
 - Subscription Status, Discount Applied, Gender 3개의 컬럼이 서로 상관관계가 높게 나옴  
  
   - Subscription Status - Discount Applied : 0.7 
   - Gender - Discount Applied : -0.6 
   - Gender - Subscription Status : -0.42  
    
        ![newplot (1)](https://github.com/MijeongKim0533/PJ_Funnel_Analysis/assets/152786534/4ebbaa23-41bb-4e2b-af83-60c29e2caa0d)

4.6 컬럼별 분석
1) 성별 고객 수 및 비율  
```
# 고객 남녀 수 그래프

fig = px.bar(df_gender_count, x=df_gender_count.index, y=df_gender_count.values, 
             title='Count of Customers by Gender',
             color=df_gender_count.index,
             color_discrete_sequence=['royalblue', 'tomato'],
             text=df_gender_count.values)  

fig.update_traces(texttemplate='%{y:,.0f}', textposition='outside')  

fig.update_layout(
    xaxis_title='',  
    yaxis_title='count',  
    width=600,  
    height=500,
    plot_bgcolor='white'
)

fig.update_layout(showlegend=False)

fig.show()
```

<div style="display: flex; justify-content: center; align-items: center;">
    <img src="https://github.com/MijeongKim0533/PJ_Funnel_Analysis/assets/152786534/f3745c1e-5ba5-4855-b603-a0d177c93339" width="360" height="330">
    <img src="https://github.com/MijeongKim0533/PJ_Funnel_Analysis/assets/152786534/6cd41a25-16a8-4459-a382-78185d80198f" width="360" height="245">
</div>

2) 연령별 고객 수　　　　　　　　　　　　　　　　　　　　3. 리뷰점수 분포   
<img src="https://github.com/MijeongKim0533/PJ_Funnel_Analysis/assets/152786534/c7d121c3-321d-46d3-95f8-af23c5307010" width="360" height="300"><img src="https://github.com/MijeongKim0533/PJ_Funnel_Analysis/assets/152786534/1ce12c0e-eaa7-4cdd-9e5c-9484990cea71" width="360" height="300">

4. 사이즈별 판매량 　　　　　　　　　　　　　　　　　　　　5. Payment Method별 거래수 
<img src="https://github.com/MijeongKim0533/PJ_Funnel_Analysis/assets/152786534/f5a096f9-f4e2-445d-b7af-e7082ba940ad" width="360" height="300"><img src="https://github.com/MijeongKim0533/PJ_Funnel_Analysis/assets/152786534/18210fa7-2825-4bc9-9c94-90334a145aa9" width="360" height="300">

6. Location별 판매량
<img src="https://github.com/MijeongKim0533/PJ_Funnel_Analysis/assets/152786534/f52e5268-3596-4dd6-bec5-fe31e5f2302e">


### 4. 심층 분석
  1. 프로모션 타겟 선정을 위한 분석 : 매출이 높은 고객층 찾기(고객 분석 및 segmentation)
- 전체 고객 객단가 및 중앙값
  
  <img src="https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/07e35cf4-508d-4ada-a5ad-376968b89826" width="400" height="420">

- __일반고객-VIP고객 segmentation__
  ```
  <고객 segmentation 기준>

  Frequency of Purchases 컬럼을 기준으로 앞으로 1년동안의 구매횟수를 추정. 
  추정 구매횟수가 26회 이상인 고객을 VIP, 미만은 Regular 고객으로 분류

  Previous Purchases 컬럼이 있지만 기준이 되는 날이 없어
  ```
  일반고객과 VIP고객의 객단가는 거의 비슷. 같다고 봐도 무방해 보인다.   

  <img src="https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/24296243-500b-4725-a9fe-ee42c7e0bce7" width="330" height="330">

- __일반고객-VIP고객 예상 매출액 비교__
  ```
  1년 예상 매출액 = 객단가 * 연간 예상 구매횟수(Frequency of Purchases 컬럼을 기준으로 예상 구매횟수 예측)
  ```  
  일반고객과 VIP고객의 객단가는 차이가 거의 없었으나 구매 빈도에서 차이가 많이 났다. 그래서 Frequency of Purchases컬럼을 바탕으로 1년 동안의 예상 구매횟수를 추측하여 1년 예상 매출액을 예측해보았다. 그 결과 VIP고객이 일반고객보다 4배 이상 매출을 가져다 줄 것으로 예측되었다.
  
  <img src="https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/11c1cff4-7623-4ed1-9a11-04837b9236d7" width="330" height="330">&nbsp;&nbsp;
  <img src="https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/56eaf4f2-4ccb-4e3a-baaf-efa8b2bc6ff6" width="330" height="330">

- __일반고객-VIP고객 비율__  
  일반고객과 VIP고객의 비율을 살펴보면 6:4 정도의 비율임을 알 수 있다.

  <img src="https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/b7f8caa9-a110-4f7c-8d4f-dc1af29d0d1c" width="330" height="330">&nbsp;&nbsp;
  <img src="https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/617563fa-9fd3-467e-9500-afd84d64f545" width="330" height="330">
  ```
  :mag_right: VIP고객은 전체고객의 40% 정도이지만 예상매출액은 일반고객의 4배가 넘는다. 
  프로모션은 VIP고객을 대상으로 하는 것이 매출증대에 효과적일 것이라 예상된다.
  ```
 --- 
  

__2) 적합한 프로모션 선정을 위한 분석 : 할인 VS 인기상품__  
  
- __매출액, 할인적용, 구매빈도 컬럼의 상관계수 확인__  
  할인 프로모션을 하는 것이 타당한지 보기 위해 매출액(Purchase Amount), 할인적용(discount_applied), 구매빈도(purchases_times_per_annual)컬럼간의 상관계수를 확인해 보았으나 상관관계가 없는 것으로 보인다.   
  
   <img src="https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/d6726164-411f-45f7-9a6b-a27a4879c9d1">
  
- __일반고객-VIP고객 그룹핑 후 상관계수 확인__  
  전체고객을 대상으로 상관계수를 확인했을 때 상관관계가 있어보이지 않았다. 심슨의 역설이 생길 수 있으니 일반고객과 VIP고객으로 그룹핑 한 후 상관관계가 있는지 확인해 보았다.    

  __[VIP고객]__  
  <img src="https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/8d4ee813-fc2d-42e0-ac84-c0fe602f3680">

  __[일반고객]__  
  <img src="https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/84a8cee0-a6aa-4fe9-baf1-b0c1f99368bf">
  ```
  :mag_right: 일반고객과 VIP고객으로 그룹핑한 후 상관계수를 확인한 결과 약간의 변화는 있었지만 매출, 할인적용, 구매빈도 간의 상관관계는 있어보이지 않았다. 때문에 할인 프로모션은 매출증대에 효과적으로 보이지 않아 고객들이 많이 찾는 인기상품들로 프로모션을 진행하는 것이 낫다고 판단했다.
  ```
---
__3) 프로모션 상품 선정을 위한 분석__  
앞에서 VIP를 대상으로 지금까지 많이 판매된 상품들로 프로모션을 진행하는 것이 매출증대에 효과적으로 판단되어 그동안 VIP가 많이 구매한 상품들을 남녀로 나누어 분석  

- 봄시즌 남성 VIP 구입 아이템 순위  
  Sweater, Shorts, Gloves 가 VIP남성 고객이 봄에 가장 많이 구매한 아이템이었다.
  <img src="https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/40a980ac-f385-4571-b522-4f8d666a661d">

- 봄시즌 여성 VIP 구입 아이템 순위  
  Boots가 VIP여성 고객이 봄에 가장 많이 구매한 아이템이었다.
  <img src="https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/b4753a39-259b-470e-b7a7-e2281141811a">
---


### 5. 결론
VIP들의 객단가는 일반고객과 다르지 않다. 매출을 늘리기 위해서는 방문횟수를 더 늘리던가 객단가를 올리는 방법뿐이다. 제품 디스플레이 를 좀더 짧은 주기로 바꿔 VIP고객들이 호기심을 가지고 더 많이 방문하도록 하여 매출을 늘리는 방법이 어떤가 한다. 물론 다양한 제품을 더 가져다 놓는다는 것은 안 팔릴 수도 있다는 리스크를 감안해야 하지만 고객들의 방문횟수를 늘리면 분명 매출이 증가할 것이라고 생각한다. 그래서 프로모션은 VIP를 대상으로  

### 6. 느낀점
데이터 선정에 시간을 더 많이 투자해야겠다. 
   



  
  
  
  
