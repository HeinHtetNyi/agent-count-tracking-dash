from dash import html, dash_table, dcc, callback, Input, Output, register_page
import pandas as pd
import plotly.graph_objects as go

register_page(__name__, path="/merchant")

df = pd.read_csv("./preparation/merchant_analysis.csv")

layout = [
    html.Div(
        children='Merchant Analysis', 
        style={'font-size': '25px', 'text-align': 'center', 'font-weight': 'bold', 'margin-bottom': 20}
    ),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    html.Hr(),
    dcc.Dropdown(
        [
            'All', 'Ahlone', 'Kyeemyindaing', 'Tamwe', 'Latha', 'Dagon Myothit (North)',
            'Mayangone', 'North Okkalapa', 'Sanchaung', 'Thingangyun'
        ],
        multi=True,
        value=['All'],
        id='marchant-townships',
        style={'margin-top': 30, 'width': 550}
    ),
    html.Div(id='merchant-graph', style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center'})
]

@callback(
    Output(component_id='merchant-graph', component_property='children'),
    Input(component_id='marchant-townships', component_property='value')
)
def update_graph(chosen_columns):
    if 'All' in chosen_columns:
        selected_rows = df.itertuples()
    else:
        selected_rows = [row for row in df.itertuples() if row[1] in chosen_columns]
        
    graphs = []
    for row in selected_rows:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = int(row[2]),
            title = {'text': row[1]},
            gauge = {
                'axis': {'range': [0, int(row[3])], 'tickwidth': 1, 'tickcolor': "darkred"},
                'bar': {'color': "purple"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, int(row[3])], 'color': 'lightgray'}], 
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': int(row[2])}}
        ))
        graphs.append(dcc.Graph(figure=fig, style={'width': '30%', 'display': 'inline-block'}))
    return graphs

