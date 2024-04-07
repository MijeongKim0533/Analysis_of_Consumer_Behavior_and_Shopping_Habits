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
    ```
    Customer ID: 고객 아이디
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

#### 4. 예상 매출액 
  1. 전체 고객의 평균 구매금액 및 중앙값<br/>
      ```
      sales_df = df['Purchase Amount (USD)'].agg(['mean', 'median'])

      fig = px.bar(sales_df, x=sales_df.index, y=sales_df.values,
                title='Average & Median Purchase Amount',
                color=sales_df.index, 
                color_discrete_sequence=['silver'])

      fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')  

      fig.update_layout(
          xaxis_title='', 
          yaxis_title='Purchase Amount (USD)',    
          width=400,  
          height=500,
          showlegend=False, 
          plot_bgcolor='white')

      fig.show()
      ```
      <img src="https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/07e35cf4-508d-4ada-a5ad-376968b89826" width="400" height="420">

  2. 충성고객-일반고객 비율 및 평균 구매금액<br/>
   - 충성고객-일반고객 비율 : 충성고객이 약 40%, 일반고객이 60% 정도를 차지<br/>
      <img src=https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/0224d3d7-9211-402a-a20b-75acfcb46828 width="340" height="360">
      <img src=https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/e1084655-7b8e-4959-a375-4dbd6caa32ca width="390" height="260">
  - 충성고객-일반고객 그룹별 평균 구매금액 : 
    그룹별로 평균단가에서 차이가 있을 것이라고 예상했지만 차이가 거의 없음<br/>
      ```
      # 그룹별 평균 금액
      df_by_class_USD = df.groupby('customer_class')['Purchase Amount (USD)'].mean()

      # 그래프
      fig = px.bar(df_by_class_USD, x=df_by_class_USD.index, y=df_by_class_USD.values,
                title='Average Order Value by Customer Type',
                color=df_by_class_USD.index, 
                color_discrete_sequence=['silver', 'gold'])

      fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')  

      fig.update_layout(
          xaxis_title='', 
          yaxis_title='Average Order Value (USD)',    
          width=400,  
          height=500,
          showlegend=False, 
          plot_bgcolor='white')

      fig.show()
      ```

      
      <img src=https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/bcec1c75-1bd3-4b29-bec1-796811ea2c2d width="400" height="420">

  1. 예상매출액 계산하기<br/>

   - 새로운 컬럼 생성 : 고객별로 이전구매횟수와 평균 구매단가를 곱하여 예상 매출액 컬럼 생성<br/><br/>
      ```
      def get_profit_column(customer_class):

        if customer_class == 'Regular':
            return 59.6 * 15
        else:
            return 60 * 40

      df['expected_sales'] = df['customer_class'].apply(get_profit_column)
      ```
      <br/>
   - 예상 매출액 계산<br/>
      
      **예상 매출액 = 평균 객단가 x 이전 구매횟수** 
      
      ```
      expected_sales_df = df.groupby("customer_class")["expected_sales"].sum()

      fig = px.bar(expected_sales_df, x=expected_sales_df.index, y=expected_sales_df.values,
             title='Sales Projection by Customer Class',
             color=expected_sales_df.index, 
             color_discrete_sequence=['silver', 'gold'])

      fig.update_traces(texttemplate='%{y:,.0f}', textposition='outside')  

      fig.update_layout(
          xaxis_title='', 
          yaxis_title='Projected Sales (USD)',    
          width=400,  
          height=500,
          showlegend=False, 
          plot_bgcolor='white')

      fig.show()
      ```
      <img src=https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/ef3ae8e8-4fbd-47da-8ced-1b15e6d45454 width="340" height="360"><img src=https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/80018cf2-96d5-45a4-b3a5-107a8f18d501 width="390" height="260"><br/>

  **&rarr; 전체 고객의 약 40%를 차지하는 충성고객이 매출의 약 64%를 올려줄 것이라고 예상됨**<br/>
  **&rarr; 충성고객이 매출의 많은 부분을 차지할 것으로 예상되므로 충성고객을 대상으로 프로모션을 진행하는 것이 타당해 보임**

### 7. 프로모션 전략 세우기
1) 충성고객 분석
- 연령대 : 50대 고객이 다른 연령대보다 조금 더 많음
  ```
  # 충성고객만 데이터 분리
  df_by_royal = df[df['customer_class']=='Royal']

  # 연령대별 충성고객 수 확인
  df_by_royal_age = df_by_royal['age_group'].value_counts().sort_index()

  # 그래프
  fig = px.bar(df_by_royal_age, x=df_by_royal_age.index, y='count',
             title='Sales Count by Age (Royal)',
             color=df_by_royal_age.index,  
             color_discrete_sequence=px.colors.sequential.GnBu[2:])

  fig.update_traces(texttemplate='%{y:.0f}', textposition='outside')  

  fig.update_layout(
      xaxis_title='', 
      yaxis_title='count',   
      width=600,  
      height=500,
      showlegend=False, 
      plot_bgcolor='white')

  fig.show()
  ```
  <img src=https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/3b22abb7-0079-492c-b1dc-62a995c2f647 width="600" height="400"><br/>

- 성별에 따른 구매 아이템<br/>
  지난 봄 시즌 남성 충성고객과 여성 충성고객이 가장 많이 구매한 아이템 top5 확인<br/>
  &rarr; 성별에 따라 많이 구매한 아이템 순위가 달랐다. 여기서 흥미로웠던 점은 남성고객의 구매 아이템 top5에 드레스와 쥬얼리가 1, 2위를 차지한 점이다. 이를 통해 남성의 경우 아내나 여자친구에게 선물용으로 구매를 많이 한다고 추측하였다.
  ```
  # 남성 충성고객
  df_by_spring_royal_men = df[(df['Season']=='Spring') & (df['customer_class']=='Royal') & (df['Gender']=='Male')]
  df_by_spring_royal_men_item = df_by_spring_royal_men['Item Purchased'].value_counts().sort_values(ascending=False)

  # 여성 충성고객
  df_by_spring_royal_women = df[(df['Season']=='Spring') & (df['customer_class']=='Royal') & (df['Gender']=='Female')]
  df_by_spring_royal_women_item = df_by_spring_royal_women['Item Purchased'].value_counts().sort_values(ascending=False)
  ```
  <img src=https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/9648f0ee-da24-45d2-8ce3-1a90ea86bfcf width="600" height="400"><br/>
  <img src=https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/79309342-4afe-4e10-86c6-2b6ba085bf2d width="600" height="400">
    |성별|구매 아이템|
    |------|---|
    |남성|Dress > Jewelry > T-shirt > Cloves > Sweater|
    |여성|Blouse > Shirt > Shoes > Handbag > Hoodie = Sandals = Dress|
<br/>

2) 프로모션 선택
- 선택 프로모션 : 충성고객 락인(lock-in) 프로모션
- 전략 : 충성고객이 많이 구매했던 아이템을 배치 및 홍보

### 8. 결론
#### '여성을 위한 선물용 상품' 으로 프로모션을 계획
남성 충성 고객의 봄시즌 주요 구매 상품은 '드레스, 쥬얼리'👗💍 <br/> 
'여성을 위한 선물용 상품'으로 프로모션을 진행할 경우, 남성 충성고객과 여성고객에게 모두 어필이 될 수 있다고 예상.<br/><br/>
추가적으로 시즌성 이벤트인 '화이트데이' 선물 프로모션을 진행할 경우, 남성 충성 고객의 구매 유도에 긍정적 영향을 줄 것.<br/>선물 상품 외 일반 상품도 추가한다면, 여성 고객의 유입을 통해 전체 매출 상승에 기여 가능할 것

<img src=https://github.com/MijeongKim0533/Analysis_of_Consumer_Behavior_and_Shopping_Habits/assets/152786534/8bf522b7-23d4-4f1e-baa4-e5cd4f8c0be0 width="500" height="250">

  




   



  
  
  
  
