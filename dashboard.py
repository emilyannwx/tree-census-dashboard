import pandas as pd 
import os
import streamlit as st 
import plotly.express as px
import altair as alt 
from numerize.numerize import numerize 



st.set_page_config(page_title ='Tree Dashboard',
                   layout = 'wide',
                   initial_sidebar_state='expanded')

custom_css = """
<style>
body {
    background-color: #f0f2f6; /* light gray */
}

.stTextInput>div>div>input {
    color: #333; /* dark gray */
}

.stButton>button {
    background-color: #4CAF50; /* green */
    color: white; /* white text */
}
.css-1l02zno {
    background-color: #333; /* dark gray */
    color: white; /* white text */
}

.css-vfdix6 {
    background-color: #4CAF50; /* green */
    color: white; /* white text */
}

.css-1gceuu2 {
    color: #4CAF50; /* green */
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

@st.cache_data
def get_data():
    df = pd.read_csv('data/2015_Street_Tree_Census_1.csv', low_memory=False)
    return df

df = get_data()
header_left, header_mid, header_right = st.columns([1,3,1],gap = 'large')

with header_mid:
    st.title('NYC Tree Dashboard')

with st.sidebar:
    Borough_filter = st.multiselect(label= 'Select a Borough',
                                  options= df["borough"].unique())    
    Health_filter = st.multiselect(label= 'Select the Tree Health',
                                  options=df['health'].unique())
    Status_filter = st.multiselect(label= 'Select the Tree Status',
                                  options=df['status'].unique())
    Species_filter = st.multiselect(label= 'Select the Tree Species',
                                  options= df["spc_common"].unique())
          

    df1 = df.query ('borough == @Borough_filter  & health == @Health_filter & status == @Status_filter')
    df2 = df.query ('borough == @Borough_filter & spc_common == @Species_filter')


st.map(df1, size=20, latitude= 'latitude', longitude = 'longitude',color='#899878')

tree_count = df1['borough'].value_counts()

chart = alt.Chart(df2).mark_bar().encode(
    x='spc_common',
    y='borough'
).properties(
    width=600,
    height=400
)

st.altair_chart(chart, use_container_width=True)




df1['Tree Health'] = pd.to_numeric(df['health'], errors='coerce')
df1['Status of Tree'] = pd.to_numeric(df['status'], errors='coerce')
df1['Tree Species'] = pd.to_numeric(df['spc_common'], errors='coerce')
df1['Tree Stewardship'] = pd.to_numeric(df['steward'], errors='coerce')


total_trees = float(df1['Tree Health'].sum())
total_trees = float(df1['Tree Health'].sum())
total_trees = float(df1['Tree Health'].sum())

average_tree = float(df1['Tree Health'].mean())


total1,total2,total3,total4,total5 = st.columns(5,gap='large')

with total1:
    #st.image('',width = 300 ,use_column_width='Auto')
    st.metric(label = 'Total Trees', value= numerize(total_trees))
    
with total2:
    #st.image('',width = 300, use_column_width=25)
    st.metric(label='Total Trees', value=numerize(total_trees))

with total3:
    #st.image('',width = 300, use_column_width=300)
    st.metric(label= 'Total Treess',value=numerize(total_trees,2))

#
#with total5:
    #st.image('',width = 300, use_column_width=300)
    #st.metric(label='Average Tree Rating',value=numerize(average_tree))

