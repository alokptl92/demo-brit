from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd


#################################### LOAD and CLEAN DATA ###################################################
df = pd.read_csv('data_all.csv')
df = df.drop([0,23])    # 0 is empty, 23 is return
df1 = df[['Date','StA','StB','StC']]
df1['Date'] = pd.to_datetime(df1['Date'],infer_datetime_format=True)
df1['Month'] = df1['Date'].dt.month.astype(str)
df1.StB = df1.StB.apply(lambda x: x if x!='empty' else 'yes')
####################################### GENERATE COLUMNS ###################################################
df1['Anum'] = [3 if x in ['H','bpc'] else 2 if x in ['bp','bc','bf'] else 1 if x in ['b','p','c','f'] else 0 for x in df.StA]
df1['Cnum'] = [3 if x in ['H','bpc'] else 2 if x in ['bp','bc','bf'] else 1 if x in ['b','p','c','f'] else 0 for x in df.StC]
df1['Date_Group'] = df1['Date'].astype(str)
################################### PREPARE DATA #########################################################
df_count = df1.groupby(['StB','Anum','StA','StC']).Cnum.count().reset_index()
df_count.rename(columns={'Cnum':'Count'},inplace=True)


df3 = df1[['Month','Anum','StA']]
df3.rename(columns={'StA':'Cust_para'},inplace=True)
df3['Month'] = pd.Categorical(df3['Month'],categories=['10','11','12','1'],ordered=True)    
# df3 = df3.pivot_table(index=['Month'], columns='Anum', aggfunc='count',fill_value=0, sort=False)
# fig2 = px.bar(df3, x='Month', color='C')
# ax = df3.plot.bar(title= 'Customer Asks Distribution',width=0.4, stacked=True, colormap='viridis')
# ax.set_xticklabels(labels = ['10','11','12','1'], rotation='horizontal')
# ax.legend(title='Parameters mentioned',title_fontsize=11,bbox_to_anchor=(1.02, 1), loc='upper left')
######################## SHARED DATA ###################################
# df_s = pd.read_csv('shared_data.csv')
# # df = df.drop([0,23])
# print(df_s)
# df_s = df_s[["Date",'St1','St2','St3','St4']]
########################################################################


app = Dash(__name__)

fig = px.sunburst(df_count, 
                    path=['StB','Anum','StA','StC','Count'],
                    title='Customer Asks Distribution')

app.layout = html.Div(children=[
    html.H1(children='Customer Behavior Analysis'),
    dcc.Graph(
        id='example-graph',
        figure=fig,
        style={'display': 'inline-block'}
    ),
    html.Div(children=[
        html.H2("Customer Buying Behaviour"),
        html.P("Parameters: Based on rings INNER->OUTER"),
        html.P('RING1 : Sales'),
        html.P('RING2 : Number of Parameters Used by Customer'),
        html.P('RING3 : Parameter used by Customer Asking'),
        html.P('RING4 : Parameter used in Coversation'),
        html.H3('Parameters -'),
        html.P('    b - Good Day'),
        html.P('    H - Harmony'),
        html.P('    c - color(black/kala)'),
        html.P('    p - price(15)'),
        html.P('    f - flavor(chocolate)')
    ],style={'display': 'inline-block'}),
    html.H2("Bar Chart Distribution v Time"),
    dcc.Graph("")
])


# @app.callback(
#     Output("graph1", "figure"),
#     Input())
# def change_colorscale(scale):
#     fig = px.sunburst(df_count, 
#                       path=['StB','Anum','StA','StC','Count'],
#                       color_continuous_scale=scale,
#                       title='Customer Asks Distribution')
#     return fig


app.run_server(debug=True)