from logging import debug
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime


# loading joblisting dataset
job_listing = pd.read_csv('workinf_df2.csv')

# change datetime
job_listing['date_scrapped'] = pd.to_datetime(job_listing['date_scrapped'])

# number of days passed since posted
days = ['1 day ago', '2 day ago', '2 day ago']


app = dash.Dash(__name__, )

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('explore-img.jpg'),
                     id='Explore-image',
                     style={'height': '200px',
                            'width': 'auto',
                            'margin-bottom': '50px'})


        ], className='one-third column'),

        html.Div([
            html.H3('Job listing Dashboard', style={
                    'margin-bottom': '0px', 'color': 'white'}),
            html.H5('Your dream job is just a click away', style={
                'margin-bottom': '0px', 'color': 'white'})
        ], className='one-half column', id='title'),

        html.Div([
            html.H6('Last Updated: ' + str(job_listing['date_scrapped'].iloc[-1].strftime('%B %d, %Y')) + ' 00:01 (SAST)',
                    style={'color': 'red'})


        ], className='one-third column', id='title1')

    ], id='header', className='row flex-display', style={'margin-bottom': '25px'}),

    html.Div([
        html.Div([
            html.H6(children='Total Jobs available',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{job_listing.index.values[-1]:,.0f}",
                   style={'textAlign': 'center',
                          'color': 'yellow', 'fontsize': 40})

        ], className='card_container three columns'),

        html.Div([
            html.H6(children='Total Remote jobs',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{job_listing['remote'][job_listing['remote']== True].count():,.0f}",
                   style={'textAlign': 'center',
                          'color': 'red', 'fontsize': 40}),
            html.P('New Job Posting: ' + f"{job_listing['remote'][(job_listing['remote'] == True) & (job_listing['date_posted'].isin(days))].count():,.0f}",
                   style={'textAlign': 'center',
                          'color': 'red', 'fontSize': 15,
                          'margin-top': '-18px'}),

        ], className='card_container three columns'),

        html.Div([
            html.H6(children='Total Entry Jobs',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{job_listing['entry'][job_listing['entry']== True].count():,.0f}",
                   style={'textAlign': 'center',
                          'color': 'blue', 'fontsize': 40}),
            html.P('New Entry Jobs: ' + f"{job_listing['entry'][(job_listing['entry'] == True) & (job_listing['date_posted'].isin(days))].count():,.0f}",
                   style={'textAlign': 'center',
                          'color': 'blue', 'fontSize': 15,
                          'margin-top': '-18px'}),

        ], className='card_container three columns')


    ], className='row flex-display'),

    html.Div([
        html.Div([
            html.P('Select Job title: ', className='fix_label',
                   style={'color': 'white'}),
            dcc.Dropdown(id='Job_title',
                         multi=True,
                         searchable=True,
                         value='',
                         placeholder='data science',
                         options=[{'label': c, 'value': c}
                                  for c in (job_listing['title'].unique())], className='dcc.compon'),
        html.Div([
            html.P('Select Job title: ', className='fix_label',
                   style={'color': 'white'}),
            dcc.Dropdown(id='Job_title',
                         multi=True,
                         searchable=True,
                         value='',
                         placeholder='data science',
                         options=[{'label': c, 'value': c}
                                  for c in (job_listing['title'].unique())], className='dcc.compon')
        

        ], className='create_container three columns')


    ], className='row flex-display')

], id='mainContainer', style={'display': 'flex', 'flex-direction': 'column'
                              })


if __name__ == '__main__':
    app.run_server(debug=True)
