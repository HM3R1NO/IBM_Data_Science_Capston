# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#Crea un DF con los lugares y coordenadas de los lanzaminetos 
spacex_coordinate_df = spacex_df[['Launch Site', 'class']]
launch_sites_df = spacex_coordinate_df.groupby(['Launch Site'], as_index=False).first()
ls_df = launch_sites_df[['Launch Site']]

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options=[{'label':'All Sites', 'value': 'ALL'},
                                                      {'label':ls_df.iloc[0]['Launch Site'], 'value': ls_df.iloc[0]['Launch Site']},
                                                      {'label':ls_df.iloc[1]['Launch Site'], 'value': ls_df.iloc[1]['Launch Site']},
                                                      {'label':ls_df.iloc[2]['Launch Site'], 'value': ls_df.iloc[2]['Launch Site']},
                                                      {'label':ls_df.iloc[3]['Launch Site'], 'value': ls_df.iloc[3]['Launch Site']}],
                                            value='ALL',
                                            placeholder='Select a Launch Site here',
                                            searchable=True
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0, max=10000, step=1000,
                                               value=[0,10000]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches by Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        fig = px.pie(filtered_df, 
                     names='class', 
                     title=f'Total Success Ratio for {entered_site}')
        return fig 

        

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),Input(component_id='payload-slider', component_property='value')])

def get_scatter_chart(entered_site,selected_payload_range):
    low, high= selected_payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    site_filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)',y='class', 
        color='Booster Version Category',
        title='Correlation Between Payload and Succes for all Sites')
        return fig
    else:
        # return the outcomes scatter for a selected site
        fig = px.scatter(site_filtered_df, 
                     x='Payload Mass (kg)',
                     y='class', 
                     title=f'Correlation Between Payload and Success for {entered_site}')
        return fig 


# Run the app
if __name__ == '__main__':
    app.run_server()
