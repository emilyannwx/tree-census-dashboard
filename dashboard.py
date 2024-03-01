import pandas as pd 
import os
import streamlit as st 
import plotly.express as px
import altair as alt 
from numerize.numerize import numerize 





st.set_page_config(page_title ='Tree Dashboard',
                   layout = 'wide',
                   initial_sidebar_state='expanded')

@st.cache_data
def get_data():
    df = pd.read_csv('tree-census-combined.csv', low_memory=False)
    return df

df = get_data()
header_left, header_mid, header_right = st.columns([1,3,1],gap = 'large')

with header_mid:
    st.title('Tree Dashboard')

with st.sidebar:
    Borough_filter = st.multiselect(label= 'Select a Borough',
                                  options=df['borough'].unique(),
                                  default = df['borough'].unique())
    
    Artist_filter = st.multiselect(label= 'Select an District',
                                  options=df['Artist'].unique(),
                                  default = df['Artist'].unique())
    

    
    df1 = df.query ('Artist == @Artist_filter & Year == @Year_filter & Genre == @Genre_filter')

df1['Duration (minutes)'] = pd.to_numeric(df['Duration (minutes)'], errors='coerce')
df1['Spotify Streams (millions)'] = pd.to_numeric(df['Spotify Streams (millions)'], errors='coerce')
df1['Album Sales (millions)'] = pd.to_numeric(df['Album Sales (millions)'], errors='coerce')
df1['YouTube Views (millions)'] = pd.to_numeric(df['YouTube Views (millions)'], errors='coerce')
df1['Popularity'] = pd.to_numeric(df['Popularity'], errors='coerce')

total_streams = float(df1['Spotify Streams (millions)'].sum())
total_sales = float(df1['Album Sales (millions)'].sum())
total_views = float(df1['YouTube Views (millions)'].sum())
#average_duration= float(df1['Duration (minutes)'].sum()) 
average_popularity = float(df1['Popularity'].mean())


total1,total2,total3,total4,total5 = st.columns(5,gap='large')

with total1:
    st.image('images/distribution.png',width = 300 ,use_column_width='Auto')
    st.metric(label = 'Total Spotify Streams', value= numerize(total_streams))
    
with total2:
    st.image('images/album.png',width = 300, use_column_width=25)
    st.metric(label='Total Album Sales', value=numerize(total_sales))

with total3:
    st.image('images/youtube.png',width = 300, use_column_width=300)
    st.metric(label= 'Total Youtube Views',value=numerize(total_views,2))

#
with total5:
    st.image('images/subscriber.png',width = 300, use_column_width=300)
    st.metric(label='Average Popularity Rating',value=numerize(average_popularity))

st.metric("Total Streams", f"{total_streams:.2f} million")

chart = alt.Chart(df1).mark_bar().encode(
    x='Song',
    y='Spotify Streams (millions)'
).properties(
    width=600,
    height=400
)

st.altair_chart(chart, use_container_width=True)


st.title('Genre Popularity Comparison')

chart = alt.Chart(df1).mark_bar().encode(
    x='Genre',
    y='Popularity'
).properties(
    width=600,
    height=400
)

st.altair_chart(chart, use_container_width=True)

