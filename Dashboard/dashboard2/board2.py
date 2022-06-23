from logging import debug
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from matplotlib.pyplot import scatter
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, timedelta


from sympy import Line


# loading joblisting dataset from github
url_markets = 'https://raw.githubusercontent.com/johnsiphiwe/EDSA-Project-2022/Scrapping-Joas/CSV_files/Global_Markets.csv'
url_local = 'https://raw.githubusercontent.com/johnsiphiwe/EDSA-Project-2022/Scrapping-Joas/CSV_files/indeed_jobs%20abroad.csv'

job_listing = pd.concat(
    map(pd.read_csv, [url_markets, url_local]))

# remove duplicates
job_listing.drop_duplicates()

# create experience feature


def experience(x):

    junior = ['internship', 'junior', 'graduate']
    mid_level = ['3 years', '4 years', 'exceptional', 'experience']
    senior = ['sr', 'manager', '6 year', '10 years', 'lead']

    for word in x.lower().split():
        if word in junior:
            return 'Junior'
        elif word in senior:
            return 'Senior'
        elif word in mid_level:
            return 'Mid_level 3-5 years'
        else:
            return 'Mid_level 1-2 years'


# apply the experience feature
job_listing['experience'] = job_listing['job_desc'].apply(experience)


# province feature
def province(x):
    type_prov = []
    #x= x.str.replace('[^\w\s\d]',' ')
    provinces = ['gauteng', 'johannesburg', 'sandton', 'parktown', 'natal', 'limpopo', 'durban', 'kwazulu', 'midrand', 'stellenbosch', 'centurion',
                 'western', 'cape', 'pretoria', 'town', 'midrand' 'limpopo', 'north', 'west', 'eastern Cape', 'free' 'State', 'mpumalanga', 'northen cape']
    remote = []
    for word in x.lower().split():
        if word in provinces:
            type_prov.append(word)
        elif word not in provinces:
            remote.append(word)
    for y in type_prov:
        if y == 'johannesburg' or y == 'gauteng' or y == 'midrand' or y == 'pretoria' or y == 'centurion':
            return 'Gauteng'
        elif y == 'stellenbosch' or y == 'western' or y == 'cape':
            return 'Western Cape'
        elif y == 'durban' or y == 'kwazulu':
            return 'Kwazulu-Natal'
        elif y == 'limpopo':
            return 'Limpopo'
        elif y == 'eastern':
            return 'Eastern Cape'
        elif y == 'free state':
            return 'Free State'
        elif y == 'limpopo':
            return 'Limpopo'
        elif y == 'northen cape':
            return 'Northen Cape'
        elif y == 'mpumalanga':
            return ' Mpumalanga'
        elif y == 'north' or 'west':
            return 'North West'
    for z in remote:
        if z in str(['united states', 'somerville', 'plano', 'dearborn', 'MI', 'sydney', 'NSW', 'Tampa', 'FL', 'Dallas', 'TX', 'San', 'Francisco', 'CA', 'Brooklyn', 'NY', 'US', 'Santa Clara', 'Seattle', 'WA', 'Plano', 'TX', 'New York City', 'NY', 'San Diego', 'Mountain View', 'CA', 'Livonia', 'MI', 'McLean', 'IL', 'Winter Park', 'FL']).lower():
            return 'Remote in the US'
        if z in str(['England', 'London', 'Cambridge', 'Manchester', 'Newcastle', 'Strand', 'Bristol Area', 'Bristol Area', 'Oxford', 'Birmingham', 'Nottingham', 'Liverpool', 'County Durham', 'England', 'Cambridge', 'Berkshire', 'Greater London']).lower():
            return 'Remote in England'
        if z in str(['AUE', 'Dubai,Abu Dhabi']).lower():
            return 'Remote in AUE'
        if z in str(['Autralia', 'Canberra', 'ACT']).lower():
            return 'Remote in Australia'
        if z in ['singapore']:
            return 'Remote in Singapore'
        else:
            return 'Remote'

    # apply function
job_listing['province'] = job_listing['location'].apply(province)


# country feature
def country(x):
    provinces = ['Gauteng', 'Limpopo', 'Western Cape', 'Free State',
                 'Eastern Cape', 'Kwazulu-Natal', 'Mpumalanga', 'North West', 'Northern Cape']
    if x in provinces:
        return 'South Africa'
    elif x == 'Remote in the US':
        return 'United States of America'
    elif x == 'Remote in England':
        return 'England'
    elif x == 'Remote in AUE':
        return 'UAE'
    elif x == 'Remote in Singapore':
        return 'Singapore'
    elif x == 'Remote':
        return 'Remote'


# apply feature
job_listing['country'] = job_listing['province'].apply(country)

# creating numbers days from date posted
job_listing['number_days'] = job_listing['date_posted'].str.extract(
    '(\d+)', expand=False)
# change date scrapped to datetime
job_listing['date_scrapped'] = pd.to_datetime(job_listing['date_scrapped'])
# convert number days to date and minus
job_listing['number_days'] = job_listing['number_days'].fillna(0).astype(int)
# creating new feature date
job_listing['date'] = job_listing['date_scrapped'] - \
    pd.to_timedelta(job_listing['number_days'], unit='d')

# creating new titles


def fix_title(x):

    machine_learning = ['machine', 'learning']
    data_scientist = ['data', 'scientist', 'science']
    bus_intel = ['business', 'intelligence', 'developer']
    data_analyst = ['data', 'analyst', ]
    aws = ['aws', 'data', 'science', 'architect']
    data_engineer = ['engineer', 'engineering']
    software = ['software']

    for word in x.lower().split():
        if word in machine_learning:
            return 'Machine Learning'
        elif word in data_scientist:
            return 'Data scientist'
        elif word in bus_intel:
            return 'Business Intelligence'
        elif word in aws:
            return 'AWS Data Science Architect'
        elif word in data_analyst:
            return 'Data analyst'
        elif word in data_engineer:
            return 'Data engineer'
        elif word in software:
            return 'Software Developer'
        else:
            return 'Data Science'


# applying to function to create new feature
job_listing['summary_title'] = job_listing['job_desc'].apply(fix_title)


# dashboard

app = dash.Dash(__name__, meta_tags=[
                {'name': 'viewport', 'content': 'width=device-width'}])

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
            html.Div([
                html.H3('Job Listing Dashboard', style={
                    'margin-bottom': '0px', 'color': 'white'}),
                html.H5('Your Job is few clicks away', style={
                    'margin-bottom': '0px', 'color': 'white'})
            ])

        ], className='one-third column', id='title'),


        html.Div([
            html.H6('Last updated: ' + str(job_listing['date_scrapped'].iloc[-1].strftime('%B %d, %Y')) + ' 00:01 (CAT)',
                    style={'color': 'orange'})

        ], className='one-third column', id='title1')


    ], id='header', className='row flex-display', style={'margin-bottom': '25px'}),


    html.Div([
        html.Div([
            html.P('Select Country', className='fix-label',
                   style={'color': 'white'}),
             dcc.Dropdown(id='countries',
                          multi=False,
                          clearable=True,
                          disabled=False,
                          style={'display': True},
                          value='',
                          placeholder='South Africa',
                          options=[{'label': c, 'value': c}
                                   for c in (job_listing['country'].unique())], className='dcc_compon'),

             html.P('Select Province', className='fix-label',
                    style={'color': 'white'}),
             dcc.Dropdown(id='provinces',
                          multi=False,
                          clearable=True,
                          disabled=False,
                          style={'display': True},
                          placeholder='Gauteng',
                          options=[], className='dcc_compon'),

             html.P('Select Day', className='fix-label', style={
                    'color': 'white', 'margin-left': '1%'}),
             dcc.RangeSlider(id='select_days',
                             min=0,
                             max=30,
                             dots=False,
                             value=[0, 30]),
             html.P('Select Job title', className='fix-label',
                    style={'color': 'white'}),
             dcc.Dropdown(id='job_title',
                          multi=False,
                          clearable=True,
                          disabled=False,
                          style={'display': True},
                          value='',
                          placeholder='Data Science',
                          options=[{'label': c, 'value': c}
                                   for c in (job_listing['summary_title'].unique())], className='dcc_compon'),

             html.P('Select Experience', className='fix-label',
                    style={'color': 'white'}),
             dcc.Dropdown(id='experience',
                          multi=False,
                          clearable=True,
                          disabled=False,
                          style={'display': True},
                          value='',
                          placeholder='Mid_level 1-2 years',
                          options=[{'label': c, 'value': c}
                                   for c in job_listing['experience'].unique()], className='dcc_compon'),



             ], className='create_container three columns')



    ], className='row flex-display')







], id='mainContainer', style={'display': 'flex', 'flex-direction': 'column'})


@app.callback(
    Output('provinces', 'options'),
    [Input('countries', 'value')])
def get_country_options(countries):
    terr3 = job_listing[job_listing['country'] == countries]
    return [{'label': i, 'value': i} for i in terr3['province'].unique()]


#@app.callback(
   # Output('provinces', 'value'),
    #Input('countries', 'value'))
#def get_country_value(countries):
    #return [k['value'] for k in province]


if __name__ == '__main__':
    app.run_server(debug=True)
