import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv('gyroscope_data.csv')
app = dash.Dash(__name__)
current_start = 0

app.layout = html.Div([
    html.H1("Gyroscope Data Visualization Page"),
    
    html.Div([
        html.Label('Select Your Graph Type >> '),
        dcc.Dropdown(
            id='graph-type',
            options=[
                {'label': 'Scatter Plot', 'value': 'scatter'},
                {'label': 'Line Chart', 'value': 'line'},
                {'label': 'Distribution Plot', 'value': 'distribution'}
            ],
            value='scatter'
        )
    ]),
    
    html.Div([
        html.Label('Select Variables >>'),
        dcc.Dropdown(
            id='data-variables',
            options=[
                {'label': 'X', 'value': 'x'},
                {'label': 'Y', 'value': 'y'},
                {'label': 'Z', 'value': 'z'}
            ],
            value=['x'],
            multi=True
        )
    ]),
    
    html.Div([
        html.Label('Number of Samples >>'),
        dcc.Input(id='num-samples', type='number', value=100, min=1)
    ]),
    
    html.Button('Previous', id='prev-button', n_clicks=0),
    html.Button('Next', id='next-button', n_clicks=0),
    
    dcc.Graph(id='graph'),
    
    html.Div(id='data-summary')
])

@app.callback(
    Output('graph', 'figure'),
    Output('data-summary', 'children'),
    Input('graph-type', 'value'),
    Input('data-variables', 'value'),
    Input('num-samples', 'value'),
    Input('prev-button', 'n_clicks'),
    Input('next-button', 'n_clicks')
)
def update_graph(graph_type, variables, num_samples, prev_clicks, next_clicks):
    global current_start

    if num_samples is None:
        num_samples = 100

    if prev_clicks > next_clicks:
        current_start = max(0, current_start - num_samples)
    elif next_clicks > prev_clicks:
        current_start = min(len(df) - num_samples, current_start + num_samples)

    df_slice = df.iloc[current_start:current_start + num_samples]

    if graph_type == 'scatter':
        fig = px.scatter(df_slice, x='timestamp', y=variables)
    elif graph_type == 'line':
        fig = px.line(df_slice, x='timestamp', y=variables)
    elif graph_type == 'distribution':
        fig = px.histogram(df_slice, x=variables[0])

    summary = df_slice.describe().to_dict()
    summary_html = [html.H4("Data Summary")]
    for key, value in summary.items():
        summary_html.append(html.P(f"{key}: {value}"))

    return fig, summary_html

if __name__ == '__main__':
    app.run_server(debug=True)
