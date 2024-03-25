# 필요한 라이브러리 불러오기
import pandas as pd
import plotly.express as px
import streamlit as st

# 데이터 파일 불러오기
df = pd.read_csv('shopping_behavior_updated.csv')

# 여기서부터 데이터 전처리 및 시각화 코드 작성

def gender_to_num(gender):
    if gender == 'Male':
        return 0
    else:
        return 1

df['gender'] = df['Gender'].apply(gender_to_num)

def subscription_to_num(subscription_status):
    if subscription_status == 'No':
        return 0
    else:
        return 1
    
df['subscription_status'] = df['Subscription Status'].apply(subscription_to_num)

def discount_to_num(discount_applied):
    if discount_applied == 'No':
        return 0
    else:
        return 1
    
df['discount_applied'] = df['Discount Applied'].apply(discount_to_num)

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
    
df['frequency_of_purchases'] = df['Frequency of Purchases'].apply(frequency_to_num)

def age_cat(age):
    return str((age//10) * 10) + '대'
  
df['age_group'] = df['Age'].apply(age_cat)  

# Streamlit 앱 구성
st.title('Shopping Behavior Analysis Dashboard')


# 1. 성별 고객 수 

df_gender_count =df['Gender'].value_counts().sort_values(ascending=False)

fig = px.bar(df_gender_count, x=df_gender_count.index, y=df_gender_count.values, 
             title='Count of Customers by Gender',
             color=df_gender_count.index,
             color_discrete_sequence=['royalblue', 'tomato'],
             text=df_gender_count.values)  

fig.update_traces(texttemplate='%{y:,.0f}', textposition='outside')  

fig.update_layout(
    xaxis_title='',  
    yaxis_title='Count',  
    width=600,  
    height=500,
    #plot_bgcolor='white'
)

st.plotly_chart(fig)

# 2. 고객 성비

df_gender = df['Gender'].value_counts().sort_values(ascending=False)/df['Customer ID'].count()*100

fig2 = px.pie(df_gender, values=df_gender, names=df_gender.index,
             title='Gender Ratio', color_discrete_sequence=['royalblue', 'tomato'],  
             hole=0.3)

fig2.update_layout(
    width=600,  
    height=400,  
)

st.plotly_chart(fig2)

# 3. 고객 연령대

df_by_agegroup = df['age_group'].value_counts().sort_index()

fig3 = px.bar(df_by_agegroup, x=df_by_agegroup.index, y=df_by_agegroup.values, 
             title='Count of Customers by Age Group',
             color=df_by_agegroup.index,
             color_discrete_sequence=px.colors.sequential.GnBu[2:],
             text=df_by_agegroup.values)  

fig3.update_traces(textposition='outside')  

fig3.update_layout(
    xaxis_title='',
    yaxis_title='count', 
    width=600, 
    height=500,
    #plot_bgcolor='white'
)
fig3.update_layout(showlegend=False)

st.plotly_chart(fig3)


