import pandas as pd 
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

#renaming colums and values 
new_column_names = {'steward':'Stewardship Signs', 'spc_common':'Species', 'nta_name': 'Neighborhood'}
df = df.rename(columns=new_column_names)
df['health'] = df['health'].fillna("Unknown (Choose for Dead/Stump)")
df['Stewardship Signs'] = df['Stewardship Signs'].fillna("No Signs")
new_values = {'1or2': '1 or 2 Signs', '3or4': '3 or 4 Signs', '4orMore': '4 or More Signs'}
df['Stewardship Signs'] = df['Stewardship Signs'].replace(new_values)


header_left, header_mid, header_right = st.columns([1,3,1],gap = 'large')

with header_mid:
    st.title('NYC Tree Dashboard')

with st.sidebar:
    Borough_filter = st.multiselect(label= 'Select a Borough',
                                  options= df["borough"].unique())    
    Status_filter = st.multiselect(label= 'Select the Tree Status',
                                  options=df['status'].unique())
    Health_filter = st.multiselect(label= 'Select the Tree Health',
                                  options=df['health'].unique())
    Species_filter = st.multiselect(label= 'Select the Tree Species',
                                  options= df["Species"].unique())
    

    df1 = df.query ('borough == @Borough_filter  & health == @Health_filter & status == @Status_filter')
    df2 = df.query ('borough == @Borough_filter & Species == @Species_filter & health == @Health_filter')


st.map(df1, size=20, latitude= 'latitude', longitude = 'longitude',color='#899878')


def plot_species_by_neighborhood():
    df_grouped = df2.groupby(['Neighborhood', 'Species']).size().to_frame(name='Count').reset_index()

    fig = px.bar(
        df_grouped, 
        x = 'Neighborhood', 
        y = "Count", 
        color = "Species", 
        title = 'Species Count by Neighborhood'
        ).update_layout(
            xaxis_title="Neighborhood", 
            yaxis_title="Tree Count"
    )
    
    fig.update_layout(legend_title_text=' Tree Species')
    fig.update_layout(width=1000, height = 1000, title_x = 0.5)  
    st.plotly_chart(fig)
plot_species_by_neighborhood()



def plot_stewardship():

    df_grouped = df1['Stewardship Signs'].value_counts().to_frame(name='Count').reset_index()  

    color_list = px.colors.sequential.Magma  #there are 10 colors in magma 
    if len(color_list) < len(df_grouped):
        color_list *= (len(df_grouped) // len(color_list)) + 1  # repeat the color sequence

    fig = px.pie(
        df_grouped, 
        values = 'Count',
        names = 'Stewardship Signs',
        color = color_list[:len(df_grouped)],  #  only use the required number of colors
        title = "Percentage of Trees Exhibiting Signs of Stewardship" 
        )
    fig.update_layout(legend_title_text = "Number of Stewardship Signs")
    st.plotly_chart(fig)
plot_stewardship()

tree_count = df1['borough'].value_counts()
unique_nbh = df['Neighborhood'].unique()





df1['Tree Health'] = pd.to_numeric(df['health'], errors='coerce')
df1['Status of Tree'] = pd.to_numeric(df['status'], errors='coerce')
#df1['Tree Species'] = pd.to_numeric(df['spc_common'], errors='coerce')
#df1['Tree Stewardship'] = pd.to_numeric(df['steward'], errors='coerce')


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

