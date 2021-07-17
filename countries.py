import requests
import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json

app = dash.Dash(__name__)
def get_countries_df():
    response = requests.get('https://restcountries.eu/rest/v2/all')
    country_list_full = json.loads(response.text)
    country_list_cut = [{} for i in  range(len(country_list_full))]

    for index in range(len(country_list_full)):
            print(country_list_full[index]['name'])
            country_list_cut[index]['name'] = country_list_full[index]['name']
            country_list_cut[index]['alpha2Code'] = country_list_full[index]['alpha2Code']
            country_list_cut[index]['alpha3Code'] = country_list_full[index]['alpha3Code']
            country_list_cut[index]['flag'] = country_list_full[index]['flag']
            country_list_cut[index]['topLevelDomain'] = country_list_full[index]['topLevelDomain']

    #country_list[28]['alpha2Code'] #ba
    #country_list[28]['alpha3Code'] #bih

    df = pd.DataFrame(country_list_cut)
    return df
def table_view(df):
    data_table = dash_table.DataTable(id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['Date', 'Region']
        ],
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        })
    app.layout = html.Div(id='output-dash', children=[data_table],)
    

if __name__ == '__main__':
    df = get_countries_df()
    table_view(df)
    app.run_server(debug=True)
