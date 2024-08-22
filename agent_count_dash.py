from dash import Dash, html, dash_table, dcc, callback, Input, Output
import dash_auth
import pandas as pd
import plotly.graph_objects as go

VALID_USERNAME_PASSWORD_PAIRS = {
    'root': 'root'
}

df = pd.read_csv("./agent_count_tracking.csv")

app = Dash()

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = [
    html.Div(
        children='Agent Count Tracking', 
        style={'font-size': '25px', 'text-align': 'center', 'font-weight': 'bold'}
    ),
    html.Hr(),
    dcc.Checklist( 
        options=[
            {'label': 'All', 'value': 'All'},
            {'label': 'Ahlone', 'value': 'Ahlone'},
            {'label': 'Kyeemyindaing', 'value': 'Kyeemyindaing'},
            {'label': 'Tamwe', 'value': 'Tamwe'},
            {'label': 'Latha', 'value': 'Latha'},
            {'label': 'Dagon Myothit (North)', 'value': 'Dagon Myothit (North)'},
            {'label': 'Mayangone', 'value': 'Mayangone'},
            {'label': 'North Okkalapa', 'value': 'North Okkalapa'},
            {'label': 'Sanchaung', 'value': 'Sanchaung'},
            {'label': 'Thingangyun', 'value': 'Thingangyun'}
        ],
        value=['All'],
        id='controls-and-checkboxes',
        style={'display': 'flex', 'gap': 20, 'margin-bottom': 50}
    ),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    html.Div(id='controls-and-graph-container', style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center'})
]

@callback(
    Output(component_id='controls-and-graph-container', component_property='children'),
    Input(component_id='controls-and-checkboxes', component_property='value')
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


if __name__ == '__main__':
    app.run(debug=True)
