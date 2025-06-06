import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd

# Create some sample data
df = pd.DataFrame({
    'Fruit': ['Apples', 'Oranges', 'Bananas', 'Grapes', 'Strawberries'],
    'Amount': [4, 1, 2, 2, 4],
    'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal']
})

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1('My Simple Dash App', style={'textAlign': 'center', 'color': '#2c3e50'}),
    
    html.Div([
        html.P('Welcome to my first Dash application! This is a simple interactive dashboard.', 
               style={'textAlign': 'center', 'fontSize': 18, 'margin': '20px'})
    ]),
    
    html.Div([
        html.Label('Select a city:', style={'fontWeight': 'bold', 'marginBottom': '10px'}),
        dcc.Dropdown(
            id='city-dropdown',
            options=[
                {'label': 'San Francisco', 'value': 'SF'},
                {'label': 'Montreal', 'value': 'Montreal'},
                {'label': 'All Cities', 'value': 'ALL'}
            ],
            value='ALL',
            style={'marginBottom': '20px'}
        )
    ], style={'width': '48%', 'display': 'inline-block', 'padding': '20px'}),
    
    html.Div([
        dcc.Graph(id='fruit-graph')
    ], style={'padding': '20px'})
])

# Callback to update the graph based on dropdown selection
@callback(
    Output('fruit-graph', 'figure'),
    Input('city-dropdown', 'value')
)
def update_graph(selected_city):
    if selected_city == 'ALL':
        filtered_df = df
        title = 'Fruit Sales - All Cities'
    else:
        filtered_df = df[df.City == selected_city]
        title = f'Fruit Sales - {selected_city}'
    
    fig = px.bar(filtered_df, x='Fruit', y='Amount', 
                 title=title,
                 color='Amount',
                 color_continuous_scale='viridis')
    
    fig.update_layout(
        title_x=0.5,
        xaxis_title='Fruit Type',
        yaxis_title='Amount Sold'
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)