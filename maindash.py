import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from datetime import date
import pandas as pd
from dash_extensions import Lottie  
import base64
import datetime
import io
import numpy as np
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from datetime import date
import dash
import dash_html_components as html
import dash_core_components as dcc
import re
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.express as px
import dash_bootstrap_components as dbc
import datetime
import pandas as pd

# ==============================================================COLORS====================================================
colors = {
    'background': '#e6faff',
    'text': '#7FDBFF'
}

colors1 = {
    'background': '#ccffef',
    'text': '#7FDBFF'
}

colors2 = {
    'background': '#ffe6b3',
    'text': '#7FDBFF'
}

a = {'Intensive':'#A9A9A9',
    'Pooled':'#EBB3FF',
    'Reciprocal':'#2AACA9',
    'Sequential':'#CC9900'
    }

b = {'PlanGrid':'#A9A9A9',
    'Unifier':'#EBB3FF'
    
    }    

# ======================================================LOTEE FILES=======================================================

# Lottie by Emil - https://github.com/thedirtyfew/dash-extensions
url_coonections = "https://assets7.lottiefiles.com/private_files/lf30_nqxm2uay.json"
url_companies = "https://assets9.lottiefiles.com/packages/lf20_EzPrWM.json"
url_msg_in = "https://assets2.lottiefiles.com/packages/lf20_7bc3hw7m.json"
url_msg_out = "https://assets2.lottiefiles.com/packages/lf20_Cc8Bpg.json"
url_reactions = "https://assets3.lottiefiles.com/private_files/lf30_i5v0risx.json"
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))



year = [2019]
# =================================================READ DATA =========================================================
df = pd.read_excel(r'D:\STUDY MATERIAL\finaldashboard - Copy\data.xlsx',sheet_name = 'Sheet2')
df['Start Month']=df['Start Date'].dt.month
df['End Month']=df['End Date'].dt.month
df['End Year']=df['End Date'].dt.year
df['Start Year']=df['Start Date'].dt.year
df['Start Month']= df['Start Month'].replace({1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'})
df['End Month']= df['End Month'].replace({1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'})

#-==========================================----------email and issue file========================================================
df1 = pd.read_excel(r'D:\STUDY MATERIAL\finaldashboard - Copy\data.xlsx',sheet_name = 'Sheet3')
df100 = df1
# -----------------------
df100['upcoming_meeting_date'] = df100['Meeting Date'].shift(periods=-1)
df100['days_between_meeting']=df100['upcoming_meeting_date']-df100['Meeting Date']
df100['firstcount']=(df100['Emails to D']+df100['Email to O']+df100['Email to GC']+df100['PlanGrid']+df100['Unifier'])
df100['secondcount']=df100['firstcount'].shift(periods=1)
df100['days_between_meeting']=df100['days_between_meeting'].astype('str')
def func1(x):
    x=x[:2]
    return x
df100['num_of_days']=df100.apply(lambda x: func1(x['days_between_meeting']), axis=1)
df100['num_of_days']=df100['num_of_days'].replace('Na',0)
df100['secondcount']=df100['secondcount'].fillna(0)
df100['secondcount']=df100['secondcount'].astype('int')
df100['num_of_days']=df100['num_of_days'].astype('int')
df100['dv']=(df100['firstcount']-df100['secondcount'])/df100['num_of_days']
df100['dv']=df100['dv'].replace(df100['dv'][0],0)
df100['sum_of_issues']=(df100['Issues to O']+df100['Issues to GC']+df100['Issues to D'])
df100['sum_of_issues']=df100['sum_of_issues'].fillna(0)
df100['sum_of_issues']=df100['sum_of_issues'].astype('int')
df100['sum_of_issues_second_meet']=df100['sum_of_issues'].shift(periods=1)
df100['WIP']=(df100['sum_of_issues']-df100['sum_of_issues_second_meet'])
df100['WIP']=df100['WIP'].fillna(0)
df100['Month']=df100['Meeting Date'].dt.month
df100['Month'] = df100['Month'].replace({1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'})
df1001=df100[['Meeting Date','upcoming_meeting_date','dv','WIP','Month','Phases','Comments']]
df1002 =pd.melt(df1001, id_vars=['Meeting Date', 'upcoming_meeting_date','Month'], var_name=[('dv', 'WIP')], value_name='Value')
df1002.columns=['Meeting Date', 'upcoming_meeting_date', 'Month', 'category','Value']

df150 = df1001
# df150['Phases'] = df100['Month'].replace({'January':'1st Phase','February':'2nd Phase','March':'3rd Phase','April':'4th Phase','May':'5th Phase','June':'6th Phase','July':'7th Phase','August':'8th Phase','September':'9th Phase','October':'10th Phase','November':'11th Phase','December':'12th Phase'})
print(df150.head())
# =======================================================BOTTLENECK DETECTION============================================================
df150['dv'] = round(abs(df150['dv']/10),2)
df150['WIP'] = round(abs(df150['WIP']/10),2)
twofive = [0.  , 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1 ,0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2 , 0.21,0.22, 0.23, 0.24, 0.25]
five = [0.25, 0.26, 0.27, 0.28, 0.29, 0.3 , 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4 , 0.41, 0.42, 0.43, 0.44, 0.45, 0.46,0.47, 0.48, 0.49, 0.5 ]
sevenfive = [0.5 , 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59, 0.6 , 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67, 0.68, 0.69, 0.7 , 0.71, 0.72, 0.73, 0.74, 0.75]
one = [0.75, 0.76, 0.77, 0.78, 0.79, 0.8 , 0.81, 0.82, 0.83, 0.84, 0.85,
       0.86, 0.87, 0.88, 0.89, 0.9 , 0.91, 0.92, 0.93, 0.94, 0.95, 0.96,
       0.97, 0.98, 0.99, 1.  , 1.01, 1.02, 1.03, 1.04, 1.05, 1.06, 1.07,
       1.08, 1.09, 1.1 , 1.11, 1.12, 1.13, 1.14, 1.15, 1.16, 1.17, 1.18,
       1.19, 1.2 , 1.21, 1.22, 1.23, 1.24, 1.25, 1.26, 1.27, 1.28, 1.29,
       1.3 , 1.31, 1.32, 1.33, 1.34, 1.35, 1.36, 1.37, 1.38, 1.39, 1.4 ,
       1.41, 1.42, 1.43, 1.44, 1.45, 1.46, 1.47, 1.48, 1.49, 1.5 , 1.51,
       1.52, 1.53, 1.54, 1.55, 1.56, 1.57, 1.58, 1.59, 1.6 , 1.61, 1.62,
       1.63, 1.64, 1.65, 1.66, 1.67, 1.68, 1.69, 1.7 , 1.71, 1.72, 1.73,
       1.74, 1.75, 1.76, 1.77, 1.78, 1.79, 1.8 , 1.81, 1.82, 1.83, 1.84,
       1.85, 1.86, 1.87, 1.88, 1.89, 1.9 , 1.91, 1.92, 1.93, 1.94, 1.95,
       1.96, 1.97, 1.98]
# onetwo = pl.frange(1.00,2.00,0.01)
def funx(x):
    x = float(x)
    if x in(twofive):
        return '0 - 0.25'
    if x in(five):
        return '0.25 - 0.50'
    if x in(sevenfive):
        return '0.50 - 0.75'
    if x in(one):
        return '0.75 - 1'
def funy(y):
    y=float(y)
    if y in(twofive):
        return '0 - 0.25'
    if y in(five):
        return '0.25 - 0.50'
    if y in(sevenfive):
        return '0.50 - 0.75'
    if y in(one):
        return '0.75 - 1'
df150['dv_range'] = df150.dv.apply(funx)
df150['wip_range'] = df150.WIP.apply(funy)
def fun2(x,y):
    if (x == '0.25 - 0.50')&(y == '0.75 - 1'):
        return 1
    if (x == '0.00 - 0.25')&(y == '0.75 - 1'):
        return 1
    if (x == '0.50 - 0.75')&(y == '0.75 - 1'):
        return 1
df150['range']= df150['dv_range']+df150['wip_range']
def fun4(x):
    if x == '0 - 0.250.75 - 1':
        return 1
    if x == '0.25 - 0.500.75 - 1':
        return 1
    if x == '0.50 - 0.750.75 - 1':
        return 1
df150['range1'] = df150.range.apply(fun4)
df150['range1'] = df150['range1'].fillna(0)
df150['range1'] = df150['range1'].astype(int)
df150 = df150[['Meeting Date', 'upcoming_meeting_date', 'dv', 'WIP', 'Month',
       'dv_range', 'wip_range',  'range1','Phases','Comments']]
df150=df150[df150['range1']==1]
df150['Year'] =df150['Meeting Date'].dt.year
df150['Meeting Date'] = df150['Meeting Date'].dt.strftime("%m/%d/%Y")
df150 = df150[['Meeting Date','Month','Phases','Year','Comments']]
df150.columns = ['Exact Dates','Month','Phases','Year','Comments']
df150 = df150[['Phases','Comments','Month','Exact Dates']]

#====================================================================================================================================

# --------------------------

# df1  = df1.rename(columns={'Issues to D':'Issues to D', 'Issues to O':'Issues to O','Issues to GC':'Issues to GC','Emails to D':'Emails to D'})
df1['Start Date'] = df1['Meeting Date']
df5 = df.merge(df1, how='inner', on='Start Date')
abc = df5
group = df5.groupby(['Description','Responsible Party','Start Date','End Date','Days to Complete','Start Year','Start Month','End Year','End Month','Phases','Comments'])[['Emails to D','Issues to D','Email to O','Issues to O','Email to GC','Issues to GC','PlanGrid','Unifier']].sum().reset_index()
print(group)

#===========================================================type of issues==================================================================

df15 = pd.read_excel(r'D:\STUDY MATERIAL\finaldashboard - Copy\data1.xlsx',sheet_name='Types of Issues')
df16=df15[['Reciprocal']]
df16=df16.dropna()
df16['name']='Reciprocal'
df16.columns=['Description', 'name']
df17=df15[['Pooled']]
df17=df17.dropna()
df17['name']='Pooled'
df17.columns=['Description', 'name']
df18=df15[['Intensive']]
df18=df18.dropna()
df18['name']='Intensive'
df18.columns=['Description', 'name']
df19=df15[['Sequential']]
df19=df19.dropna()
df19['name']='Sequential'
df19.columns=['Description', 'name']
df20 =pd.concat([df16,df17,df18,df19],axis=0)
df19.columns=['Description', 'name']
df21=df.merge(df16,how = 'inner',on='Description')
df22=df.merge(df17,how = 'inner',on='Description')
df23=df.merge(df18,how = 'inner',on='Description')
df24=df.merge(df19,how = 'inner',on='Description')
df26 = pd.concat([df21,df22,df23,df24],axis=0)
df27=df26.groupby(['name','Start Month','Responsible Party','Days to Complete', 'End Month','Start Year','End Year'])[['Description']].count().reset_index()
print(df27.head(1))

# ================================================================START DASH APP=======================================================

external_stylesheets = 'bootstrap.css'

# app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL],
#   meta_tags=[{'name': 'viewport',
#                             'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
#     )
month = ['January','February','March','April','May','June','July','August','September','October','November','December']

#app = dash.Dash(external_stylesheets=[dbc.themes.LUMEN],
 # meta_tags=[{'name': 'viewport',
 #                           'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
 #   )

def create_dash_application(flask_app):
    dash_app = dash.Dash(external_stylesheets=[dbc.themes.LUMEN],server=flask_app,name='Dashboard',url_base_pathname = '/dash/',
    meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}])
                            
    dash_app.layout = html.Div(
    [
        dcc.Store(id='side_click'),
        dcc.Location(id="url"),
        navbar,
        sidebar,
        content,
    ],
    )   

    @dash_app.callback(
    [
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("side_click", "data"),
    ],

    [Input("btn_sidebar", "n_clicks")],
    [
        State("side_click", "data"),
    ]
)
    def toggle_sidebar(n, nclick):
        if n:
            if nclick == "SHOW":
                sidebar_style = SIDEBAR_HIDEN
                content_style = CONTENT_STYLE1
                cur_nclick = "HIDDEN"
            else:
                sidebar_style = SIDEBAR_STYLE
                content_style = CONTENT_STYLE
                cur_nclick = "SHOW"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = 'SHOW'

        return sidebar_style, content_style, cur_nclick

    # this callback uses the current pathname to set the active state of the
    # corresponding nav link to true, allowing users to tell see page they are on
    @dash_app.callback(
        [Output(f"page-{i}-link", "active") for i in range(1, 4)],
        [Input("url", "pathname")],
    )
    def toggle_active_links(pathname):
        if pathname == "/":
            # Treat page 1 as the homepage / index
            return True, False, False
        return [pathname == f"/page-{i}" for i in range(1, 4)]

    # ==================================================================LINK PAGES================================================
    @dash_app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def render_page_content(pathname):
        if pathname in ["/dash/page-1"]:
            return [layout_1]
        elif pathname == "/dash/page-2":
            return [layout2]
        # elif pathname == "/page-3":
        #     return [layout3]
        elif pathname == "/dash/page-4":
            return [layout4]
        elif pathname == "/dash/page-6":
            return [layout5]
        elif pathname == "/dash/page-7":
            return [layout7]
        elif pathname == "/dash/page-8":
            return [layout8]        
        else:
            return [
            # index_page,
            homelayout
            ]

        # If the user tries to reach a different page, return a 404 message
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )


    # ======================================================================EMAIL INFORMATION===================================================
    @dash_app.callback(
        Output("output", "figure"),
        Input("input1", "value"),
        Input("input2", "value"),
        Input("input3", "value"),
        Input("input4", "value"),
    )   
    def func(start_year,start_month,end_year,end_month):
        df = group[(group['Start Year']==start_year)&(group['End Year']==end_year)&(group['Start Month']==start_month)&(group['End Month']==end_month)]
        df = df[['Start Year','Start Month','End Year','End Month','Start Date','End Date','Days to Complete','Emails to D','Issues to D','Email to O','Issues to O','Email to GC','Issues to GC','PlanGrid','Unifier']]
        dff =pd.melt(df, id_vars=['Start Year','Start Month','End Year','End Month','Start Date','End Date','Days to Complete'], var_name=[('Emails to D','Issues to D','Email to O','Issues to O','Email to GC','Issues to GC','PlanGrid','Unifier')], value_name='value')
        dff.columns = ['Start Year','Start Month','End Year','End Month','Start Date','End Date','Days to Complete','colnames','value']
        dff = dff[(dff['colnames']!='PlanGrid')&(dff['colnames']!='Unifier')&(dff['colnames']!='Issues to D')&(dff['colnames']!='Issues to O')&(dff['colnames']!='Issues to GC')]
        dff['colnames'] = dff['colnames'].replace(['Emails to D','Email to O','Email to GC'],['Designer','Owner','General Contrator'])
        dff=dff.groupby(['Start Month','End Month','Start Year','End Year','colnames'])[['value']].sum().reset_index()
        return px.bar(dff, x='colnames', y='value',template = 'plotly_white',color='colnames',title='<b>Email Information</b>', height=380)\
        .update_layout(showlegend=False,margin=dict(t=50, b=50, l=50, r=50),title_x=0.5,yaxis=dict(title=dict(text='Number of Emails',font=dict(size=14))),xaxis=dict(title=dict(text='Responsible Party',font=dict(size=14)))) 

    @dash_app.callback(
        Output("output13", "figure"),
        Input("input1", "value"),
        Input("input2", "value"),
        Input("input3", "value"),
        Input("input4", "value"),
    )   
    def func(start_year,start_month,end_year,end_month):
        df = group[(group['Start Year']==start_year)&(group['End Year']==end_year)&(group['Start Month']==start_month)&(group['End Month']==end_month)]
        df = df[['Start Year','Start Month','End Year','End Month','Start Date','End Date','Days to Complete','Emails to D','Issues to D','Email to O','Issues to O','Email to GC','Issues to GC','PlanGrid','Unifier']]
        dff =pd.melt(df, id_vars=['Start Year','Start Month','End Year','End Month','Start Date','End Date','Days to Complete'], var_name=[('Emails to D','Issues to D','Email to O','Issues to O','Email to GC','Issues to GC','PlanGrid','Unifier')], value_name='value')
        dff.columns = ['Start Year','Start Month','End Year','End Month','Start Date','End Date','Days to Complete','colnames','value']
        dff = dff[(dff['colnames']!='Emails to D')&(dff['colnames']!='Email to O')&(dff['colnames']!='Email to GC')&(dff['colnames']!='Issues to D')&(dff['colnames']!='Issues to O')&(dff['colnames']!='Issues to GC')]
        dff=dff.groupby(['Start Month','End Month','Start Year','End Year','colnames'])[['value']].sum().reset_index()
        return px.bar(dff, x='colnames', y='value',template = 'plotly_white',color='colnames',color_discrete_map= b,title='<b>Web Based Project Documentation Data</b>', height=380)\
        .update_layout(showlegend=False,margin=dict(t=50, b=50, l=50, r=50),title_x=0.5,yaxis=dict(title=dict(text='Number of Information bits',font=dict(size=14))),xaxis=dict(title=dict(text='PlanGrid & Unifier',font=dict(size=14)))) 

    @dash_app.callback(
    Output("output7", "figure"),
    Input("input1", "value"),
    Input("input2", "value"),
    Input("input3", "value"),
    Input("input4", "value"),
    )   
    def func(start_year,start_month,end_year,end_month):
        df = group[(group['Start Year']==start_year)&(group['End Year']==end_year)&(group['Start Month']==start_month)&(group['End Month']==end_month)]
        dff =pd.melt(df, id_vars=['Description','Responsible Party','Start Year','Start Month','End Year','End Month','Start Date','End Date','Days to Complete'], var_name=[('Emails to D','Issues to D','Email to O','Issues to O','Email to GC','Issues to GC')], value_name='value')
        dff.columns = ['Description','Responsible Party','Start Year','Start Month','End Year','End Month','Start Date','End Date','Days to Complete','colnames','value']
        dff = dff[(dff['colnames']!='Emails to D')&(dff['colnames']!='Email to O')&(dff['colnames']!='Email to GC')]
        dff=dff.groupby(['Description','Responsible Party','Start Month','End Month','Start Year','End Year','colnames'])[['value']].sum().reset_index()
        return px.bar(dff, x='colnames', y='value',template = 'plotly_white',color='Description',title='<b>Issue Information</b>', height=380)\
        .update_layout(showlegend=True,margin=dict(t=50, b=50, l=50, r=50),title_x=0.5,xaxis=dict(title=dict(text='Responsible Party',font=dict(size=14))))      

    # =================================================================TYPE OF ISSUE================================================
    @dash_app.callback(
        Output("output5", "figure"),
        Input("input2", "value"),
        Input("input4", "value"),
    )
    def func1011(startmonth,endmonth):
        df28=df27[(df27['Start Month']==startmonth)&(df27['End Month']==endmonth)]
        df28 = df28.groupby(['name','Responsible Party'])[['Description']].sum().reset_index()
        return px.bar(df28, x='name', y='Description',color = 'Responsible Party',template = 'plotly_white',title='<b>Issue Report</b>', height=380)\
        .update_layout(showlegend=True,margin=dict(t=50, b=50, l=50, r=50),title_x=0.5,yaxis=dict(title=dict(text='',font=dict(size=14))),xaxis=dict(title=dict(text='Types of Activity',font=dict(size=14))))
    # ===============================================================WIP AND DV====================================================
    @dash_app.callback(
        Output("output3", "figure"),
        Input("input5", "value"),
    )
    def func100(month):
        df12=df1002[df1002['Month']==month]
        return px.line(df12, x='Meeting Date', y='Value',color = 'category',template = 'plotly_white',title='WIP and DV', height=380)\
        .update_layout(showlegend=True,margin=dict(t=50, b=50, l=50, r=50),title_x=0.5).update_traces(mode='lines+markers')
    # ===========================================================DV=======================================================
    @dash_app.callback(
        Output("output4", "figure"),
        Input("input5", "value"),
    )
    def dv(month):
        df12=df1001[df1001['Month']==month]
        return px.bar(df12, x='Meeting Date', y='dv',orientation='h',color = 'Meeting Date',template = 'plotly_white',title='DV', height=380)\
        .update_layout(showlegend=True,margin=dict(t=50, b=50, l=50, r=50),title_x=0.5)

    @dash_app.callback(
        Output("output1", "figure"),
        Input("input1", "value"),
        Input("input2", "value"),
        Input("input3", "value"),
        Input("input4", "value"),
    )   
    def func1(start_year,start_month,end_year,end_month):
        owner = abc[(abc['Responsible Party']=='O')&(abc['Start Year']==start_year)&(abc['End Year']==end_year)&(abc['Start Month']==start_month)&(abc['End Month']==end_month)]
        owner=owner[['Responsible Party','Email to O','Issues to O','Days to Complete']]
        owner['average_days_to_complete']=owner['Days to Complete'].mean()
        owner['total_email']=owner['Email to O'].sum()
        owner['email']=owner['Issues to O'].sum()
        owner['productivity'] = (owner['email']/owner['total_email'])*100
        owner  =owner[['Responsible Party','total_email','productivity','average_days_to_complete']]
        owner=owner[0:1]
        gc = abc[(abc['Responsible Party']=='GC')&(abc['Start Year']==start_year)&(abc['End Year']==end_year)&(abc['Start Month']==start_month)&(abc['End Month']==end_month)]
        gc=gc[['Responsible Party','Email to GC','Issues to GC','Days to Complete']]
        gc['average_days_to_complete']=gc['Days to Complete'].mean()
        gc['total_email']=gc['Email to GC'].sum()
        gc['email']=gc['Issues to GC'].sum()
        gc['productivity'] = (gc['email']/gc['total_email'])*100
        gc  =gc[['Responsible Party','total_email','productivity','average_days_to_complete']]
        gc=gc[0:1]
        d = abc[(abc['Responsible Party']=='D')&(abc['Start Year']==start_year)&(abc['End Year']==end_year)&(abc['Start Month']==start_month)&(abc['End Month']==end_month)]
        d=d[['Responsible Party','Emails to D','Issues to D','Days to Complete']]
        d['average_days_to_complete']=d['Days to Complete'].mean()
        d['total_email']=d['Emails to D'].sum()
        d['email']=d['Issues to D'].sum()
        d['productivity'] = (d['email']/d['total_email'])*100
        d  =d[['Responsible Party','total_email','productivity','average_days_to_complete']]
        d=d[0:1]
        frames = [owner, d, gc]
        result = pd.concat(frames)
        # pie_fig = px.pie(result, names=result['Responsible Party'], values='average_days_to_complete' ,height = 480,hole = .3,template = 'plotly_white',color = 'Responsible Party' , title='Average Days to Complete')\
        #         .update_layout(showlegend=True,margin=dict(t=50, b=50, l=50, r=50),title_x=0.5).update_traces(textposition='inside',  textinfo='label+percent+value')
        # return pie_fig
        return px.bar(result, x='Responsible Party', y='average_days_to_complete',color = 'Responsible Party',template = 'plotly_white',title='<b>Average Days to Complete</b>', height=380)\
        .update_layout(showlegend=True,margin=dict(t=50, b=50, l=50, r=50),title_x=0.5)

    @dash_app.callback(
        Output("output11", "figure"),
        Input("input1", "value"),
        Input("input2", "value"),
        Input("input3", "value"),
        Input("input4", "value"),
    )   
    def func1(start_year,start_month,end_year,end_month):
        df28 = df27[(df27['Start Year']==start_year)&(df27['End Year']==end_year)&(df27['Start Month']==start_month)&(df27['End Month']==end_month)]
        df28 = df28.groupby(['name'])[['Days to Complete']].mean().reset_index()
        return px.bar(df28, x='name', y='Days to Complete',color = 'name',color_discrete_map= a,template = 'plotly_white',title='<b>Average Days to Resolve Issue</b>', height=380)\
        .update_layout(showlegend=True,margin=dict(t=50, b=50, l=50, r=50),title_x=0.5,xaxis=dict(title=dict(text='Issue Reported',font=dict(size=14))))


    # ==================================================================PRODUCTIVITY=========================================================
    @dash_app.callback(
        Output("output12", "figure"),
        Input("input1", "value"),
    )   
    def productivity1(start_year):
        owner1 = abc[(abc['Responsible Party']=='O')&(abc['Start Year']==start_year)]
        owner1['Start Month']= owner1['Start Month'].replace({'January':'01/01','February':'01/02','March':'01/03','April':'01/04','May':'01/05','June':'01/06','July':'01/07','August':'01/08','September':'01/09','October':'01/10','November':'01/11','December':'01/12'})
        a = owner1.groupby(['Responsible Party','Start Month'])[['Email to O']].sum().reset_index()
        b=owner1.groupby(['Responsible Party','Start Month'])[['Issues to O']].sum().reset_index()
        b=b[['Issues to O']]
        owner = pd.concat([a,b],axis = 1)
        owner['Values'] = (owner['Issues to O']/owner['Email to O'])
        gc1 = abc[(abc['Responsible Party']=='GC')&(abc['Start Year']==start_year)]
        gc1['Start Month']= gc1['Start Month'].replace({'January':'01/01','February':'01/02','March':'01/03','April':'01/04','May':'01/05','June':'01/06','July':'01/07','August':'01/08','September':'01/09','October':'01/10','November':'01/11','December':'01/12'})
        a = gc1.groupby(['Responsible Party','Start Month'])[['Email to GC']].sum().reset_index()
        b=gc1.groupby(['Responsible Party','Start Month'])[['Issues to GC']].sum().reset_index()
        b=b[['Issues to GC']]
        gc = pd.concat([a,b],axis = 1)
        gc['Values'] = (gc['Issues to GC']/gc['Email to GC'])
        d1 = abc[(abc['Responsible Party']=='D')&(abc['Start Year']==start_year)]
        d1['Start Month']= d1['Start Month'].replace({'January':'01/01','February':'01/02','March':'01/03','April':'01/04','May':'01/05','June':'01/06','July':'01/07','August':'01/08','September':'01/09','October':'01/10','November':'01/11','December':'01/12'})
        a = d1.groupby(['Responsible Party','Start Month'])[['Emails to D']].sum().reset_index()
        b=d1.groupby(['Responsible Party','Start Month'])[['Issues to D']].sum().reset_index()
        b=b[['Issues to D']]
        d = pd.concat([a,b],axis = 1)
        d['Values'] = (d['Issues to D']/d['Emails to D'])
        frame =[owner,gc,d]
        productive = pd.concat(frame,axis = 0)
        productive=productive[['Responsible Party', 'Start Month','Values']]
        print(productive.head())
        return px.line(productive, x='Start Month', y='Values',color = 'Responsible Party',template = 'plotly_white',title='<b>Productivity</b>', height=380)\
        .update_layout(showlegend=True,margin=dict(t=50, b=50, l=50, r=50),title_x=0.5,yaxis=dict(tickformat = "%",title=dict(text='Percentage',font=dict(size=14))),xaxis=dict(title=dict(text='Month',font=dict(size=14)))).update_traces(mode='lines+markers')
    


    return dash_app    
#app.config['suppress_callback_exceptions'] = True

#app.config.suppress_callback_exceptions = True

#app.css.config.serve_locally = True
#app.scripts.config.serve_locally = True

#server = app.server
# ================================================================FRONT VIEW==========================================================
layout_1 = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.I('Start Year'),
            dcc.Dropdown(id='input1', multi=False, value=2019,options=[{'label':x, 'value':x}
                                  for x in sorted(group['Start Year'].unique())])],width={'size':2}),

        dbc.Col([
            html.I('Start Month'),
            dcc.Dropdown(id='input2', multi=False,  value='February',options=[{'label':x, 'value':x}
                                  for x in month])],width={'size':2}),

        dbc.Col([
            html.I('End Year'),
            dcc.Dropdown(id='input3', multi=False, value=2019,options=[{'label':x, 'value':x}
                                  for x in sorted(group['End Year'].unique())]
                )],width={'size':2}),

        dbc.Col([
            html.I('End Month'),
            dcc.Dropdown(id='input4', multi=False,  value='February',options=[{'label':x, 'value':x}
                                  for x in month])],width={'size':2}),


        ], no_gutters=False, justify='start',style = {"padding": "1rem 0rem"}),
    dbc.Row([
        dbc.Col([
        	
        	dcc.Loading(dcc.Graph(id='output', figure={},style = {"border":"10px groove"}  ,)),
        	],width={'size':6}),
        dbc.Col([
            
            dcc.Loading(dcc.Graph(id='output13', figure={},style = {"border":"10px groove"}  ,)),
            ],width={'size':6}),
        ]),
    dbc.Row([dbc.Col([
    	dcc.Markdown(("""**Email Information**: Emails exchanged between project teams during the time selected.""")),
        dcc.Markdown(("""**Web Based Project Documentation Data**: Information shared in online platforms.""")),
    	
    	])],style = {"padding": "1rem 0rem"}),
    # dbc.Row([dbc.Col([
    # 	dcc.Markdown(("""**Issue Information**: Number of Issues discussed in project meetings for each team during the time selected.""")),
    # 	])],style = {"padding": "1rem 0rem"}),

    ], fluid=True,style = {"padding": "2rem 0rem"}  )
	


layout2 = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.I('Start Year'),
            dcc.Dropdown(id='input1', multi=False, value=2019,options=[{'label':x, 'value':x}
                                  for x in sorted(group['Start Year'].unique())])],width={'size':2}),

        dbc.Col([
            html.I('Start Month'),
            dcc.Dropdown(id='input2', multi=False,  value='February',options=[{'label':x, 'value':x}
                                  for x in month])],width={'size':2}),

        dbc.Col([
            html.I('End Year'),
            dcc.Dropdown(id='input3', multi=False, value=2019,options=[{'label':x, 'value':x}
                                  for x in sorted(group['End Year'].unique())]
                )],width={'size':2}),

        dbc.Col([
            html.I('End Month'),
            dcc.Dropdown(id='input4', multi=False,  value='February',options=[{'label':x, 'value':x}
                                  for x in month])],width={'size':2}),


        ], no_gutters=False, justify='start',style = {"padding": "1rem 0rem"}),
    # dbc.Row([
    #     dbc.Col([dcc.Loading(dcc.Graph(id='output', figure={},style = {"border":"10px groove"}  ,)),],width={'size':12})

    #     ]),

    dbc.Row([
        dbc.Col([dcc.Loading(dcc.Graph(id='output5', figure={},style = {"border":"10px groove"}  ,)),],width={'size':12})

        ], no_gutters=False, justify='start',style = {"padding": "0rem 0rem"}),
    #dbc.Row([  
    #dbc.Col([
        #html.Div(children = html.Img(src=dash_app.get_asset_url("im3.png"),style={'height':'20%','width':'70%','textAlign': 'center'}),),
        #],style={'textAlign': 'center'})
        #]),
    dbc.Row([dbc.Col([
    	dcc.Markdown(("""**Issue Report**: Four major categories of issues: Pooled, Sequential, Reciprocal, and Intensive.""")),
    	
    	])],style = {"padding": "1rem 0rem"}),
    ], fluid=True)


layout3 = dbc.Container([
   
    dbc.Row([
        dbc.Col([
            html.I('Meeting Month'),
            dcc.Dropdown(id='input5', multi=False, value=2,options=[{'label':x, 'value':x}
                                  for x in month])],width={'size':2}),
        ], no_gutters=False, justify='start',style = {"padding": "1rem 0rem"}),

    dbc.Row([
        
        dbc.Col([dcc.Loading(dcc.Graph(id='output3', figure={},style = {"border":"10px groove"}  ,)),],width={'size':12}),
        # dbc.Col([dcc.Loading(dcc.Graph(id='output4', figure={},style = {"border":"10px groove"}  ,)),],width={'size':6})

        ], no_gutters=False, justify='start',style = {"padding": "1rem 0rem"}),

    dbc.Row([dbc.Col([
    	dcc.Markdown(("""**WIP and DV**: Development Velocity and Work in Progress: Information exchange metrics illustrating how information is modified.""")),
    	
    	])],style = {"padding": "1rem 0rem"}),

    ], fluid=True)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavItem(dbc.NavLink("HOME", href="/"), id="HOME-link"),),
        dbc.Button("☰", outline=True, color="secondary", className="mr-1", id="btn_sidebar"),
        
        # dbc.DropdownMenu(
        #     children=[
        #         dbc.DropdownMenuItem("More pages", header=True),
        #         dbc.DropdownMenuItem("Page 2", href="#"),
        #         dbc.DropdownMenuItem("Page 3", href="#"),
        #     ],
        #     nav=True,
        #     in_navbar=True,
        #     label="More",
        # ),
    ],
    brand="BOTTLENECK REPORTING TOOL",
    brand_href="#",
    color="dark",
    dark=True,
    fluid=True,
)

layout4 = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.I('Start Year'),
            dcc.Dropdown(id='input1', multi=False, value=2019,options=[{'label':x, 'value':x}
                                  for x in sorted(group['Start Year'].unique())])],width={'size':2}),

        dbc.Col([
            html.I('Start Month'),
            dcc.Dropdown(id='input2', multi=False,  value='February',options=[{'label':x, 'value':x}
                                  for x in month])],width={'size':2}),

        dbc.Col([
            html.I('End Year'),
            dcc.Dropdown(id='input3', multi=False, value=2019,options=[{'label':x, 'value':x}
                                  for x in sorted(group['End Year'].unique())]
                )],width={'size':2}),

        dbc.Col([
            html.I('End Month'),
            dcc.Dropdown(id='input4', multi=False,  value='February',options=[{'label':x, 'value':x}
                                  for x in month])],width={'size':2}),


        ], no_gutters=False, justify='start',style = {"padding": "1rem 0rem"}),
    

    dbc.Row([
        dbc.Col([dcc.Loading(dcc.Graph(id='output1', figure={},style = {"border":"10px groove"}  ,)),],width={'size':6}),
        dbc.Col([dcc.Loading(dcc.Graph(id='output11', figure={},style = {"border":"10px groove"}  ,)),],width={'size':6})


        ], no_gutters=False, justify='start',style = {"padding": "1rem 0rem"}),

    #dbc.Row([
        #dbc.Col([
        #html.Div(children = html.Img(src=app.get_asset_url("image3.png"),style={'height':'20%','width':'70%','textAlign': 'center'}),),
        #],style={'textAlign': 'center'})


        #], no_gutters=False, justify='start',style = {"padding": "1rem 0rem"}),

    dbc.Row([
        dbc.Col([
        
    	dcc.Markdown(("""**Average Days to Resolve**: Team Performance Metric, illustrating the average number of days to resolve a particular issue during the selected time.""")),
    	
    	])],style = {"padding": "1rem 0rem"}),

   

    ], fluid=True)

layout7 = dbc.Container([
    dbc.Row([
dbc.Col([
    html.I('Start Year'),
            dcc.Dropdown(id='input1', multi=False, value=2019,options=[{'label':x, 'value':x}
                                  for x in year]),

    ])
        ]),
    dbc.Row([

dbc.Col([dcc.Loading(dcc.Graph(id='output12', figure={},style = {"border":"10px groove"}  ))],width={'size':12}),

        ]),
    dbc.Row([dbc.Col([
      dcc.Markdown(("""**Productivity**: Team Performance Metric, illustrating the how productive project teams are in resolving issues.""")),
        
      ])],style = {"padding": "1rem 0rem"}),
   
 


    ], fluid=True)

layout5 = dbc.Container([
    dbc.Row([dbc.Col([
        dcc.Markdown((""" **Bottleneck Reporting** """)),
        
        ])],style = {"padding": "1rem 0rem"}),

    dbc.Row([

        dbc.Col([
            dbc.Card([
                # dbc.CardHeader(Lottie(options=options, width="67%", height="30%", url=url_msg_in)),
                dbc.CardBody([
                    dash_table.DataTable(
    data=df150.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df150.columns],

    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['Date', 'Region']
    ],
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(242, 230, 255)'
        }
    ],
    style_data={
       
        'lineHeight': '20px'
    },
    style_cell = {
                # 'font_family': 'cursive',
                'font_size': '14px',
                'text_align': 'center'
            },
    style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
    }
),


                ]),
                
            ]),
            ],width={"size":12}),
        # html.Img(src=app.get_asset_url("image.png"),style={'height':'100%'}),
            ]),
    #dbc.Row([
        #dbc.Col([
        #html.Div(children = html.Img(src=app.get_asset_url("image2.png"),style={'height':'20%','width':'70%','textAlign': 'center'}),),
        #],style={'textAlign': 'center'})])
#     dbc.Row([
#         dbc.Col([ Lottie(options=options, width="40%", height="50%", url=url_coonections),
#             ],style={"padding": "2rem  0rem"})

# #     dbc.Col([
# #         Lottie(options=options, width="40%", height="50%", url=url_coonections),
# #         ],style={"padding": "2rem  0rem"})    
#     # dbc.Col([
#     #     html.Div(children = html.Img(src=app.get_asset_url("image.png"),style={'height':'20%','width':'70%'}),),
#     #     ],style={'textAlign': 'center'})
#         ])
   
    ], fluid=True)

layout8 = dbc.Container([
    dbc.Row([dbc.Col([
        dcc.Markdown((""" **Bottleneck Prediction Moving Forward** """)),
        
        ])],style = {"padding": "1rem 0rem"}),

    
    #dbc.Row([

#         
    #dbc.Col([
        #html.Div(children = html.Img(src=app.get_asset_url("image5.png"),style={'height':'20%','width':'70%','textAlign': 'center'}),),
        #],style={'textAlign': 'center'})
        #])
   
    ], fluid=True)



# =========================================================SIDEBAR==========================================================

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 60.5,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "background-color": "#ccefff",
}

SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": 60.5,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    "background-color": "#ccefff",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "16rem",
    "margin-right": "0rem",
    "padding": "1rem 1rem",
    "background-color": "#e6ffff",
}

CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "0rem",
    "margin-right": "0rem",
    "padding": "1rem 1rem",
    "background-color": "#e6ffff",
}

# ==========================================================INDEX========================================================================

index_page = html.Div(
                className="container scalable",
                children=[
                    html.Div(
                        id="banner1",
                        className="banner1",
                        children=[
                        
                            dbc.NavbarSimple(
    children=[
        html.Div(html.H3("BOTTLENECK REPORTING TOOL"),style = { 'padding': '0rem 18rem 0rem'}), 


    ],
    color="#FFFFFF",
    dark=False,
    style = {'backgroundColor': colors2['background']},
    
),
                            
                        ],

                    ),
                 
    
])

homelayout = dbc.Container([
    dbc.Row([
        dbc.Col([
             dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="67%", height="67%", url=url_msg_in),style={"padding": "1rem 7rem 0rem"}),

    dbc.CardBody(
        [
            # html.H5("", className="card-title"),
            html.H4(""" This Tool reports Information Bottlenecks in ACE Projects using Archival Project Data.
            The Tool Uses project documentation data,email dates,project meeting dates to report on information bottleneck. """),
                
            
        ]
    ),],
    style={"padding": "1rem 0rem","width": "70rem",'backgroundColor': colors['background']},
)

            ])
        ],style={"padding": "1rem 0rem"},),

    dbc.Row([
        dbc.Col([
            dbc.Card(
    dbc.CardBody(
        [
            html.H5("KEY TERMS:", className="card-title"),
            dcc.Markdown(("""**INFORMATION BOTTLENECK:** Defined as a withholding of information by team members  """ )),   
            dcc.Markdown(("""**TEAM PERFORMANCE DATA:** Metrics used to measure the performance of ACE teams.  """ )), 
            dcc.Markdown(("""**PROJECT PERFORMANCE DATA:** Metrics used to measure the performance of ACE projects.  """ )),                 
            
                            # "The Tool use data from bi-weekly meeting, email exchange between team members. Project documentation data to report on Information bottlenecks during that period."
                        
        ]
    ),
    style={"padding": "1rem 0rem","width": "50rem",'backgroundColor': colors1['background']},
)

            ])
        ],style={"padding": "1rem 0rem"}),

    ], fluid=True)


date =date.today()
date = date.strftime("%m-%d-%Y")
sidebar = html.Div(
    [
        # html.H2("Sidebar", className="display-4"),
        html.I('Date :: {}'.format(date)),
        html.Hr(),
        # html.P(
        #     "A simple sidebar layout with navigation links", className="lead"
        # ),
        dbc.Nav(
            [   
                html.H5('Bottleneck Reporting'),

                dbc.NavLink("BOTTLENECK REPORTING", href="/dash/page-6", id="page-6-link", active="exact"),

                dbc.NavLink("INFORMATION TREND", href="/dash/page-1", id="page-1-link", active="exact"),
                dbc.NavLink("ISSUE REPORT", href="/dash/page-2", id="page-2-link", active="exact"),
                # dbc.NavLink("WIP & DV", href="/dash/page-3", id="page-3-link"),
                dbc.NavLink("AVG DAYS TO COMPLETE", href="/dash/page-4", id="page-4-link", active="exact"),
                dbc.NavLink("PRODUCTIVITY", href="/dash/page-7", id="page-7-link", active="exact"),
                html.H5('Prediciton'),
                dbc.NavLink("BOTTLENECK PREDICTION", href="/dash/page-8", id="page-8-link", active="exact")
                
                # dbc.NavLink("WIP", href="/page-3", id="page-5-link"),
                # dbc.NavLink("DV", href="/page-3", id="page-6-link"),

            ],
            vertical=True,
            pills=True,
        ),
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)

content = html.Div(

    id="page-content",
    style=CONTENT_STYLE)

#app.layout = html.Div(
 #   [
  #      dcc.Store(id='side_click'),
   #     dcc.Location(id="url"),
  #      navbar,
  #      sidebar,
   #     content,
    #],
#)
# ====================================================================CALLBACK FUNCTION=================================================



 # ================================================================START SERVER==============================================  

#if __name__ == "__main__":
#    app.run_server(debug=True, port=8088,dev_tools_ui=False)