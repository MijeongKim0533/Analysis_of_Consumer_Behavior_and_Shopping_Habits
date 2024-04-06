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
pip install scikit-learn
```
### 5. EDA
#### 5.1 패키지 불러오기
```
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
```
#### 5.2 데이터 확인
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
3)  Null 확인 : Null값 없음  
  
    <img width="400" alt="스크린샷 2024-03-25 오전 10 09 42" src="https://github.com/MijeongKim0533/PJ_Funnel_Analysis/assets/152786534/cc9fd251-6a57-4375-8572-a2ed714b0157"><br/><br/>  
   
4) 대체값 확인 : Null 대신 0이나 1과 같은 다른 값으로 대체된 곳이 있는지 확인. index 역할을 하는 Customer ID 컬럼을 제외하고 0, 1인 값 없음
    ```
    # 0이나 1인 값이 있는지 확인

    for column in df.columns:
        print(column, ':', (df[column] == 0).any())


    for column in df.columns:
        print(column, ':', (df[column] == 1).any())
    ```  

    <img width="243" alt="image" src="https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/ea2e7fa7-9bbe-4b78-bf50-d39b4e61a06d"><br/>
  
   

#### 5.3 이상치 확인 : 수치형 컬럼 중 이상치 없음
```
# 수치형 변수 이상치 확인

fig = go.Figure()

fig.add_trace(go.Box(y=df['Purchase Amount (USD)'], name='Purchase Amount (USD)'))
fig.add_trace(go.Box(y=df['Review Rating'], name='Review Rating'))
fig.add_trace(go.Box(y=df['Previous Purchases'], name='Previous Purchases'))
fig.add_trace(go.Box(y=df['Age'], name='Age'))

fig.update_layout(title='Boxplot of Numeric Columns',
                  xaxis=dict(title=''),
                  yaxis=dict(title='Value'),
                  width=800,  
                  height=500)  

fig.update_layout(showlegend=False)

fig.show()
```
  <img src="https://github.com/MijeongKim0533/PJ_Funnel_Analysis/assets/152786534/b29e3da2-a504-4639-8bc6-a880c502a5b2" width="750" height="480">

  
#### 5.4 상관관계 확인
- 수치형 컬럼 생성 : 상관관계를 보기 위해 범주형 컬럼을 수치형으로 변경하여 컬럼 생성
- Subscription Status, Discount Applied, Gender 3개의 컬럼이 서로 상관관계가 높게 나옴  
  
   - Subscription Status - Discount Applied : 0.7 
   - Gender - Discount Applied : -0.6 
   - Gender - Subscription Status : -0.42  
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

    
    ![newplot (1)](https://github.com/MijeongKim0533/PJ_Funnel_Analysis/assets/152786534/4ebbaa23-41bb-4e2b-af83-60c29e2caa0d)

#### 5.5 컬럼별 분석
1) 성별 고객 수 및 비율<br/>
  
   데이터를 바탕으로 보았을 때 고객의 비율은 남성이 68%, 여성이 32%, 약 7:3 정도로 남성고객의 비율이 높다.
   
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

2) 연령대별 고객 수<br/>
  
    10대, 70대를 제외하고 연령대별 비슷한 고객수를 보임.<br/>

    ```
    # 고객 연령대 확인

    df_by_agegroup = df['age_group'].value_counts().sort_index()

    # 고객 연령대별 판매량 그래프

    fig = px.bar(df_by_agegroup, x=df_by_agegroup.index, y=df_by_agegroup.values, 
                title='Count of Customers by Age Group',
                color=df_by_agegroup.index,
                color_discrete_sequence=px.colors.sequential.GnBu[2:],
                text=df_by_agegroup.values)  

    fig.update_traces(textposition='outside')  

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
    <img src="https://github.com/MijeongKim0533/PJ_Funnel_Analysis/assets/152786534/c7d121c3-321d-46d3-95f8-af23c5307010" width="500" height="380">


  3) 리뷰점수 분포<br/>
   
      2.5점~5점 사이에 리뷰점수가 분포하고 있고 점수들의 분포가 비교적 고르다.
      ```
      fig = px.histogram(df, x='Review Rating', nbins=50, 
                        title='Review Score Distribution',
                        color_discrete_sequence=[px.colors.sequential.GnBu[5]])

      fig.update_layout(width=600,  
                        height=500,
                        plot_bgcolor='white')  

      fig.show() 
      ```
    
      <img src="https://github.com/MijeongKim0533/PJ_Funnel_Analysis/assets/152786534/1ce12c0e-eaa7-4cdd-9e5c-9484990cea71" width="500" height="380">

   4. [사이즈별 판매량](https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/blob/main/Analysis_of_Consumer_Behavior_and_Shopping_Habits_ver8.ipynb)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;       5. [Payment Method별 거래수](https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/blob/main/Analysis_of_Consumer_Behavior_and_Shopping_Habits_ver8.ipynb)   
<img src="https://github.com/MijeongKim0533/PJ_Funnel_Analysis/assets/152786534/f5a096f9-f4e2-445d-b7af-e7082ba940ad" width="360" height="300"><img src="https://github.com/MijeongKim0533/PJ_Funnel_Analysis/assets/152786534/18210fa7-2825-4bc9-9c94-90334a145aa9" width="360" height="300">   

   6) [지역별 판매량](https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/blob/main/Analysis_of_Consumer_Behavior_and_Shopping_Habits_ver8.ipynb) 

<img src="https://github.com/MijeongKim0533/PJ_Funnel_Analysis/assets/152786534/f52e5268-3596-4dd6-bec5-fe31e5f2302e">


### 6. 심층 분석
#### 1. 할인 여부와 매출의 상관관계
- 상관계수 확인 : 할인적용 유무와 구매금액의 상관계수는 -0.0178로 관계가 없음<br/> &rarr; 심슨의 역설이 생길 수 있으므로 고객을 분류한 후 다시 체크
  
    ```
    corr2 = df[['Purchase Amount (USD)', 'discount_applied']].corr(method='pearson')

    fig = px.imshow(corr2.values,
                x=corr2.columns,
                y=corr2.index,
                text_auto = '.4f',
                color_continuous_scale=px.colors.sequential.GnBu[2:],
                color_continuous_midpoint=0,
                title='Correlation Heatmap')

    fig.update_layout(
        width=400,
        height=300,
        margin=dict(l=0, r=0, t=40, b=0),
    )

    fig.show()
    ```
    ![image](https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/94f51b41-3bd0-4ad6-a2e2-32e646990b33)

#### 2. 고객 분류하기
  1) 분류 기준 찾기<br/>
    고객을 분류하려면 기준을 정해야 하는데 해당 데이터셋에는 한계점이 존재.<br/> 
    일정 기간동안의 고객의 구매내역을 보여주는 것이 아니라 고객의 마지막 구매내역만 보여주어 매출파악이 어렵다. 또, 구매 시점에 대한 정보도 없어 해당 데이터셋으로는 정확한 매출을 측정하기 어렵다고 판단.<br/> 보통 고객을 분류할 때 매출을 기준으로 판단하는데 해당 데이터셋은 고객별 정확한 매출을 측정하기 어려우므로  이전 구매횟수 컬럼과 평균 매출을 이용하여 대략적인 매출을 추측했다. 그러나 이전구매횟수도 고객이 가입일 이후 구매한 횟수를 말하는 것인지 1년동안 구매한 횟수를 말하는 것인지 알 수 없어 정확한 판단을 내리기 어려웠다. 그래서 이번 프로젝트에서는 1년동안 구매한 횟수를 의미한다고 생각하고 분석을 진행하였다. 
- 히스토그램 : 이전 구매횟수를 기준으로 했을 때 고객층을 나눌만한 뚜렷한 지점이 없어보임
  ```
  fig = px.histogram(df, x='Previous Purchases', nbins=50)

  fig.update_layout(
      width=600,  
      height=400,  
  )
  fig.show()
  ```
  ![image](https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/00e68f88-9540-4d79-b833-9adcf6625df1)
- k-means 알고리즘: 알고리즘으로 클러스터링을 시도했으나 데이터셋 한계로 클러스터링 결과가 타당해 보이지 않아 제외<br/><br/>
  [클러스터링 개수에 따른 실루엣 계수](https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/blob/main/kmeans_visual.py) 
  <img width="1106" alt="image" src="https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/bec63516-0122-448c-8366-a8d3a9286c52"><br/><br/>
  &rarr; 2개 그룹으로 클러스터링을 했을 때 실루엣 계수가 가장 높아 그래프 확인해 보니 Purchase Amount컬럼이 그룹핑의 기준이 된 것을 알 수 있었다. 하지만 데이터셋에서 Purchase Amout가 의미하는 것이 마지막으로 구매한 상품 1건을 의미해서 단순하게 이 하나의 컬럼만으로 고객을 분류하는 것은 타당하지 않다고 판단했다.
  
  ```
  X_features = df[['Previous Purchases', 'Purchase Amount (USD)']]

  kmeans = KMeans(n_clusters=2)
  kmeans.fit(X_features)

  df['segmentation'] = kmeans.predict(X_features)

  # 그래프
  centers = kmeans.cluster_centers_
  colors = ['blue' if label == 0 else 'red' for label in df['segmentation']]
  plt.scatter(df['Previous Purchases'], df['Purchase Amount (USD)'], c=colors, alpha=0.5)
  plt.scatter(centers[:, 0], centers[:, 1], marker='o', c='black', s=100, alpha=0.5)
  plt.xlabel('Previous Purchases')
  plt.ylabel('Purchase Amount (USD)')
  plt.title('K-Means Clustering Result')
  plt.show()
  ```
  <img src="https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/bc0f1fd3-3651-4a34-bd19-f7bbc63fcb93" width="550" height="400"><br/><br/>

  **&rarr; 구매횟수를 기준으로 고객을 분류하기로 결정. 구매횟수가 30회 초과하면 충성고객, 이하는 일반고객으로 분류**<br/><br/>
2. 고객 분류
- 새로운 컬럼 생성 : 
  이전 구매 횟수가 30회 초과하는 고객들은 충성고객, 이하는 일반고객으로 분류함.
  ```
  # 고객분류 함수
  def customer_re_grouping(previous_purchases):
    if previous_purchases > 30:
        return 'Royal'
    else:
        return 'Regular'

  # 컬럼 생성
  df['customer_class'] = df['Previous Purchases'].apply(customer_re_grouping)
  ```
  <br/>

#### 3. 새로 분류한 고객 그룹별 할인여부와 매출 상관관계 확인
고객 그룹별로 나눠 상관관계를 보아도 상관계수가 매우 낮아 두 컬럼간에는 관계가 없어 처음 생각했던 프로모션 계획중 할인 프로모션은 제외하기로 결정
```
df_by_royal = df[df['customer_class'] == 'Royal']
corr3 = df_by_royal[['Purchase Amount (USD)', 'discount_applied']].corr(method='pearson')

df_by_regular = df[df['customer_class'] == 'Regular']
corr5 = df_by_regular[['Purchase Amount (USD)', 'discount_applied']].corr(method='pearson')

# 히트맵 그래프
fig = px.imshow(corr3.values,
                x=corr3.columns,
                y=corr3.index,
                text_auto = '.4f',
                color_continuous_scale=px.colors.sequential.GnBu[2:],
                color_continuous_midpoint=0,
                title='Correlation Heatmap')

fig.update_layout(
    width=400,
    height=300,
    margin=dict(l=0, r=0, t=40, b=0),
)

fig.show()
```
<br/>
&nbsp;&nbsp;&nbsp;<충성고객>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<일반고객><br/><br/>
<img src="https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/6e500e5c-0acc-4c03-a79c-8790fc5c17d4" width="380" height="300"><img src=https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/6a685805-7044-4173-9a48-b3485248133c width="390" height="300">

#### 4. 예상 매출액 예측










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
   



  
  
  
  
