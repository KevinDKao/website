import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Create some sample data
df = pd.DataFrame({
    'Fruit': ['Apples', 'Oranges', 'Bananas', 'Grapes', 'Strawberries'],
    'Amount': [4, 1, 2, 2, 4],
    'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal']
})

# Initialize the Dash app
app = dash.Dash(__name__)

# Custom CSS styling
app.layout = html.Div([
    # Header section
    html.Div([
        html.H1('🍎 Fruit Sales Dashboard', 
                className='header-title',
                style={
                    'textAlign': 'center', 
                    'color': '#ffffff',
                    'fontSize': '3rem',
                    'fontWeight': '700',
                    'marginBottom': '10px',
                    'textShadow': '2px 2px 4px rgba(0,0,0,0.3)'
                }),
        html.P('Beautiful data visualization made simple', 
               style={
                   'textAlign': 'center', 
                   'color': '#ffffff',
                   'fontSize': '1.2rem',
                   'fontWeight': '300',
                   'opacity': '0.9'
               })
    ], style={
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'padding': '60px 20px',
        'marginBottom': '0px'
    }),
    
    # Main content container
    html.Div([
        # Stats cards row
        html.Div([
            html.Div([
                html.Div([
                    html.H3('🏪', style={'fontSize': '2rem', 'margin': '0'}),
                    html.H4('Total Cities', style={'color': '#666', 'margin': '5px 0'}),
                    html.H2('2', style={'color': '#667eea', 'margin': '0', 'fontSize': '2.5rem'})
                ], className='stat-card')
            ], className='stat-container'),
            
            html.Div([
                html.Div([
                    html.H3('🍓', style={'fontSize': '2rem', 'margin': '0'}),
                    html.H4('Fruit Types', style={'color': '#666', 'margin': '5px 0'}),
                    html.H2('5', style={'color': '#ff6b6b', 'margin': '0', 'fontSize': '2.5rem'})
                ], className='stat-card')
            ], className='stat-container'),
            
            html.Div([
                html.Div([
                    html.H3('📊', style={'fontSize': '2rem', 'margin': '0'}),
                    html.H4('Total Sales', style={'color': '#666', 'margin': '5px 0'}),
                    html.H2('13', style={'color': '#4ecdc4', 'margin': '0', 'fontSize': '2.5rem'})
                ], className='stat-card')
            ], className='stat-container')
        ], style={
            'display': 'flex',
            'justifyContent': 'space-around',
            'flexWrap': 'wrap',
            'marginBottom': '30px'
        }),
        
        # Control panel
        html.Div([
            html.Div([
                html.H3('🎛️ Controls', style={
                    'color': '#333',
                    'marginBottom': '20px',
                    'fontSize': '1.5rem'
                }),
                html.Label('Select a city to filter:', style={
                    'fontWeight': '600', 
                    'marginBottom': '10px',
                    'color': '#555',
                    'display': 'block'
                }),
                dcc.Dropdown(
                    id='city-dropdown',
                    options=[
                        {'label': '🌉 San Francisco', 'value': 'SF'},
                        {'label': '🍁 Montreal', 'value': 'Montreal'},
                        {'label': '🌍 All Cities', 'value': 'ALL'}
                    ],
                    value='ALL',
                    style={
                        'marginBottom': '20px',
                        'borderRadius': '8px'
                    },
                    className='custom-dropdown'
                )
            ], className='control-panel')
        ], style={'marginBottom': '30px'}),
        
        # Chart container
        html.Div([
            html.Div([
                dcc.Graph(id='fruit-graph', className='chart-container')
            ], className='chart-card')
        ])
        
    ], style={
        'maxWidth': '1200px',
        'margin': '0 auto',
        'padding': '30px 20px',
        'backgroundColor': '#f8f9fa'
    })
    
], style={
    'fontFamily': '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif',
    'backgroundColor': '#f8f9fa',
    'minHeight': '100vh'
})

# Custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                margin: 0;
                font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            }
            .stat-card {
                background: white;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
                text-align: center;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                border: 1px solid #e1e8ed;
            }
            .stat-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 35px rgba(0,0,0,0.15);
            }
            .stat-container {
                flex: 1;
                margin: 0 10px;
                min-width: 200px;
            }
            .control-panel {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
                border: 1px solid #e1e8ed;
            }
            .chart-card {
                background: white;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
                border: 1px solid #e1e8ed;
            }
            .custom-dropdown .Select-control {
                border-radius: 8px !important;
                border: 2px solid #e1e8ed !important;
            }
            .custom-dropdown .Select-control:hover {
                border-color: #667eea !important;
            }
            @media (max-width: 768px) {
                .stat-container {
                    margin: 10px 0;
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Callback to update the graph based on dropdown selection
@callback(
    Output('fruit-graph', 'figure'),
    Input('city-dropdown', 'value')
)
def update_graph(selected_city):
    if selected_city == 'ALL':
        filtered_df = df
        title = '🍎 Fruit Sales - All Cities'
    else:
        city_name = 'San Francisco' if selected_city == 'SF' else 'Montreal'
        filtered_df = df[df.City == selected_city]
        title = f'🍎 Fruit Sales - {city_name}'
    
    # Create a beautiful bar chart
    fig = px.bar(filtered_df, x='Fruit', y='Amount', 
                 title=title,
                 color='Amount',
                 color_continuous_scale=['#ff9a9e', '#fecfef', '#fecfef', '#a8edea', '#fed6e3'])
    
    # Update layout for better aesthetics
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#333', 'family': 'Segoe UI'}
        },
        xaxis_title='Fruit Type',
        yaxis_title='Amount Sold',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#666', 'size': 12},
        showlegend=False,
        margin=dict(t=80, b=60, l=60, r=40)
    )
    
    # Update bar appearance
    fig.update_traces(
        marker_line_color='white',
        marker_line_width=2,
        textposition='outside',
        texttemplate='%{y}',
        textfont_size=14,
        textfont_color='#333'
    )
    
    # Style the axes
    fig.update_xaxes(
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='#e1e8ed',
        tickfont={'size': 12, 'color': '#666'}
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#f0f0f0',
        showline=True,
        linewidth=1,
        linecolor='#e1e8ed',
        tickfont={'size': 12, 'color': '#666'}
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)