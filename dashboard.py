import pandas as pd 
import streamlit as st 
import plotly.express as px
from numerize.numerize import numerize 


st.set_page_config(page_title ='TreeNYC',
                   page_icon= ":deciduous_tree:",
                   layout = 'wide',
                   initial_sidebar_state='expanded')


@st.cache_data
def get_data():
    df = pd.read_csv('data/2015_Street_Tree_Census_1.csv', low_memory=False)
    return df

df = get_data()

#renaming colums and values 
new_column_names = {'steward':'Stewardship Signs', 'spc_common':'Species', 'nta_name': 'Neighborhood'}
df = df.rename(columns=new_column_names)
df['health'] = df['health'].fillna("Unknown (Choose for Dead/Stump)")
df['Species'] = df['Species'].fillna("Unknown")
df['Stewardship Signs'] = df['Stewardship Signs'].fillna("No Signs")
new_values = {'1or2': '1 or 2 Signs', '3or4': '3 or 4 Signs', '4orMore': '4 or More Signs'}
df['Stewardship Signs'] = df['Stewardship Signs'].replace(new_values)

title_left, title_mid, title_right = st.columns([1,5,1],gap = 'large')

with title_mid:
    st.title('TreeNYC: An Interactive Dashboard')

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

total_trees = df['tree_id'].value_counts()

tree_health = df['health'].value_counts()
good_trees = tree_health.get('Good',0)
fair_trees = tree_health.get('Fair',0)
healthy_trees = good_trees + fair_trees

tree_status = df['status'].value_counts()
dead_trees = tree_status.get('Dead', 0)
stumps = tree_status.get('Stump', 0)
dead_stumps = dead_trees + stumps 



total1,total2,total3 = st.columns([3,3,2])

with total1:
    st.image('images/nature.png',width = 200 ,use_column_width='Auto')
    st.metric(label = 'Total Trees', value= numerize(len(total_trees)))
    
with total2:
    st.image('images/fruit-tree.png',width = 200, use_column_width='Auto')
    st.metric(label='Healthy Trees', value = healthy_trees)

with total3:
    st.image('images/dead-tree.png',width = 200, use_column_width='Auto')
    st.metric(label= 'Dead Trees and Stumps',value=dead_stumps)



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
    fig.update_layout(width=1000, height = 1000)  
    st.plotly_chart(fig, use_container_width = True)


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
    fig.update_layout(width=1000, height = 1000)  
 

    st.plotly_chart(fig, use_container_width = True)



st.title("Tree Distribution Across NYC")
st.map(df1, size=20, latitude= 'latitude', longitude = 'longitude',color='#899878', use_container_width= False)

chart1, chart2 = st.columns([2,1])

with chart1:
    plot_species_by_neighborhood()
with chart2:
    plot_stewardship()


