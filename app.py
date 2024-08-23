import dash
import dash_auth

VALID_USERNAME_PASSWORD_PAIRS = {
    'root': 'root'
}

app = dash.Dash(__name__, use_pages=True)

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = dash.html.Div([
    dash.html.H1('AYAPAY DASHBOARD'),
    dash.html.Hr(),
    dash.html.Div([
        dash.html.Div(
            dash.dcc.Link(f"{page['name']}", href=page["relative_path"], style={'text-decoration': 'none'})
        ) for page in dash.page_registry.values()
    ], style={'display': 'flex', 'gap': 20, 'margin-bottom': 30, 'justify-content': 'center'}),
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)